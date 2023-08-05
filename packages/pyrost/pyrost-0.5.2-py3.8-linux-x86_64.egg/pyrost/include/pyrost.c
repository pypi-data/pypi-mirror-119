#include "include.h"
#include "array.h"
#include "pocket_fft.h"

#define  NFFT_PRECISION_DOUBLE

#include <nfft3mp.h>

#define FIND_MIN_MAX(_min, _max, _arr, _len)        \
{                                                   \
    int _n;                                         \
    _min = _max = (_arr)[0];                        \
    for (_n = 1; _n < (int)(_len); _n++)            \
    {                                               \
        if (_min > (_arr)[_n]) _min = (_arr)[_n];   \
        if (_max < (_arr)[_n]) _max = (_arr)[_n];   \
    }                                               \
}

int make_reference_nfft(double **I0, int *X0, int *Y0, double *dX0, double *dY0,
    double *I_n, double *W, double *u, size_t *dims, double *di, double *dj,
    double ls, unsigned int threads)
{
    /* check parameters */
    if (!I_n || !W || !u || !dims || !di || !dj)
    {ERROR("make_reference_nfft: one of the arguments is NULL."); return -1;}
    if (ls <= 0) {ERROR("make_reference_nfft: ls must be positive."); return -1;}
    if (threads == 0) {ERROR("make_reference_nfft: threads must be positive."); return -1;}

    omp_set_num_threads(threads);

    size_t udims[3] = {2, dims[1], dims[2]};
    array Iarr = new_array(3, dims, sizeof(double), I_n);
    array Warr = new_array(2, dims + 1, sizeof(double), W);
    array uarr = new_array(3, udims, sizeof(double), u);

    double uy_min, uy_max, ux_min, ux_max;
    FIND_MIN_MAX(uy_min, uy_max, u, uarr->strides[0]);
    FIND_MIN_MAX(ux_min, ux_max, u + uarr->strides[0], uarr->strides[0]);
    if (uy_max == uy_min && ux_max == ux_min) {ERROR("make_reference_nfft: pixel map is constant."); return -1;}

    double di_max, di_min, dj_max, dj_min;
    FIND_MIN_MAX(di_min, di_max, di, dims[0]);
    FIND_MIN_MAX(dj_min, dj_max, dj, dims[0]);
    *dY0 = di_max - uy_min;
    *dX0 = dj_max - ux_min;
    
    *Y0 = uy_max - di_min + *dY0 + 1;
    *X0 = ux_max - dj_min + *dX0 + 1;
    size_t N0[2] = {(*Y0), (*X0)};
    *I0 = (double *)malloc(N0[0] * N0[1] * sizeof(double));
    array I0_arr = new_array(2, N0, sizeof(double), *I0);

    // fastsum_plan fs_plan;
    /* n = p = m = 4 yields 10^-6 accuracy */
    // fastsum_init_guru(&fs_plan, Iarr->size, I0_arr->size, 4, 4, 4);

    free_array(I0_arr); free_array(Iarr); free_array(Warr); free_array(uarr);

    return 0;
}