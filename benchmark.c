#include <stdint.h>
#include <stdio.h>
#include <string.h>
static volatile uint32_t data[4096];
int main(int argc, char **argv) {
    const char *mode = argc > 1 ? argv[1] : "integer";
    uint32_t a=1,b=2,c=3,d=4, seed=7;
    double f=1.1,g=1.2,h=1.3,k=1.4;
    for(unsigned i=0;i<20000;i++) {
        if(!strcmp(mode,"integer")) { a=a*1664525u+1; b=b*22695477u+1; c=c*1103515245u+1; d=d*214013u+1; }
        else if(!strcmp(mode,"floating")) { f=f*1.000001+.01; g=g*1.000002+.02; h=h*1.000003+.03; k=k*1.000004+.04; }
        else if(!strcmp(mode,"memory")) { data[i%4096]=i; a+=data[(i*17)%4096]; }
        else { seed=seed*1664525u+1013904223u; if(seed & 0x10000) a+=i; else b^=i; }
    }
    printf("mode=%s checksum=%u floating=%.6f\n",mode,a+b+c+d,f+g+h+k);
    return 0;
}
