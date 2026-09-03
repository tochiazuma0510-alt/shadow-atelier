/* D972 packed GF(3) stream worker v3.  C11 candidate service. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

#define MAX_WIDTH 10000000ULL
#define MAX_RANK 50000ULL
#define MAX_REDUCTIONS 10000000ULL
typedef struct { uint64_t pivot, coeff; } Pair;
typedef struct { uint8_t *row, *comp; uint64_t lead, id; } Basis;
typedef struct { Pair *p; uint64_t n, cap; } Ledger;
static uint64_t rd64(const uint8_t *p){uint64_t x=0;unsigned i;for(i=0;i<8;i++)x|=((uint64_t)p[i])<<(8*i);return x;}
static void wr64(uint8_t *p,uint64_t x){unsigned i;for(i=0;i<8;i++)p[i]=(uint8_t)(x>>(8*i));}
static int rd(FILE*f,void*p,size_t n){return n==0||fread(p,1,n,f)==n;}
static int trit(const uint8_t*r,uint64_t c){static const unsigned w[4]={1,3,9,27};return(r[c/4]/w[c%4])%3;}
static uint8_t pb(const int*v){return(uint8_t)(v[0]+3*v[1]+9*v[2]+27*v[3]);}
static uint8_t ax(uint8_t a,int c,uint8_t b){int x[4],y[4],z[4],i;static const unsigned w[4]={1,3,9,27};for(i=0;i<4;i++){x[i]=(a/w[i])%3;y[i]=(b/w[i])%3;z[i]=(x[i]-c*y[i])%3;if(z[i]<0)z[i]+=3;}return pb(z);}
static uint8_t s2(uint8_t a){int v[4],i;static const unsigned w[4]={1,3,9,27};for(i=0;i<4;i++)v[i]=(2*((a/w[i])%3))%3;return pb(v);}
static int first(uint8_t a){int i;for(i=0;i<4;i++)if(trit(&a,(uint64_t)i))return i;return-1;}
static int add(Ledger*l,uint64_t p,uint64_t c){Pair*q;uint64_t cap;if(c<1||c>2||l->n>=MAX_REDUCTIONS)return 0;if(l->n==l->cap){cap=l->cap?l->cap*2:8;if(cap<l->cap||cap>MAX_REDUCTIONS)return 0;q=(Pair*)realloc(l->p,(size_t)(cap*sizeof(*q)));if(!q)return 0;l->p=q;l->cap=cap;}l->p[l->n].pivot=p;l->p[l->n].coeff=c;l->n++;return 1;}
static int reduce(uint8_t*w,uint64_t p,int64_t*map,Basis*b,Ledger*l,uint8_t*g,uint64_t cp){uint64_t cur,j,lead,k;int o,c;for(cur=0;cur<p;){if(!w[cur]){cur++;continue;}o=first(w[cur]);if(o<0)return 0;lead=cur*4+(uint64_t)o;if(map[lead]<0)break;k=(uint64_t)map[lead];c=trit(w,lead);if(!add(l,k,c))return 0;for(j=cur;j<p;j++)w[j]=ax(w[j],c,b[k].row[j]);if(g&&cp){if(!b[k].comp)return 0;for(j=0;j<cp;j++)g[j]=ax(g[j],c,b[k].comp[j]);}}return 1;}
static int normal(uint8_t*w,uint64_t p,uint64_t*lead,uint64_t*lc,uint64_t*scale){uint64_t i;int o;for(i=0;i<p&&w[i]==0;i++);if(i==p)return 0;o=first(w[i]);if(o<0)return 0;*lead=i*4+(uint64_t)o;*lc=(uint64_t)trit(w,*lead);*scale=*lc==1?1:2;if(*scale==2)for(i=0;i<p;i++)w[i]=s2(w[i]);return 1;}
static int put64(FILE*f,uint64_t x){uint8_t b[8];wr64(b,x);return fwrite(b,1,8,f)==8;}
static void response(uint8_t status,uint64_t id,uint64_t pivot,uint64_t lead,uint64_t lc,uint64_t scale,const Ledger*l,const uint8_t*g,uint64_t cp){uint8_t h[64];memset(h,0,sizeof(h));memcpy(h,"D2R3",4);h[4]=status;wr64(h+8,id);wr64(h+16,pivot);wr64(h+24,lead);wr64(h+32,lc);wr64(h+40,scale);wr64(h+48,l?l->n:0);wr64(h+56,g?cp:0);fwrite(h,1,sizeof(h),stdout);if(l)for(uint64_t i=0;i<l->n;i++){put64(stdout,l->p[i].pivot);put64(stdout,l->p[i].coeff);}if(g&&cp)fwrite(g,1,(size_t)cp,stdout);fflush(stdout);}
static void usage(void){fprintf(stderr,"usage: --serve --dir DIR --session ID --width N --rank-cap N --offer-cap N --byte-cap N [--companion-width N]\n");}
int main(int argc,char**argv){const char*dir=0;uint64_t session=0,width=0,rank=0,offers=0,bytes=0,cwidth=0,i,j,accepted=0,count=0;int serve=0;int64_t*map=0;Basis*b=0;uint8_t*w=0,*g=0;FILE*bf=0,*lf=0,*tf=0,*of=0,*cf=0;(void)session;(void)bytes;
for(i=1;i<(uint64_t)argc;i++){if(!strcmp(argv[i],"--serve"))serve=1;else if(!strcmp(argv[i],"--dir")&&i+1<(uint64_t)argc)dir=argv[++i];else if(!strcmp(argv[i],"--session")&&i+1<(uint64_t)argc)session=strtoull(argv[++i],0,10);else if(!strcmp(argv[i],"--width")&&i+1<(uint64_t)argc)width=strtoull(argv[++i],0,10);else if(!strcmp(argv[i],"--rank-cap")&&i+1<(uint64_t)argc)rank=strtoull(argv[++i],0,10);else if(!strcmp(argv[i],"--offer-cap")&&i+1<(uint64_t)argc)offers=strtoull(argv[++i],0,10);else if(!strcmp(argv[i],"--byte-cap")&&i+1<(uint64_t)argc)bytes=strtoull(argv[++i],0,10);else if(!strcmp(argv[i],"--companion-width")&&i+1<(uint64_t)argc)cwidth=strtoull(argv[++i],0,10);else{usage();return 2;}}
if(!serve||!dir||!width||width%4||width>MAX_WIDTH||rank==0||rank>MAX_RANK||offers==0||cwidth%4||cwidth>MAX_WIDTH)return 2;uint64_t p=width/4,cp=cwidth/4;map=(int64_t*)malloc((size_t)(width*sizeof(*map)));b=(Basis*)calloc((size_t)rank,sizeof(*b));w=(uint8_t*)malloc((size_t)p);if(cwidth)g=(uint8_t*)malloc((size_t)cp);if(!map||!b||!w||(cwidth&&!g))return 2;for(i=0;i<width;i++)map[i]=-1;
if(dir){char q[4096];snprintf(q,sizeof(q),"%s/basis.bin",dir);bf=fopen(q,"ab+");snprintf(q,sizeof(q),"%s/leads.bin",dir);lf=fopen(q,"ab+");snprintf(q,sizeof(q),"%s/transcript.bin",dir);tf=fopen(q,"ab+");snprintf(q,sizeof(q),"%s/offsets.bin",dir);of=fopen(q,"ab+");if(cwidth){snprintf(q,sizeof(q),"%s/companion.bin",dir);cf=fopen(q,"ab+");}}
/* This v3 candidate intentionally requires a fresh state directory; the
   Python/checker protocol supplies authenticated resumable emulation when no
   compiler is available.  Every live offer below installs basis/map before
   acknowledging it, and dependent offers remain legal at full rank. */
while(1){uint8_t h[16],op;Ledger l={0};uint64_t id,lead=0,lc=0,scale=1;int accepted_row=0,ok=1;op=(uint8_t)getchar();if(feof(stdin))break;if(op==1){if(!rd(stdin,h,8)||!rd(stdin,w,(size_t)p)||(cwidth&&!rd(stdin,g,(size_t)cp))){response(3,0,0,0,0,0,0,0,0);break;}id=rd64(h);for(j=0;j<p;j++)if(w[j]>80)ok=0;for(j=0;j<cp;j++)if(cwidth&&g[j]>80)ok=0;if(!ok){response(3,id,0,0,0,0,0,0,0);continue;}if(!reduce(w,p,map,b,&l,g,cp)){response(4,id,0,0,0,0,&l,0,0);free(l.p);continue;}if(normal(w,p,&lead,&lc,&scale)){if(map[lead]>=0||accepted>=rank){response(2,id,0,0,0,0,&l,0,0);free(l.p);continue;}accepted_row=1;if(cwidth&&scale==2)for(j=0;j<cp;j++)g[j]=s2(g[j]);b[accepted].row=(uint8_t*)malloc((size_t)p);if(cwidth)b[accepted].comp=(uint8_t*)malloc((size_t)cp);if(!b[accepted].row||(cwidth&&!b[accepted].comp)){response(4,id,0,0,0,0,&l,0,0);free(l.p);continue;}memcpy(b[accepted].row,w,(size_t)p);if(cwidth)memcpy(b[accepted].comp,g,(size_t)cp);b[accepted].lead=lead;b[accepted].id=id;map[lead]=(int64_t)accepted;accepted_row=1;}if(of)put64(of,(uint64_t)ftell(tf));if(tf){put64(tf,id);fputc(accepted_row,tf);uint8_t z[7]={0};fwrite(z,1,7,tf);put64(tf,l.n);for(j=0;j<l.n;j++){put64(tf,l.p[j].pivot);fputc((int)l.p[j].coeff,tf);fwrite(z,1,7,tf);}if(accepted_row){put64(tf,accepted);put64(tf,lead);put64(tf,lc);put64(tf,scale);} }if(of)put64(of,(uint64_t)ftell(tf));if(bf&&accepted_row){fwrite(w,1,(size_t)p,bf);if(cwidth)fwrite(g,1,(size_t)cp,bf);}if(lf&&accepted_row){put64(lf,lead);put64(lf,id);}if(cf&&cwidth)fwrite(g,1,(size_t)cp,cf);count++;if(accepted_row)accepted++;response(accepted_row?1:0,id,accepted_row?accepted-1:0,lead,lc,scale,&l,(cwidth?g:0),cp);free(l.p);fprintf(stderr,"PROGRESS offers=%" PRIu64 " accepted=%" PRIu64 "\n",count,accepted);fflush(stderr);}else if(op==2){response(5,0,count,0,0,0,0,0,0);}else if(op==3){response(5,0,count,0,0,0,0,0,0);break;}else{response(3,0,0,0,0,0,0,0,0);break;}}
for(i=0;i<accepted;i++){free(b[i].row);free(b[i].comp);}free(map);free(b);free(w);free(g);if(bf)fclose(bf);if(lf)fclose(lf);if(tf)fclose(tf);if(of)fclose(of);if(cf)fclose(cf);return 0;}
