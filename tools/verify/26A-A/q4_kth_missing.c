/* 26A-A Q4b: the official findKthMissing, transcribed, against a brute force.
   clang -Wall -Wextra q4_kth_missing.c -o q4.exe && q4.exe  -> prints OK and exits 0 */
#include <stdio.h>
#include <stdlib.h>

int findKthMissing(int A[], int size, int k) {
    int low = 0;
    int high = size - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        int missing = A[mid] - (mid + 1);
        if (missing < k) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return low + k;
}

static int brute(int A[], int size, int k) {
    int x = 0, i = 0;
    while (k) {
        x++;
        while (i < size && A[i] < x) i++;
        if (!(i < size && A[i] == x)) k--;
    }
    return x;
}

int main(void) {
    int ex1[] = {2, 3, 4, 7, 11};
    int ex2[] = {3, 5, 9, 10, 11, 12};
    if (findKthMissing(ex1, 5, 5) != 9) { printf("FAIL ex1\n"); return 1; }
    if (findKthMissing(ex2, 6, 2) != 2) { printf("FAIL ex2 k=2\n"); return 1; }
    if (findKthMissing(ex2, 6, 3) != 4) { printf("FAIL ex2 k=3\n"); return 1; }
    srand(7);
    for (int t = 0; t < 20000; t++) {
        int size = 1 + rand() % 12, A[12], v = 0;
        for (int i = 0; i < size; i++) { v += 1 + rand() % 4; A[i] = v; }
        int k = 1 + rand() % 30;
        if (findKthMissing(A, size, k) != brute(A, size, k)) { printf("FAIL random %d\n", t); return 1; }
    }
    printf("OK\n");
    return 0;
}
