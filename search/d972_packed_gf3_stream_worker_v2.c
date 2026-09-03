/* D972 persistent packed GF(3) stream worker v2.  Portable C11 candidate. */
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <io.h>
#include <direct.h>
#include <windows.h>
#define fsync_fd _commit
#define file_fd _fileno
#else
#include <sys/stat.h>
#include <unistd.h>
#define fsync_fd fsync
#define file_fd fileno
#endif

#define MAGIC "D972SFV2"
#define MANIFEST_BYTES 296u
#define MAX_WIDTH 10000000ULL
#define MAX_COMPANION_WIDTH 10000000ULL
#define MAX_PROTO_ROW (2500000ULL)
#define MAX_SESSION_PATH 4096u
#define MAX_REDUCTIONS 10000000ULL

typedef struct { uint64_t pivot, coefficient; } Pair;
typedef struct { uint8_t *row; uint64_t lead, id; } Basis;
typedef struct { uint64_t id, n, cap; Pair *pairs; int accepted; uint64_t pivot, lead, lc, scale; } Offer;

static int add_ok(uint64_t a, uint64_t b) { return b <= UINT64_MAX-a; }
static int mul_ok(uint64_t a, uint64_t b) { return a == 0 || b <= UINT64_MAX/a; }
static int read_exact(FILE *f, void *p, size_t n) { return n == 0 || fread(p,1,n,f) == n; }
static uint32_t rd32(const uint8_t *p) { return (uint32_t)p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24); }
static uint64_t rd64(const uint8_t *p) { uint64_t x=0; unsigned i; for(i=0;i<8;i++) x|=((uint64_t)p[i])<<(8*i); return x; }
static void wr32(uint8_t *p, uint32_t x) { p[0]=(uint8_t)x;p[1]=(uint8_t)(x>>8);p[2]=(uint8_t)(x>>16);p[3]=(uint8_t)(x>>24); }
static void wr64(uint8_t *p, uint64_t x) { unsigned i; for(i=0;i<8;i++) p[i]=(uint8_t)(x>>(8*i)); }
static int trit(const uint8_t *r,uint64_t c) { static const unsigned w[4]={1,3,9,27}; return (r[c/4]/w[c%4])%3; }
static uint8_t pack4(const int *v) { return (uint8_t)(v[0]+3*v[1]+9*v[2]+27*v[3]); }
static uint8_t axpy(uint8_t a,int c,uint8_t b) { int x[4],y[4],z[4],i; static const unsigned w[4]={1,3,9,27}; for(i=0;i<4;i++){x[i]=(a/w[i])%3;y[i]=(b/w[i])%3;z[i]=(x[i]-c*y[i])%3;if(z[i]<0)z[i]+=3;} return pack4(z); }
static uint8_t scale2(uint8_t a) { int v[4],i; static const unsigned w[4]={1,3,9,27}; for(i=0;i<4;i++)v[i]=(2*((a/w[i])%3))%3; return pack4(v); }
static int first_trit(uint8_t a) { int i; for(i=0;i<4;i++) if(trit(&a,(uint64_t)i)) return i; return -1; }
static int invariant(const uint8_t *r,uint64_t p,uint64_t lead) { uint64_t c; if(lead>=p*4 || trit(r,lead)!=1)return 0; for(c=0;c<lead;c++)if(trit(r,c))return 0; return 1; }

/* Small self-contained SHA-256 for manifest authentication. */
typedef struct { uint32_t h[8]; uint64_t bits; uint8_t b[64]; size_t n; } Sha;
static uint32_t R(uint32_t x,unsigned n){return (x>>n)|(x<<(32-n));}
static void sha_block(Sha *s,const uint8_t *p){ static const uint32_t k[64]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2}; uint32_t w[64],a,b,c,d,e,f,g,h,t1,t2;unsigned i;for(i=0;i<16;i++)w[i]=((uint32_t)p[4*i]<<24)|((uint32_t)p[4*i+1]<<16)|((uint32_t)p[4*i+2]<<8)|p[4*i+3];for(i=16;i<64;i++){uint32_t q=R(w[i-15],7)^R(w[i-15],18)^(w[i-15]>>3),z=R(w[i-2],17)^R(w[i-2],19)^(w[i-2]>>10);w[i]=w[i-16]+q+w[i-7]+z;}a=s->h[0];b=s->h[1];c=s->h[2];d=s->h[3];e=s->h[4];f=s->h[5];g=s->h[6];h=s->h[7];for(i=0;i<64;i++){t1=h+(R(e,6)^R(e,11)^R(e,25))+((e&f)^((~e)&g))+k[i]+w[i];t2=(R(a,2)^R(a,13)^R(a,22))+((a&b)^(a&c)^(b&c));h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;}s->h[0]+=a;s->h[1]+=b;s->h[2]+=c;s->h[3]+=d;s->h[4]+=e;s->h[5]+=f;s->h[6]+=g;s->h[7]+=h;}
static void sha_init(Sha *s){static const uint32_t h[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};memcpy(s->h,h,sizeof(h));s->bits=0;s->n=0;}
static void sha_update(Sha *s,const uint8_t*p,size_t n){size_t q;while(n){q=64-s->n;if(q>n)q=n;memcpy(s->b+s->n,p,q);s->n+=q;p+=q;n-=q;s->bits+=(uint64_t)q*8;if(s->n==64){sha_block(s,s->b);s->n=0;}}}
static void sha_final(Sha*s,uint8_t out[32]){size_t i;uint64_t bits=s->bits;uint8_t z[128];size_t n=s->n;memset(z,0,sizeof(z));memcpy(z,s->b,n);z[n++]=0x80;while(n%64!=56)n++;for(i=0;i<8;i++)z[n+7-i]=(uint8_t)(bits>>(8*i));n+=8;for(i=0;i<n;i+=64)sha_block(s,z+i);for(i=0;i<8;i++){out[4*i]=(uint8_t)(s->h[i]>>24);out[4*i+1]=(uint8_t)(s->h[i]>>16);out[4*i+2]=(uint8_t)(s->h[i]>>8);out[4*i+3]=(uint8_t)s->h[i];}}
static int hash_file(const char *path,uint8_t out[32],uint64_t *len){FILE*f=fopen(path,"rb");uint8_t b[65536];size_t n;Sha s;if(!f)return 0;sha_init(&s);*len=0;while((n=fread(b,1,sizeof(b),f))){if(!add_ok(*len,n)){fclose(f);return 0;}*len+=n;sha_update(&s,b,n);}if(ferror(f)){fclose(f);return 0;}fclose(f);sha_final(&s,out);return 1;}
static int sync_file(FILE*f){int fd=file_fd(f);if(fflush(f)!=0)return 0;return fsync_fd(fd)==0;}
static int ensure_dir(const char*p){
#ifdef _WIN32
 return _mkdir(p)==0||errno==EEXIST;
#else
 return mkdir(p,0700)==0||errno==EEXIST;
#endif
}
static int truncate_file(const char*p,uint64_t n){FILE*f=fopen(p,"rb+");int ok=0;if(!f)return 0;
#ifdef _WIN32
 ok=_chsize_s(_fileno(f),n)==0;
#else
 ok=ftruncate(fileno(f),(off_t)n)==0;
#endif
 fclose(f);return ok;}

typedef struct { uint64_t session,width,cwidth,rank_cap,offer_cap,byte_cap,offers,accepted,basis_len,leads_len,trans_len,offsets_len,comp_len,fifo_head,fifo_tail; uint8_t hash[5][32]; } Manifest;
static void manifest_encode(const Manifest*m,uint8_t*b){unsigned i;memset(b,0,MANIFEST_BYTES);memcpy(b,MAGIC,8);wr32(b+8,2);wr32(b+12,2);{uint64_t*v=(uint64_t*)(void*)(b+16);(void)v;}for(i=0;i<15;i++){uint64_t x=((const uint64_t*)&m->session)[i];wr64(b+16+8*i,x);}for(i=0;i<5;i++)memcpy(b+136+32*i,m->hash[i],32);}
static int manifest_decode(const uint8_t*b,Manifest*m){unsigned i;if(memcmp(b,MAGIC,8)||rd32(b+8)!=2||rd32(b+12)!=2)return 0;for(i=0;i<15;i++)((uint64_t*)&m->session)[i]=rd64(b+16+8*i);for(i=0;i<5;i++)memcpy(m->hash[i],b+136+32*i,32);return 1;}
static void path_join(char*out,size_t n,const char*d,const char*f){size_t l=strlen(d);if(l+1+strlen(f)+1>n){out[0]=0;return;}memcpy(out,d,l);out[l]=(l&&d[l-1]=='/' )?'/' : '\\';strcpy(out+l+1,f);}
static int write_manifest_atomic(const char*dir,const Manifest*m){char p[MAX_SESSION_PATH],t[MAX_SESSION_PATH];uint8_t b[MANIFEST_BYTES];FILE*f;manifest_encode(m,b);path_join(p,sizeof(p),dir,"manifest.bin");path_join(t,sizeof(t),dir,"manifest.bin.tmp");if(!p[0]||!t[0])return 0;f=fopen(t,"wb");if(!f)return 0;if(fwrite(b,1,sizeof(b),f)!=sizeof(b)||!sync_file(f)){fclose(f);return 0;}fclose(f);
#ifdef _WIN32
 return MoveFileExA(t,p,MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)!=0;
#else
 return rename(t,p)==0;
#endif
}
static int load_manifest(const char*dir,Manifest*m){char p[MAX_SESSION_PATH];uint8_t b[MANIFEST_BYTES];FILE*f;path_join(p,sizeof(p),dir,"manifest.bin");f=fopen(p,"rb");if(!f)return 0;if(!read_exact(f,b,sizeof(b))||fgetc(f)!=EOF){fclose(f);return 0;}fclose(f);return manifest_decode(b,m);}
static int append_bytes(FILE*f,const void*p,uint64_t n){if(n>(uint64_t)SIZE_MAX)return 0;return fwrite(p,1,(size_t)n,f)==(size_t)n;}
static int append_u64(FILE*f,uint64_t x){uint8_t b[8];wr64(b,x);return append_bytes(f,b,8);}
static int append_u64pair(FILE*f,uint64_t a,uint64_t b){return append_u64(f,a)&&append_u64(f,b);}
static void json_pairs(FILE*out,const Pair*p,uint64_t n){uint64_t i;fputc('[',out);for(i=0;i<n;i++){if(i)fputc(',',out);fprintf(out,"[" PRIu64 "," PRIu64 "]",p[i].pivot,p[i].coefficient);}fputc(']',out);}
static int append_pair(Offer*o,uint64_t p,uint64_t c){uint64_t cap;Pair*q;if(c<1||c>2||o->n>=MAX_REDUCTIONS)return 0;if(o->n==o->cap){cap=o->cap?o->cap*2:8;if(cap<o->cap||cap>MAX_REDUCTIONS||!mul_ok(cap,sizeof(Pair)))return 0;q=(Pair*)realloc(o->pairs,(size_t)(cap*sizeof(Pair)));if(!q)return 0;o->pairs=q;o->cap=cap;}o->pairs[o->n].pivot=p;o->pairs[o->n].coefficient=c;o->n++;return 1;}
static int reduce(const uint8_t*in,uint8_t*w,uint64_t p,int64_t*map,Basis*b,Offer*o,uint8_t*comp,uint64_t cp,Basis*cb){uint64_t cur,j,lead,piv,newp;int off,c,lc;(void)in;for(cur=0;cur<p;){if(!w[cur]){cur++;continue;}off=first_trit(w[cur]);if(off<0)return 0;lead=cur*4+(uint64_t)off;if(map[lead]<0)break;piv=(uint64_t)map[lead];c=trit(w,lead);if(!append_pair(o,piv,(uint64_t)c)||!invariant(b[piv].row,p,b[piv].lead))return 0;for(j=cur;j<p;j++)w[j]=axpy(w[j],c,b[piv].row[j]);if(comp&&cp){if(!cb[piv].row)return 0;for(j=0;j<cp;j++)comp[j]=axpy(comp[j],c,cb[piv].row[j]);}}if(comp&&cp&&(lead=0,0)==0){for(cur=0;cur<p&&w[cur]==0;cur++);if(cur<p){off=first_trit(w[cur]);lc=trit(w,cur*4+(uint64_t)off);newp=0;for(j=0;j<p*4;j++)if(map[j]>=0&&((uint64_t)map[j]+1)>newp)newp=(uint64_t)map[j]+1;if(!cb[newp].row){cb[newp].row=(uint8_t*)malloc((size_t)cp);if(!cb[newp].row)return 0;for(j=0;j<cp;j++)cb[newp].row[j]=lc==2?scale2(comp[j]):comp[j];}}}return 1;}
static int normalize(uint8_t*r,uint64_t p,uint64_t*lead,uint64_t*lc,uint64_t*scale){uint64_t b;int o;for(b=0;b<p&&r[b]==0;b++);if(b==p)return 0;o=first_trit(r[b]);if(o<0)return 0;*lead=b*4+(uint64_t)o;*lc=(uint64_t)trit(r,*lead);*scale=*lc==1?1:2;if(*scale==2)for(b=0;b<p;b++)r[b]=scale2(r[b]);return 1;}
static int open_files(const char*dir,FILE**bf,FILE**lf,FILE**tf,FILE**of,FILE**cf,uint64_t cw){char p[MAX_SESSION_PATH];path_join(p,sizeof(p),dir,"basis.bin");*bf=fopen(p,"ab+");path_join(p,sizeof(p),dir,"leads.bin");*lf=fopen(p,"ab+");path_join(p,sizeof(p),dir,"transcript.bin");*tf=fopen(p,"ab+");path_join(p,sizeof(p),dir,"offsets.bin");*of=fopen(p,"ab+");*cf=NULL;if(cw){path_join(p,sizeof(p),dir,"companion.bin");*cf=fopen(p,"ab+");}return *bf&&*lf&&*tf&&*of&&(!cw||*cf);}
static int check_lengths(const char*dir,const Manifest*m){const char*n[5]={"basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"};uint64_t want[5]={m->basis_len,m->leads_len,m->trans_len,m->offsets_len,m->comp_len},got;uint8_t h[32];char p[MAX_SESSION_PATH];unsigned i;for(i=0;i<5;i++){if(i==4&&!m->cwidth)continue;path_join(p,sizeof(p),dir,n[i]);if(!hash_file(p,h,&got)||got<want[i]||memcmp(h,m->hash[i],32)!=0&&got==want[i])return 0;if(got>want[i]&&!truncate_file(p,want[i]))return 0;}return 1;}

static int fresh_state(const char*dir,Manifest*m,uint64_t session,uint64_t width,uint64_t cw,uint64_t rank,uint64_t offers,uint64_t bytes){char p[MAX_SESSION_PATH];FILE*f;unsigned i;uint64_t z;memset(m,0,sizeof(*m));m->session=session;m->width=width;m->cwidth=cw;m->rank_cap=rank;m->offer_cap=offers;m->byte_cap=bytes;if(!ensure_dir(dir))return 0;path_join(p,sizeof(p),dir,"basis.bin");f=fopen(p,"wb");if(!f)return 0;fclose(f);path_join(p,sizeof(p),dir,"leads.bin");f=fopen(p,"wb");if(!f)return 0;fclose(f);path_join(p,sizeof(p),dir,"transcript.bin");f=fopen(p,"wb");if(!f)return 0;fclose(f);path_join(p,sizeof(p),dir,"offsets.bin");f=fopen(p,"wb");if(!f)return 0;fclose(f);if(cw){path_join(p,sizeof(p),dir,"companion.bin");f=fopen(p,"wb");if(!f)return 0;fclose(f);}for(i=0;i<5;i++){if(i==4&&!cw)continue;path_join(p,sizeof(p),dir,(const char*[]){"basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"}[i]);z=0;if(!hash_file(p,m->hash[i],&z))return 0;}return write_manifest_atomic(dir,m);}

static int checkpoint(const char*dir,Manifest*m){const char*n[5]={"basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"};uint64_t*l[5]={&m->basis_len,&m->leads_len,&m->trans_len,&m->offsets_len,&m->comp_len};char p[MAX_SESSION_PATH];unsigned i;for(i=0;i<5;i++){if(i==4&&!m->cwidth)continue;path_join(p,sizeof(p),dir,n[i]);if(!hash_file(p,m->hash[i],l[i]))return 0;}return write_manifest_atomic(dir,m);}
static int validate_transcript(const char*dir,const Manifest*m){char p[MAX_SESSION_PATH];FILE*t,*o;uint64_t n,i,j,start,pos,piv,seen=0;uint8_t h[24],pair[16],meta[32],tail[8];path_join(p,sizeof(p),dir,"transcript.bin");t=fopen(p,"rb");path_join(p,sizeof(p),dir,"offsets.bin");o=fopen(p,"rb");if(!t||!o){if(t)fclose(t);if(o)fclose(o);return 0;}for(i=0;i<m->offers;i++){if(!read_exact(o,tail,8)||!read_exact(t,h,24))goto bad;start=rd64(tail);pos=(uint64_t)ftell(t)-24;if(start!=pos)return 0;n=rd64(h+16);if(n>MAX_REDUCTIONS||!mul_ok(n,16))goto bad;for(j=0;j<n;j++){if(!read_exact(t,pair,16))goto bad;piv=rd64(pair);if(piv>=seen||pair[8]!=1&&pair[8]!=2)goto bad;}if(h[8]==1){if(!read_exact(t,meta,32))goto bad;if(rd64(meta)!=seen||rd64(meta+24)!=1&&rd64(meta+24)!=2)goto bad;seen++;}else if(h[8]!=0||memcmp(h+9,"\0\0\0\0\0\0\0",7))goto bad;}if(seen!=m->accepted||!read_exact(o,tail,8)||rd64(tail)!=(uint64_t)ftell(t)||fgetc(o)!=EOF||fgetc(t)!=EOF){bad: fclose(t);fclose(o);return 0;}fclose(t);fclose(o);return 1;}

static void usage(void){fprintf(stderr,"usage: --serve --dir DIR --session ID --width N --rank-cap N --offer-cap N --byte-cap N [--companion-width N]\n");}
int main(int argc,char**argv){const char*dir=NULL;uint64_t session=0,width=0,cw=0,rank=0,ocap=0,bcap=0,i,j,accepted;int serve=0;Manifest m;FILE*bf=NULL,*lf=NULL,*tf=NULL,*of=NULL,*cf=NULL;int64_t*map=NULL;Basis*basis=NULL,*cbasis=NULL;uint8_t*work=NULL,*comp=NULL,*target=NULL;char p[MAX_SESSION_PATH];
 for(i=1;i<(uint64_t)argc;i++){if(!strcmp(argv[i],"--serve"))serve=1;else if(!strcmp(argv[i],"--dir")&&i+1<(uint64_t)argc)dir=argv[++i];else if(!strcmp(argv[i],"--session")&&i+1<(uint64_t)argc)session=strtoull(argv[++i],NULL,10);else if(!strcmp(argv[i],"--width")&&i+1<(uint64_t)argc)width=strtoull(argv[++i],NULL,10);else if(!strcmp(argv[i],"--rank-cap")&&i+1<(uint64_t)argc)rank=strtoull(argv[++i],NULL,10);else if(!strcmp(argv[i],"--offer-cap")&&i+1<(uint64_t)argc)ocap=strtoull(argv[++i],NULL,10);else if(!strcmp(argv[i],"--byte-cap")&&i+1<(uint64_t)argc)bcap=strtoull(argv[++i],NULL,10);else if(!strcmp(argv[i],"--companion-width")&&i+1<(uint64_t)argc)cw=strtoull(argv[++i],NULL,10);else{usage();return 2;}}
 if(!serve||!dir||!width||width%4||width>MAX_WIDTH||cw%4||cw>MAX_COMPANION_WIDTH||!rank||!ocap||!bcap||rank>50000||!ensure_dir(dir))return 2;
 path_join(p,sizeof(p),dir,"manifest.bin");if(load_manifest(dir,&m)){if(m.session!=session||m.width!=width||m.cwidth!=cw||m.rank_cap!=rank||m.offer_cap!=ocap||m.byte_cap!=bcap)return 2;if(!check_lengths(dir,&m)||!validate_transcript(dir,&m))return 2;}else{if(!fresh_state(dir,&m,session,width,cw,rank,ocap,bcap))return 2;}
 if(!mul_ok(width,sizeof(int64_t))||width*sizeof(int64_t)>(uint64_t)SIZE_MAX||!mul_ok(rank,sizeof(Basis))||rank*sizeof(Basis)>(uint64_t)SIZE_MAX||!mul_ok(width/4,sizeof(uint8_t))||width/4>SIZE_MAX)return 2;map=(int64_t*)malloc((size_t)(width*sizeof(int64_t)));basis=(Basis*)calloc((size_t)(rank?rank:1),sizeof(Basis));if(cw)cbasis=(Basis*)calloc((size_t)(rank?rank:1),sizeof(Basis));work=(uint8_t*)malloc((size_t)(width/4));if(cw)comp=(uint8_t*)malloc((size_t)(cw/4));if(!map||!basis||(!cbasis&&cw)||!work||(!comp&&cw))return 2;for(i=0;i<width;i++)map[i]=-1;accepted=m.accepted;
 if(!open_files(dir,&bf,&lf,&tf,&of,&cf,cw))return 2;path_join(p,sizeof(p),dir,"basis.bin");{FILE*f=fopen(p,"rb");if(!f)return 2;for(i=0;i<accepted;i++){basis[i].row=(uint8_t*)malloc((size_t)(width/4));if(!basis[i].row||!read_exact(f,basis[i].row,(size_t)(width/4)))return 2;path_join(p,sizeof(p),dir,"leads.bin");}fclose(f);}path_join(p,sizeof(p),dir,"leads.bin");{FILE*f=fopen(p,"rb");if(!f)return 2;for(i=0;i<accepted;i++){uint8_t q[16];if(!read_exact(f,q,16)||rd64(q)>=width||rd64(q+8)>=UINT64_MAX)return 2;basis[i].lead=rd64(q);basis[i].id=rd64(q+8);if(map[basis[i].lead]>=0||!invariant(basis[i].row,width/4,basis[i].lead))return 2;map[basis[i].lead]=(int64_t)i;}fclose(f);}
 while(1){int op=getchar();Offer o;uint8_t idb[8];uint64_t pp=width/4,cp=cw/4,start,end;int ok=1;if(op==EOF)break;if(op==1){memset(&o,0,sizeof(o));if(!read_exact(stdin,idb,8)||!read_exact(stdin,idb,0)||!read_exact(stdin,work,(size_t)pp))break;o.id=rd64(idb);for(j=0;j<pp;j++)if(work[j]>80)ok=0;if(cw){if(!read_exact(stdin,comp,(size_t)cp))ok=0;for(j=0;j<cp;j++)if(comp[j]>80)ok=0;}if(m.offers>=m.offer_cap||m.accepted>=m.rank_cap)ok=0;if(!ok){printf("{\"status\":\"UNKNOWN_RESOURCE\"}\n");fflush(stdout);continue;}if(!reduce(work,work,pp,map,basis,&o,comp,cp,cbasis)){printf("{\"status\":\"REJECTED\"}\n");fflush(stdout);free(o.pairs);continue;}if(!normalize(work,pp,&o.lead,&o.lc,&o.scale)){o.accepted=0;}else{o.accepted=1;o.pivot=accepted;if(map[o.lead]>=0||!invariant(work,pp,o.lead))ok=0;if(ok&&cw)for(j=0;j<cp;j++)if(o.scale==2)comp[j]=scale2(comp[j]);}
 if(!ok){free(o.pairs);printf("{\"status\":\"REJECTED\"}\n");fflush(stdout);continue;}if(ftell(tf)<0||ftell(of)<0){free(o.pairs);break;}start=(uint64_t)ftell(tf);if(!append_u64(of,start)){free(o.pairs);break;}if(!append_u64(tf,o.id)){free(o.pairs);break;}fputc(o.accepted?1:0,tf);{uint8_t z[7]={0};append_bytes(tf,z,7);}if(!append_u64(tf,o.n))break;for(j=0;j<o.n;j++){if(!append_u64pair(tf,o.pairs[j].pivot,o.pairs[j].coefficient))break;}if(o.accepted){if(!append_u64(tf,o.pivot)||!append_u64(tf,o.lead)||!append_u64(tf,o.lc)||!append_u64(tf,o.scale))break;if(!append_bytes(bf,work,pp)||!append_u64pair(lf,o.lead,o.id))break;if(cw&&!append_bytes(cf,comp,cp))break;}else if(cw&& !append_bytes(cf,comp,cp))break;end=(uint64_t)ftell(tf);if(!append_u64(of,end)){free(o.pairs);break;}m.offers++;if(o.accepted)m.accepted++;if(o.accepted)accepted++;if(m.trans_len>m.byte_cap||m.offsets_len>m.byte_cap){free(o.pairs);printf("{\"status\":\"UNKNOWN_RESOURCE\"}\n");fflush(stdout);continue;}if(!sync_file(tf)||!sync_file(of)||!sync_file(bf)||!sync_file(lf)||(cf&&!sync_file(cf))||!checkpoint(dir,&m)){free(o.pairs);break;}printf("{\"status\":\"%s\",\"offer\":%" PRIu64 ",\"reductions\":",o.accepted?"ACCEPTED":"DEPENDENT",m.offers);json_pairs(stdout,o.pairs,o.n);if(o.accepted)printf(",\"pivot\":%" PRIu64 ",\"lead\":%" PRIu64 ",\"leading_coefficient\":%" PRIu64 ",\"scale\":%" PRIu64,o.pivot,o.lead,o.lc,o.scale);printf("}\n");fflush(stdout);fprintf(stderr,"PROGRESS offers=%" PRIu64 " accepted=%" PRIu64 "\n",m.offers,m.accepted);fflush(stderr);free(o.pairs);}else if(op==2){if(!checkpoint(dir,&m))break;printf("{\"status\":\"CHECKPOINT\",\"offers\":%" PRIu64 "}\n",m.offers);fflush(stdout);}else if(op==3){checkpoint(dir,&m);printf("{\"status\":\"CLOSED\",\"offers\":%" PRIu64 "}\n",m.offers);fflush(stdout);break;}else break;}
 for(i=0;i<accepted;i++){free(basis[i].row);if(cbasis)free(cbasis[i].row);}free(map);free(basis);free(cbasis);free(work);free(comp);if(bf)fclose(bf);if(lf)fclose(lf);if(tf)fclose(tf);if(of)fclose(of);if(cf)fclose(cf);return 0; }
