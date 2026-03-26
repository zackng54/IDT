#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define HOT_SIZE  (4UL  * 1024 * 1024 * 1024)  // 4GB  - accessed frequently
#define WARM_SIZE (8UL  * 1024 * 1024 * 1024)  // 8GB  - accessed occasionally  
#define COLD_SIZE (50UL * 1024 * 1024 * 1024)  // 50GB - rarely accessed
// Total ~62GB: just overflows fast tier (62GB), forces demotion

int main() {
    printf("Allocating hot region  (4GB)...\n");
    char *hot  = malloc(HOT_SIZE);

    printf("Allocating warm region (8GB)...\n");
    char *warm = malloc(WARM_SIZE);

    printf("Allocating cold region (50GB)...\n");
    char *cold = malloc(COLD_SIZE);

    if (!hot || !warm || !cold) {
        fprintf(stderr, "Allocation failed\n");
        return 1;
    }

    // Touch all pages to force physical allocation (move off zero page)
    printf("Faulting in all pages...\n");
    memset(hot,  1, HOT_SIZE);
    memset(warm, 2, WARM_SIZE);
    memset(cold, 3, COLD_SIZE);
    printf("All pages faulted in. Starting access loop...\n");

    long iter = 0;
    while (1) {
        // Hot region: stride access every iteration
        for (size_t i = 0; i < HOT_SIZE; i += 4096)
            hot[i]++;

        // Warm region: every 10 iterations
        if (iter % 10 == 0)
            for (size_t i = 0; i < WARM_SIZE; i += 4096)
                warm[i]++;

        // Cold region: every 100 iterations (IDT should demote this)
        if (iter % 100 == 0)
            for (size_t i = 0; i < COLD_SIZE; i += 4096)
                cold[i]++;

        iter++;
        printf("\riter %ld", iter);
        fflush(stdout);
    }
    return 0;
}
