#include <stdio.h>
#include <stdlib.h>
#include "median.h"
#include "pyrost.h"

static int test_median();
static int test_nfft();

int main(int argc, char *argv[])
{
    return test_nfft();
}

static int test_median()
{
    int X = 16;
    int Y = 16;
    double *data = (double *)malloc(X * Y * sizeof(double));
    unsigned char *mask = (unsigned char *)malloc(X * Y);
    double *out = (double *)malloc(X * Y * sizeof(double));

    if (!data || !out)
    {
        printf("not enough memory\n");
        free(data); free(mask); free(out);
        return EXIT_FAILURE;
    }
    for (int i = 0; i < X * Y; i++)
    {data[i] = (double)i; mask[i] = 1;}

    size_t dims[2] = {X, Y};
    size_t fsize[2] = {3, 3};
    double cval = 0.0;

    median_filter(out, data, mask, 2, dims, sizeof(double), fsize,
        EXTEND_MIRROR, &cval, compare_double, 1);

    printf("Result:\n");
    for (int i = 0; i < X; i++)
    {
        for (int j = 0; j < Y; j++) printf("%.0f ", out[i]);
        printf("\n");
    }
    printf("\n");

    free(data); free(mask); free(out);

    return EXIT_SUCCESS;
}

static int test_nfft()
{
    int NF = 10;
    int Y = 1;
    int X = 1000;
    size_t dims[3] = {NF, Y, X};
    double *I_n = (double *)malloc(NF * Y * X * sizeof(double));
    double *W = (double *)malloc(Y * X * sizeof(double));
    double *u = (double *)malloc(2 * Y * X * sizeof(double));
    double *di = (double *)malloc(NF * sizeof(double));
    double *dj = (double *)malloc(NF * sizeof(double));

    for (int i = 0; i < Y; i++)
    {
        for (int j = 0; j < X; j++)
        {
            for (int n = 0; n < NF; n++)
                I_n[n * Y * X + i * X + j] = 5.0 * (n % 2) + 5.0;
            W[i * X + j] = 7.5;
            u[i * X + j] = i; u[i * X + j + Y * X] = j;
        }
    }
    for (int n = 0; n < NF; n++) {di[n] = n * (Y - 1) / 2; dj[n] = n * (X - 1) / 2;}
    
    double *I0, dX0, dY0;
    int X0, Y0;

    make_reference_nfft(&I0, &X0, &Y0, &dX0, &dY0, I_n, W, u, dims, di, dj, 1.0, 1);

    free(I_n); free(W); free(u); free(di); free(dj);
    return EXIT_SUCCESS;
}