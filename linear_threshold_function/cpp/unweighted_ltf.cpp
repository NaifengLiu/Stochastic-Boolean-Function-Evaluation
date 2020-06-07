#ifdef __cplusplus
extern "C" char get_non_adaptive_cost_unit_cost(int k, int n, double* p)
#else
double get_non_adaptive_cost_unit_cost(int k, int n, double* p)
#endif
{

    int z = n - k + 1;

    double** P = new double* [n+1];
    for (int i = 0; i <= n; i++)
    {
        P[i] = new double[k+1];
    }

    P[0][0] = 1;

    for (int j = 1; j <= k; j++)
    {
        P[0][j] = 0;
    }

    for (int i = 1; i <= n; i++)
    {
        P[i][0] = 1;
        for (int a = 1; a <= i; a++) {
            P[i][0] *= (1 - p[a-1]);
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= k; j++)
        {
            if (j > i)
            {
                P[i][j] = 0;
            }
            else {
                P[i][j] = P[i - 1][j - 1] * p[i-1] + P[i - 1][j] * (1 - p[i-1]);
            }
        }
    }

    double** Q = new double* [n + 1];
    for (int i = 0; i <= n; i++)
    {
        Q[i] = new double[z + 1];
    }

    Q[0][0] = 1;

    for (int j = 1; j <= z; j++)
    {
        Q[0][j] = 0;
    }

    for (int i = 1; i <= n; i++)
    {
        Q[i][0] = 1;
        for (int a = 1; a <= i; a++) {
            Q[i][0] *= p[a-1];
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= z; j++)
        {
            if (j > i)
            {
                Q[i][j] = 0;
            }
            else {
                Q[i][j] = Q[i - 1][j - 1] * (1-p[i-1]) + Q[i - 1][j] * p[i-1];
            }
        }
    }

    double cost = 0;

    for (int i = 1; i <= n; i++)
    {
        cost += (P[i - 1][k - 1] * p[i-1] + Q[i - 1][z - 1] * (1 - p[i-1])) * double(i);
    }

    for (int i = 0; i < n+1; ++i) {
        delete[] P[i];
        delete[] Q[i];
    }
    delete[] P, Q;



    return cost;
}


#ifdef __cplusplus
extern "C" char get_non_adaptive_cost_arbitrary_cost(int k, int n, double* p, int* c)
#else
double get_non_adaptive_cost_arbitrary_cost(int k, int n, double* p, int* c)
#endif
{

    int z = n - k + 1;

    int* C = new int[n];
    C[0] = c[0];
    for (int i = 1; i< n; i++)
    {
        C[i] = C[i-1]+c[i];
    }

    double** P = new double* [n+1];
    for (int i = 0; i <= n; i++)
    {
        P[i] = new double[k+1];
    }

    P[0][0] = 1;

    for (int j = 1; j <= k; j++)
    {
        P[0][j] = 0;
    }

    for (int i = 1; i <= n; i++)
    {
        P[i][0] = 1;
        for (int a = 1; a <= i; a++) {
            P[i][0] *= (1 - p[a-1]);
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= k; j++)
        {
            if (j > i)
            {
                P[i][j] = 0;
            }
            else {
                P[i][j] = P[i - 1][j - 1] * p[i-1] + P[i - 1][j] * (1 - p[i-1]);
            }
        }
    }

    double** Q = new double* [n + 1];
    for (int i = 0; i <= n; i++)
    {
        Q[i] = new double[z + 1];
    }

    Q[0][0] = 1;

    for (int j = 1; j <= z; j++)
    {
        Q[0][j] = 0;
    }

    for (int i = 1; i <= n; i++)
    {
        Q[i][0] = 1;
        for (int a = 1; a <= i; a++) {
            Q[i][0] *= p[a-1];
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= z; j++)
        {
            if (j > i)
            {
                Q[i][j] = 0;
            }
            else {
                Q[i][j] = Q[i - 1][j - 1] * (1-p[i-1]) + Q[i - 1][j] * p[i-1];
            }
        }
    }

    double cost = 0;

    for (int i = 1; i <= n; i++)
    {
        cost += (P[i - 1][k - 1] * p[i-1] + Q[i - 1][z - 1] * (1 - p[i-1])) * double(C[i-1]);
    }

    for (int i = 0; i < n+1; ++i) {
        delete[] P[i];
        delete[] Q[i];
    }
    delete[] P, Q;



    return cost;
}