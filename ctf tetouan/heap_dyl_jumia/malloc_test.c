#include <stdio.h>
#include <stdlib.h>
int main(){
    void *a = malloc(0x26);
    printf("a=%p\n", a);
    free(a);
    void *b = malloc(0x26);
    printf("b=%p\n", b);
    return 0;
}
