/* External-owner GF(3) worker v10. Durable files are read-only inputs. */
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif

#define HLEN 88u
#define MAX_WIDTH 36288u
#define MAX_COMPANION_WIDTH 48384u
#define MAX_RANK 4095u

static uint8_t SUB[3][81][81];
static uint8_t SCALE2[81];
static uint8_t FIRST[81];
static uint8_t *WIRE_BODY;
static size_t WIRE_BODY_CAP;
static uint16_t *LEDGER;

static void init_tables(void) {
    static const unsigned weight[4] = {1u, 3u, 9u, 27u};
    unsigned value, left, right, i;
    for (value = 0; value < 81u; ++value) {
        unsigned x = value;
        FIRST[value] = 4u;
        for (i = 0; i < 4u; ++i) {
            if (x % 3u) {
                FIRST[value] = (uint8_t)i;
                break;
            }
            x /= 3u;
        }
        x = value;
        for (i = 0; i < 4u; ++i) {
            unsigned digit = (2u * (x % 3u)) % 3u;
            SCALE2[value] = (uint8_t)(SCALE2[value] + digit * weight[i]);
            x /= 3u;
        }
    }
    for (left = 0; left < 81u; ++left) {
        for (right = 0; right < 81u; ++right) {
            unsigned coefficient;
            SUB[0][left][right] = (uint8_t)left;
            for (coefficient = 1u; coefficient <= 2u; ++coefficient) {
                unsigned a = left, b = right, packed = 0u;
                for (i = 0; i < 4u; ++i) {
                    int digit = (int)(a % 3u) - (int)coefficient * (int)(b % 3u);
                    digit %= 3;
                    if (digit < 0) {
                        digit += 3;
                    }
                    packed += (unsigned)digit * weight[i];
                    a /= 3u;
                    b /= 3u;
                }
                SUB[coefficient][left][right] = (uint8_t)packed;
            }
        }
    }
}

typedef struct {
    uint8_t *p;
    uint8_t *g;
    uint64_t lead;
    uint64_t id;
} Pivot;

/* 1=full, 0=clean zero-byte EOF, -1=partial/error. */
static int read_full(FILE *f, void *v, size_t n) {
    uint8_t *p = (uint8_t *)v;
    size_t done = 0;
    while (done < n) {
        size_t got = fread(p + done, 1, n - done, f);
        if (!got) {
            return done ? -1 : (feof(f) ? 0 : -1);
        }
        done += got;
    }
    return 1;
}

static int write_full(FILE *f, const void *v, size_t n) {
    const uint8_t *p = (const uint8_t *)v;
    size_t done = 0;
    while (done < n) {
        size_t put = fwrite(p + done, 1, n - done, f);
        if (!put) {
            return 0;
        }
        done += put;
    }
    return 1;
}

static uint64_t get64(const uint8_t *p) {
    uint64_t x = 0;
    unsigned i;
    for (i = 0; i < 8u; ++i) {
        x |= ((uint64_t)p[i]) << (8u * i);
    }
    return x;
}

static void put64(uint8_t *p, uint64_t x) {
    unsigned i;
    for (i = 0; i < 8u; ++i) {
        p[i] = (uint8_t)(x >> (8u * i));
    }
}

static void put16(uint8_t *p, uint16_t x) {
    p[0] = (uint8_t)x;
    p[1] = (uint8_t)(x >> 8);
}

static int u64(const char *s, uint64_t *out) {
    char *end;
    unsigned long long x;
    const char *p;
    if (!s || !*s) {
        return 0;
    }
    for (p = s; *p; ++p) {
        if (*p < '0' || *p > '9') {
            return 0;
        }
    }
    errno = 0;
    end = NULL;
    x = strtoull(s, &end, 10);
    if (errno == ERANGE || end == s || *end) {
        return 0;
    }
    *out = (uint64_t)x;
    return 1;
}

static int trit(const uint8_t *row, uint64_t index) {
    static const unsigned weight[4] = {1u, 3u, 9u, 27u};
    return (int)((row[index / 4u] / weight[index % 4u]) % 3u);
}

static uint8_t pack4(const int *v) {
    return (uint8_t)(v[0] + 3 * v[1] + 9 * v[2] + 27 * v[3]);
}

static uint8_t subbyte(uint8_t a, int coefficient, uint8_t b) {
    static const unsigned weight[4] = {1u, 3u, 9u, 27u};
    int x[4], y[4], z[4], i;
    if (a <= 80u && b <= 80u && coefficient >= 1 && coefficient <= 2) {
        return SUB[coefficient][a][b];
    }
    for (i = 0; i < 4; ++i) {
        x[i] = (a / weight[i]) % 3u;
        y[i] = (b / weight[i]) % 3u;
        z[i] = (x[i] - coefficient * y[i]) % 3;
        if (z[i] < 0) {
            z[i] += 3;
        }
    }
    return pack4(z);
}

static uint8_t twice(uint8_t a) {
    static const unsigned weight[4] = {1u, 3u, 9u, 27u};
    int z[4], i;
    if (a <= 80u) {
        return SCALE2[a];
    }
    for (i = 0; i < 4; ++i) {
        z[i] = (2 * ((a / weight[i]) % 3u)) % 3;
    }
    return pack4(z);
}

static uint64_t first(const uint8_t *row, uint64_t width) {
    uint64_t byte, count = (width + 3u) / 4u;
    for (byte = 0; byte < count; ++byte) {
        if (row[byte]) {
            return byte * 4u + FIRST[row[byte]];
        }
    }
    return width;
}

static uint64_t first_from(const uint8_t *row, uint64_t width, uint64_t *cursor) {
    uint64_t byte = *cursor, count = (width + 3u) / 4u;
    if (byte > count) {
        byte = count;
    }
    for (; byte < count; ++byte) {
        if (row[byte]) {
            *cursor = byte;
            return byte * 4u + FIRST[row[byte]];
        }
    }
    *cursor = count;
    return width;
}

static int bytes_ok(const uint8_t *row, uint64_t n) {
    uint64_t i;
    for (i = 0; i < n; ++i) {
        if (row[i] > 80u) {
            return 0;
        }
    }
    return 1;
}

static int add_ok(uint64_t a, uint64_t b, uint64_t cap, uint64_t *z) {
    if (b > UINT64_MAX - a || a + b > cap) {
        return 0;
    }
    *z = a + b;
    return 1;
}

static int mul_u64(uint64_t a, uint64_t b, uint64_t *z) {
    if (b && a > UINT64_MAX / b) {
        return 0;
    }
    *z = a * b;
    return 1;
}

static int size_ok(uint64_t a, size_t *z) {
    if (a > (uint64_t)SIZE_MAX) {
        return 0;
    }
    *z = (size_t)a;
    return 1;
}

static int response(uint8_t status, uint64_t id, uint64_t offers, uint64_t accepted,
                    uint64_t pivot, uint64_t lead, uint64_t lc, uint64_t scale,
                    uint64_t nq, const uint16_t *q, const uint8_t *primary, uint64_t pn,
                    const uint8_t *companion, uint64_t cn) {
    uint8_t h[HLEN] = {0};
    uint64_t i, body_len;
    if (nq > MAX_RANK || (primary && !bytes_ok(primary, pn)) ||
        (companion && !bytes_ok(companion, cn))) {
        return 0;
    }
    memcpy(h, "EOWA", 4);
    h[4] = 10u;
    h[5] = status;
    put64(h + 8, id);
    put64(h + 16, offers);
    put64(h + 24, accepted);
    put64(h + 32, pivot);
    put64(h + 40, lead);
    put64(h + 48, lc);
    put64(h + 56, scale);
    put64(h + 64, nq);
    put64(h + 72, pn);
    put64(h + 80, cn);
    if (!write_full(stdout, h, HLEN)) {
        return 0;
    }
    if (!add_ok(2u * nq, pn, UINT64_MAX, &body_len) ||
        !add_ok(body_len, cn, UINT64_MAX, &body_len) ||
        body_len > (uint64_t)WIRE_BODY_CAP) {
        return 0;
    }
    for (i = 0; i < nq; ++i) {
        put16(WIRE_BODY + 2u * i, q[i]);
    }
    if (pn) {
        memcpy(WIRE_BODY + 2u * nq, primary, (size_t)pn);
    }
    if (cn) {
        memcpy(WIRE_BODY + 2u * nq + (size_t)pn, companion, (size_t)cn);
    }
    if (!write_full(stdout, WIRE_BODY, (size_t)body_len)) {
        return 0;
    }
    return fflush(stdout) == 0;
}

static int file_len(FILE *f, uint64_t *n) {
    long end;
    if (fseek(f, 0, SEEK_END) != 0) {
        return 0;
    }
    end = ftell(f);
    if (end < 0 || fseek(f, 0, SEEK_SET) != 0) {
        return 0;
    }
    *n = (uint64_t)end;
    return 1;
}

static int load_state(const char *bp, const char *gp, const char *lp, Pivot *basis,
                      int64_t *map, uint64_t accepted, uint64_t width, uint64_t cp,
                      uint64_t cap) {
    FILE *bf = NULL, *gf = NULL, *lf = NULL;
    uint64_t bl = 0, gl = 0, ll = 0, i, lead, id, product;
    uint8_t *p = NULL, *g = NULL, rec[16];
    int ok = 0;
    size_t pn, cn;
    if (!size_ok(width / 4u, &pn) || !size_ok(cp / 4u, &cn)) {
        return 0;
    }
    if (!accepted) {
        if (bp && (bf = fopen(bp, "rb"))) {
            if (!file_len(bf, &bl) || bl) {
                goto done;
            }
            fclose(bf);
            bf = NULL;
        }
        if (gp && (gf = fopen(gp, "rb"))) {
            if (!file_len(gf, &gl) || gl) {
                goto done;
            }
            fclose(gf);
            gf = NULL;
        }
        if (lp && (lf = fopen(lp, "rb"))) {
            if (!file_len(lf, &ll) || ll) {
                goto done;
            }
            fclose(lf);
            lf = NULL;
        }
        return 1;
    }
    if (!bp || !lp || accepted > cap) {
        return 0;
    }
    bf = fopen(bp, "rb");
    lf = fopen(lp, "rb");
    if (cp) {
        gf = gp ? fopen(gp, "rb") : NULL;
    }
    if (!bf || !lf || (cp && !gf) || !file_len(bf, &bl) || !file_len(lf, &ll) ||
        (cp && !file_len(gf, &gl))) {
        goto done;
    }
    if (!mul_u64(accepted, (uint64_t)pn, &product) || bl != product ||
        !mul_u64(accepted, 16u, &product) || ll != product ||
        (cp && (!mul_u64(accepted, (uint64_t)cn, &product) || gl != product))) {
        goto done;
    }
    p = (uint8_t *)malloc(pn);
    if (cp) {
        g = (uint8_t *)malloc(cn);
    }
    if (!p || (cp && !g)) {
        goto done;
    }
    for (i = 0; i < accepted; ++i) {
        uint64_t j;
        if (read_full(bf, p, pn) != 1 || (cp && read_full(gf, g, cn) != 1) ||
            read_full(lf, rec, 16u) != 1) {
            goto done;
        }
        if (!bytes_ok(p, pn) || (cp && !bytes_ok(g, cn))) {
            goto done;
        }
        lead = get64(rec);
        id = get64(rec + 8);
        if (lead >= width || first(p, width) != lead || trit(p, lead) != 1 ||
            map[lead] >= 0 || id == 0) {
            goto done;
        }
        for (j = 0; j < i; ++j) {
            if (basis[j].id == id) {
                goto done;
            }
        }
        basis[i].p = (uint8_t *)malloc(pn);
        if (cp) {
            basis[i].g = (uint8_t *)malloc(cn);
        }
        if (!basis[i].p || (cp && !basis[i].g)) {
            goto done;
        }
        memcpy(basis[i].p, p, pn);
        if (cp) {
            memcpy(basis[i].g, g, cn);
        }
        basis[i].lead = lead;
        basis[i].id = id;
        map[lead] = (int64_t)i;
    }
    ok = 1;
done:
    free(p);
    free(g);
    if (bf) {
        fclose(bf);
    }
    if (gf) {
        fclose(gf);
    }
    if (lf) {
        fclose(lf);
    }
    return ok;
}

static void *accepted_alloc(size_t n) {
#ifdef EOW_TEST_FAIL_ACCEPT_ALLOC
    (void)n;
    return NULL;
#else
    return malloc(n);
#endif
}

int main(int ac, char **av) {
    uint64_t width = 0, cp = 0, rankcap = 0, offercap = 0, bytecap = 0;
    uint64_t session = 0, offers = 0, accepted = 0, logical = 0, i;
    const char *bp = NULL, *gp = NULL, *lp = NULL;
    int serve = 0;
    int64_t *map = NULL;
    uint8_t h[HLEN], *work = NULL, *comp = NULL;
    Pivot *basis = NULL;

    for (i = 1; i < (uint64_t)ac; ++i) {
        const char *key = av[i];
        uint64_t value;
        if (!strcmp(key, "--serve")) {
            serve = 1;
        } else if (i + 1 >= (uint64_t)ac) {
            return 2;
        } else if (!strcmp(key, "--width")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            width = value;
        } else if (!strcmp(key, "--companion-width")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            cp = value;
        } else if (!strcmp(key, "--rank-cap")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            rankcap = value;
        } else if (!strcmp(key, "--offer-cap")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            offercap = value;
        } else if (!strcmp(key, "--byte-cap")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            bytecap = value;
        } else if (!strcmp(key, "--session")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            session = value;
        } else if (!strcmp(key, "--committed-offers")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            offers = value;
        } else if (!strcmp(key, "--committed-accepted")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            accepted = value;
        } else if (!strcmp(key, "--logical-bytes")) {
            if (!u64(av[++i], &value)) {
                return 2;
            }
            logical = value;
        } else if (!strcmp(key, "--basis")) {
            bp = av[++i];
        } else if (!strcmp(key, "--companion")) {
            gp = av[++i];
        } else if (!strcmp(key, "--leads")) {
            lp = av[++i];
        } else {
            return 2;
        }
    }
    (void)session;
    init_tables();
    if (!serve || !width || width > MAX_WIDTH || width % 4u ||
        cp > MAX_COMPANION_WIDTH || cp % 4u || !rankcap || rankcap > MAX_RANK ||
        !offercap || !bytecap || accepted > rankcap || offers > offercap ||
        accepted > offers || logical > bytecap) {
        return 2;
    }
#ifdef _WIN32
    _setmode(_fileno(stdin), _O_BINARY);
    _setmode(_fileno(stdout), _O_BINARY);
#endif
    {
        size_t width_size, primary_size, companion_size, ledger_size;
        uint64_t product;
        if (!size_ok(width, &width_size) || !size_ok(width / 4u, &primary_size) ||
            !size_ok(cp / 4u, &companion_size) ||
            !mul_u64(width, sizeof(*map), &product) || !size_ok(product, &width_size) ||
            !mul_u64(rankcap, sizeof(*basis), &product) || !size_ok(product, &width_size)) {
            return 2;
        }
        map = (int64_t *)malloc((size_t)width * sizeof(*map));
        basis = (Pivot *)calloc((size_t)rankcap, sizeof(*basis));
        work = (uint8_t *)malloc(primary_size);
        if (cp) {
            comp = (uint8_t *)malloc(companion_size);
        }
        if (!mul_u64(rankcap, 2u, &product) ||
            !add_ok(product, width / 4u, UINT64_MAX, &product) ||
            !add_ok(product, cp / 4u, UINT64_MAX, &product) ||
            !size_ok(product, &WIRE_BODY_CAP)) {
            free(map);
            free(basis);
            free(work);
            free(comp);
            return 2;
        }
        WIRE_BODY = (uint8_t *)malloc(WIRE_BODY_CAP);
        if (!mul_u64(rankcap, 2u, &product) || !size_ok(product, &ledger_size)) {
            free(map);
            free(basis);
            free(work);
            free(comp);
            free(WIRE_BODY);
            return 2;
        }
        LEDGER = (uint16_t *)malloc(ledger_size);
    }
    if (!map || !basis || !work || (cp && !comp) || !WIRE_BODY || !LEDGER) {
        free(map);
        free(basis);
        free(work);
        free(comp);
        free(WIRE_BODY);
        free(LEDGER);
        return 5;
    }
    for (i = 0; i < width; ++i) {
        map[i] = -1;
    }
    if (!load_state(bp, gp, lp, basis, map, accepted, width, cp, rankcap)) {
        for (i = 0; i < accepted; ++i) {
            free(basis[i].p);
            free(basis[i].g);
        }
        free(map);
        free(basis);
        free(work);
        free(comp);
        free(WIRE_BODY);
        free(LEDGER);
        return 5;
    }

    for (;;) {
        uint64_t id, committed_offers, committed_accepted, count, lead, lc, scale;
        uint64_t charge, next, scan = 0;
        uint16_t *q = LEDGER;
        int valid = 1;
        size_t pn = (size_t)(width / 4u), cn = (size_t)(cp / 4u);
        int header_result = read_full(stdin, h, HLEN);
        if (header_result == 0) {
            goto clean_cleanup;
        }
        if (header_result != 1) {
            goto fatal_cleanup;
        }
        if (memcmp(h, "EORA", 4) || h[4] != 10u || h[6] || h[7]) {
            goto fatal_cleanup;
        }
        id = get64(h + 8);
        committed_offers = get64(h + 16);
        committed_accepted = get64(h + 24);
        if (committed_offers != offers || committed_accepted != accepted) {
            if (!response(3u, id, offers, accepted, 0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            goto fatal_cleanup;
        }
        if (h[5] == 2u || h[5] == 3u) {
            if (id || get64(h + 32) || get64(h + 40) || get64(h + 48) ||
                get64(h + 56) || get64(h + 64) || get64(h + 72) || get64(h + 80)) {
                if (!response(3u, id, offers, accepted, 0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                    goto fatal_cleanup;
                }
                goto fatal_cleanup;
            }
            if (!response(h[5] == 2u ? 5u : 6u, 0, offers, accepted,
                          0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            if (h[5] == 3u) {
                break;
            }
            continue;
        }
        if (h[5] != 1u || id == 0 || get64(h + 32) || get64(h + 40) ||
            get64(h + 48) || get64(h + 56) || get64(h + 64) ||
            get64(h + 72) != (uint64_t)pn || get64(h + 80) != (uint64_t)cn) {
            if (!response(3u, id, offers, accepted, 0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            goto fatal_cleanup;
        }
        if (read_full(stdin, work, pn) != 1 || (cp && read_full(stdin, comp, cn) != 1)) {
            goto fatal_cleanup;
        }
        if (!bytes_ok(work, pn) || (cp && !bytes_ok(comp, cn))) {
            if (!response(3u, id, offers, accepted, 0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            goto fatal_cleanup;
        }
        count = 0;
        while ((lead = first_from(work, width, &scan)) < width) {
            uint64_t pivot = (uint64_t)map[lead];
            int coefficient;
            if (map[lead] < 0 || pivot >= accepted) {
                break;
            }
            coefficient = trit(work, lead);
            if (coefficient < 1 || coefficient > 2 || count >= accepted) {
                valid = 0;
                break;
            }
            q[count++] = (uint16_t)(2u * pivot + (uint64_t)coefficient - 1u);
            for (i = 0; i < pn; ++i) {
                work[i] = subbyte(work[i], coefficient, basis[pivot].p[i]);
            }
            if (cp) {
                for (i = 0; i < cn; ++i) {
                    comp[i] = subbyte(comp[i], coefficient, basis[pivot].g[i]);
                }
            }
        }
        if (!valid) {
            if (!response(4u, id, offers, accepted, 0, 0, 0, 0, 0, NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            goto fatal_cleanup;
        }
        if (first_from(work, width, &scan) == width) {
            if (!add_ok(56u, 2u * count, UINT64_MAX, &charge) ||
                !add_ok(charge, 8u, UINT64_MAX, &charge)) {
                goto fatal_cleanup;
            }
            if (!add_ok(logical, charge, bytecap, &next) || offers >= offercap) {
                if (!response(2u, id, offers, accepted, 0, 0, 0, 0, 0,
                              NULL, NULL, 0, NULL, 0)) {
                    goto fatal_cleanup;
                }
                continue;
            }
            ++offers;
            logical = next;
            if (!response(0u, id, offers, accepted, 0, 0, 0, 0, count,
                          q, NULL, 0, comp, cn)) {
                goto fatal_cleanup;
            }
            continue;
        }
        lead = first_from(work, width, &scan);
        lc = (uint64_t)trit(work, lead);
        scale = lc == 1u ? 1u : 2u;
        if (!add_ok(56u, 2u * count, UINT64_MAX, &charge) ||
            !add_ok(charge, 8u, UINT64_MAX, &charge)) {
            goto fatal_cleanup;
        }
        {
            uint64_t extra;
            if (!add_ok((uint64_t)pn, (uint64_t)cn, UINT64_MAX, &extra) ||
                !add_ok(extra, 16u, UINT64_MAX, &extra) ||
                !add_ok(charge, extra, UINT64_MAX, &charge)) {
                goto fatal_cleanup;
            }
        }
        if (!add_ok(logical, charge, bytecap, &next) || offers >= offercap ||
            accepted >= rankcap) {
            if (!response(2u, id, offers, accepted, 0, 0, 0, 0, 0,
                          NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            continue;
        }
        if (scale == 2u) {
            for (i = 0; i < pn; ++i) {
                work[i] = twice(work[i]);
            }
            if (cp) {
                for (i = 0; i < cn; ++i) {
                    comp[i] = twice(comp[i]);
                }
            }
        }
        basis[accepted].p = (uint8_t *)accepted_alloc(pn);
        if (basis[accepted].p && cp) {
            basis[accepted].g = (uint8_t *)accepted_alloc(cn);
        }
        if (!basis[accepted].p || (cp && !basis[accepted].g)) {
            free(basis[accepted].p);
            free(basis[accepted].g);
            basis[accepted].p = NULL;
            basis[accepted].g = NULL;
            if (!response(4u, id, offers, accepted, 0, 0, 0, 0, 0,
                          NULL, NULL, 0, NULL, 0)) {
                goto fatal_cleanup;
            }
            goto fatal_cleanup;
        }
        memcpy(basis[accepted].p, work, pn);
        if (cp) {
            memcpy(basis[accepted].g, comp, cn);
        }
        basis[accepted].lead = lead;
        basis[accepted].id = id;
        map[lead] = (int64_t)accepted;
        ++accepted;
        ++offers;
        logical = next;
        if (!response(1u, id, offers, accepted, accepted - 1u, lead, lc, scale,
                      count, q, work, pn, comp, cn)) {
            goto fatal_cleanup;
        }
    }

clean_cleanup:
    for (i = 0; i < accepted; ++i) {
        free(basis[i].p);
        free(basis[i].g);
    }
    free(map);
    free(basis);
    free(work);
    free(comp);
    free(WIRE_BODY);
    free(LEDGER);
    return 0;

fatal_cleanup:
    for (i = 0; i < accepted; ++i) {
        free(basis[i].p);
        free(basis[i].g);
    }
    free(map);
    free(basis);
    free(work);
    free(comp);
    free(WIRE_BODY);
    free(LEDGER);
    return 6;
}
