#include <stdio.h>

#define V 4
#define INF 99999

void printMatrix(int d[V][V], const char *title) {
    printf("%s\n", title);
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            if (d[i][j] == INF) printf("%5s", "INF");
            else printf("%5d", d[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void floydWarshall(int d[V][V]) {
    printMatrix(d, "D(0): direct edges");
    for (int k = 0; k < V; k++) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (d[i][k] != INF && d[k][j] != INF &&
                    d[i][k] + d[k][j] < d[i][j]) {
                    printf("k=%d: D[%d][%d] %d -> %d\n", k + 1, i + 1, j + 1,
                           d[i][j], d[i][k] + d[k][j]);
                    d[i][j] = d[i][k] + d[k][j];
                }
            }
        }
        char title[32];
        sprintf(title, "D(%d): pivot vertex %d", k + 1, k + 1);
        printMatrix(d, title);
    }
}

int main(void) {
    int d[V][V] = {
        {0,   3,   INF, 7},
        {8,   0,   2,   INF},
        {5,   INF, 0,   1},
        {2,   INF, INF, 0}
    };
    floydWarshall(d);
    return 0;
}