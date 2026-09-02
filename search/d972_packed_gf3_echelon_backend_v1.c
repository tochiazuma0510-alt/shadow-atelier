/* D972 packed GF(3) echelon backend candidate.  Portable C11, schema v1. */
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAGIC "D972P3GF"
#define MAGIC_BYTES 8u
#define HEADER_BYTES 48u
#define SCHEMA_NAME "packed-gf3-echelon-v1"
#define MAX_WIDTH 10000000ULL
#define MAX_ROWS 100000ULL
#define MAX_LEDGER 10000000ULL
#define MAX_STATE_BYTES (512ULL * 1024ULL * 1024ULL)

typedef struct { uint64_t pivot, coefficient; } Reduction;
typedef struct {
    uint64_t id;
    uint8_t *row;
    uint64_t lead;
} Basis;
typedef struct {
    uint64_t id;
    Reduction *red;
    uint64_t nred, capred;
    int accepted;
    uint64_t pivot, lead, leading_coefficient, scale;
} Offered;

static int add_ok(uint64_t a, uint64_t b) { return b <= UINT64_MAX - a; }
static int mul_ok(uint64_t a, uint64_t b) { return a == 0 || b <= UINT64_MAX / a; }
static int read_exact(FILE *f, void *p, size_t n) { return n == 0 || fread(p, 1, n, f) == n; }
static uint32_t le32(const uint8_t *p) { return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24); }
static uint64_t le64(const uint8_t *p) {
    uint64_t x = 0; unsigned i;
    for (i = 0; i < 8; ++i) x |= ((uint64_t)p[i]) << (8u * i);
    return x;
}
static void put_u64(uint8_t *p, uint64_t x) {
    unsigned i; for (i = 0; i < 8; ++i) p[i] = (uint8_t)(x >> (8u * i));
}
static int trit(const uint8_t *row, uint64_t coord) {
    return (int)((row[coord / 4u] / (uint8_t)(coord % 4u == 0 ? 1 : coord % 4u == 1 ? 3 : coord % 4u == 2 ? 9 : 27)) % 3u);
}
static uint8_t pack4(const int *v) { return (uint8_t)(v[0] + 3*v[1] + 9*v[2] + 27*v[3]); }
static uint8_t axpy_byte(uint8_t a, uint8_t c, uint8_t b) {
    int x[4], y[4], z[4], i;
    for (i = 0; i < 4; ++i) { x[i] = (a / (i == 0 ? 1 : i == 1 ? 3 : i == 2 ? 9 : 27)) % 3; y[i] = (b / (i == 0 ? 1 : i == 1 ? 3 : i == 2 ? 9 : 27)) % 3; z[i] = (x[i] - (int)c*y[i]) % 3; if (z[i] < 0) z[i] += 3; }
    return pack4(z);
}
static int first_trit(uint8_t b) { int i; for (i = 0; i < 4; ++i) if (trit(&b, (uint64_t)i)) return i; return -1; }
static int row_invariant(const uint8_t *row, uint64_t packed, uint64_t lead) {
    uint64_t c;
    if (lead >= packed * 4u || trit(row, lead) != 1) return 0;
    for (c = 0; c < lead; ++c) if (trit(row, c) != 0) return 0;
    return 1;
}
static int append_red(Offered *o, uint64_t pivot, uint64_t coefficient, uint64_t *ledger_total) {
    Reduction *p; uint64_t ncap;
    if (o->nred >= MAX_LEDGER || *ledger_total >= MAX_LEDGER) return 0;
    if (o->nred == o->capred) {
        ncap = o->capred ? o->capred * 2u : 8u;
        if (ncap < o->capred || ncap > MAX_LEDGER || !mul_ok(ncap, sizeof(*p))) return 0;
        p = (Reduction *)realloc(o->red, (size_t)(ncap * sizeof(*p))); if (!p) return 0;
        o->red = p; o->capred = ncap;
    }
    o->red[o->nred].pivot = pivot; o->red[o->nred].coefficient = coefficient; ++o->nred; ++*ledger_total;
    return 1;
}
static int reduce(const uint8_t *input, uint8_t *work, uint64_t packed, int64_t *lead_to_pivot, Basis *basis, Offered *o, uint64_t *ledger_total) {
    uint64_t cursor, j, lead, pivot; int off, coeff;
    memcpy(work, input, (size_t)packed);
    for (cursor = 0; cursor < packed;) {
        if (work[cursor] == 0) { ++cursor; continue; }
        off = first_trit(work[cursor]); if (off < 0) return 0;
        lead = cursor * 4u + (uint64_t)off; pivot = (uint64_t)(lead_to_pivot[lead]);
        if (lead_to_pivot[lead] < 0) break;
        coeff = trit(work, lead); if (coeff != 1 && coeff != 2) return 0;
        if (!append_red(o, pivot, (uint64_t)coeff, ledger_total)) return 0;
        /* The invariant is checked on every pivot before suffix update. */
        if (!row_invariant(basis[pivot].row, packed, basis[pivot].lead)) return 0;
        for (j = cursor; j < packed; ++j) work[j] = axpy_byte(work[j], (uint8_t)coeff, basis[pivot].row[j]);
    }
    return 1;
}
static int normalize(uint8_t *row, uint64_t packed, uint64_t *lead, uint64_t *lc, uint64_t *scale) {
    uint64_t b; int off, i, v[4];
    for (b = 0; b < packed && row[b] == 0; ++b) {}
    if (b == packed) return 0;
    off = first_trit(row[b]); if (off < 0) return 0;
    *lead = b * 4u + (uint64_t)off; *lc = (uint64_t)trit(row, *lead); *scale = *lc == 1 ? 1u : 2u;
    if (*scale == 2u) for (b = 0; b < packed; ++b) { for (i = 0; i < 4; ++i) v[i] = (row[b] / (i == 0 ? 1 : i == 1 ? 3 : i == 2 ? 9 : 27)) % 3; for (i = 0; i < 4; ++i) v[i] = (2*v[i]) % 3; row[b] = pack4(v); }
    return 1;
}
static void json_bytes(FILE *out, const uint8_t *row, uint64_t n) {
    uint64_t i; fputc('[', out); for (i = 0; i < n; ++i) { if (i) fputc(',', out); fprintf(out, "%u", (unsigned)row[i]); } fputc(']', out);
}
static void json_red(FILE *out, const Reduction *r, uint64_t n) {
    uint64_t i; fputc('[', out); for (i = 0; i < n; ++i) { if (i) fputc(',', out); fprintf(out, "[%" PRIu64 ",%" PRIu64 "]", r[i].pivot, r[i].coefficient); } fputc(']', out);
}
static void free_offered(Offered *o, uint64_t n) { uint64_t i; if (!o) return; for (i = 0; i < n; ++i) free(o[i].red); free(o); }
static void usage(void) { fprintf(stderr, "usage: backend --version 1 --schema " SCHEMA_NAME " --input FILE --output FILE\n"); }

int main(int argc, char **argv) {
    const char *input_path = NULL, *output_path = NULL, *version = NULL, *schema = NULL;
    FILE *in = NULL, *out = NULL; uint8_t h[HEADER_BYTES], *work = NULL, *target = NULL;
    Basis *basis = NULL; Offered *off = NULL; int64_t *lead_to_pivot = NULL; uint64_t width, packed, nrows, i, j, id;
    uint32_t hv, hs; uint64_t accepted = 0, lead, lc, scale, ledger_total = 0; int rc = 2; Offered target_o;
    memset(&target_o, 0, sizeof(target_o));
    for (i = 1; i < (uint64_t)argc; ++i) {
        if (strcmp(argv[i], "--input") == 0 && i+1 < (uint64_t)argc) input_path = argv[++i];
        else if (strcmp(argv[i], "--output") == 0 && i+1 < (uint64_t)argc) output_path = argv[++i];
        else if (strcmp(argv[i], "--version") == 0 && i+1 < (uint64_t)argc) version = argv[++i];
        else if (strcmp(argv[i], "--schema") == 0 && i+1 < (uint64_t)argc) schema = argv[++i];
        else { usage(); goto done; }
    }
    if (!input_path || !output_path || !version || !schema || strcmp(version, "1") || strcmp(schema, SCHEMA_NAME)) { usage(); goto done; }
    in = fopen(input_path, "rb"); if (!in) goto done;
    if (!read_exact(in, h, sizeof(h)) || memcmp(h, MAGIC, MAGIC_BYTES) != 0) goto done;
    hv = le32(h+8); hs = le32(h+12); width = le64(h+16); nrows = le64(h+24); packed = le64(h+32);
    if (hv != 1u || hs != 1u || le64(h+40) != 0 || width == 0 || width > MAX_WIDTH || width % 4u || packed != width/4u || nrows > MAX_ROWS) goto done;
    if (!mul_ok(packed, sizeof(uint8_t)) || packed > (uint64_t)SIZE_MAX || !mul_ok(width, sizeof(*lead_to_pivot)) || width * sizeof(*lead_to_pivot) > (uint64_t)SIZE_MAX || !mul_ok(nrows, sizeof(*basis)) || nrows * sizeof(*basis) > (uint64_t)SIZE_MAX || !mul_ok(nrows, sizeof(*off)) || nrows * sizeof(*off) > (uint64_t)SIZE_MAX) goto done;
    /* Check the complete declared payload size before any allocation/read. */
    if (!mul_ok(nrows, 8u + packed) || !add_ok(HEADER_BYTES, nrows * (8u + packed)) || !add_ok(HEADER_BYTES + nrows * (8u + packed), packed) || !mul_ok(nrows, packed) || nrows * packed > MAX_STATE_BYTES) goto done;
    lead_to_pivot = (int64_t *)malloc((size_t)(width * sizeof(*lead_to_pivot))); if (!lead_to_pivot) goto done;
    for (i = 0; i < width; ++i) lead_to_pivot[i] = -1;
    work = (uint8_t *)malloc((size_t)packed); target = (uint8_t *)malloc((size_t)packed);
    basis = (Basis *)calloc((size_t)(nrows ? nrows : 1u), sizeof(*basis)); off = (Offered *)calloc((size_t)(nrows ? nrows : 1u), sizeof(*off));
    if (!work || !target || !basis || !off) goto done;
    for (i = 0; i < nrows; ++i) {
        uint8_t idbuf[8]; off[i].red = NULL;
        if (!read_exact(in, idbuf, 8) || !read_exact(in, work, (size_t)packed)) goto done;
        id = le64(idbuf); off[i].id = id; for (j = 0; j < packed; ++j) if (work[j] > 80u) goto done;
        if (!reduce(work, work, packed, lead_to_pivot, basis, &off[i], &ledger_total)) goto done;
        if (!normalize(work, packed, &lead, &lc, &scale)) { off[i].accepted = 0; continue; }
        if (lead_to_pivot[lead] >= 0 || !row_invariant(work, packed, lead)) goto done;
        off[i].accepted = 1; off[i].pivot = accepted; off[i].lead = lead; off[i].leading_coefficient = lc; off[i].scale = scale;
        basis[accepted].id = id; basis[accepted].lead = lead; basis[accepted].row = (uint8_t *)malloc((size_t)packed); if (!basis[accepted].row) goto done; memcpy(basis[accepted].row, work, (size_t)packed);
        lead_to_pivot[lead] = (int64_t)accepted; ++accepted;
    }
    if (!read_exact(in, target, (size_t)packed)) goto done; for (j = 0; j < packed; ++j) if (target[j] > 80u) goto done;
    if (fgetc(in) != EOF || ferror(in)) goto done;
    if (!reduce(target, target, packed, lead_to_pivot, basis, &target_o, &ledger_total)) goto done;
    out = fopen(output_path, "wb"); if (!out) goto done;
    fprintf(out, "{\"version\":1,\"schema\":\"" SCHEMA_NAME "\",\"width\":%" PRIu64 ",\"packed_bytes\":%" PRIu64 ",\"accepted_basis\":[", width, packed);
    for (i = 0; i < accepted; ++i) { if (i) fputc(',', out); fprintf(out, "{\"pivot\":%" PRIu64 ",\"row_id\":%" PRIu64 ",\"lead\":%" PRIu64 ",\"bytes\":", i, basis[i].id, basis[i].lead); json_bytes(out, basis[i].row, packed); fputc('}', out); }
    fprintf(out, "],\"offered\":[");
    for (i = 0; i < nrows; ++i) { if (i) fputc(',', out); fprintf(out, "{\"row_id\":%" PRIu64 ",\"reductions\":", off[i].id); json_red(out, off[i].red, off[i].nred); fprintf(out, ",\"accepted\":%s", off[i].accepted ? "true" : "false"); if (off[i].accepted) fprintf(out, ",\"pivot\":%" PRIu64 ",\"lead\":%" PRIu64 ",\"leading_coefficient\":%" PRIu64 ",\"scale\":%" PRIu64, off[i].pivot, off[i].lead, off[i].leading_coefficient, off[i].scale); fputc('}', out); }
    fprintf(out, "],\"target\":{\"reductions\":"); json_red(out, target_o.red, target_o.nred); fprintf(out, ",\"coefficients\":"); json_red(out, target_o.red, target_o.nred); fprintf(out, ",\"remainder\":"); json_bytes(out, target, packed); fprintf(out, "}}\n");
    if (fclose(out) != 0) { out = NULL; goto done; } out = NULL; rc = 0;
done:
    if (out) fclose(out); if (in) fclose(in); for (i = 0; i < accepted; ++i) free(basis[i].row); free(basis); free_offered(off, nrows); free(target_o.red); free(work); free(target); free(lead_to_pivot); return rc;
}
