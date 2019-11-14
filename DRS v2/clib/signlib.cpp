// reduce the message using the secret key, and then stores information in the signature structure
#include <stdio.h>
#include <string.h>
#include <random>
#include <iostream>

using namespace std;    

#define M (1 << 28)
#define n nnn
#define D nnn
typedef long double FT;

#define feature_count 7

extern "C"
{

    void reductionS_D(long *m, long *sk) 
    {
        unsigned int i = 0, k = 0, j = 0;
        long q;
    	// reduce the message with the reduction matrix
        do {
            q = m[i]/((long)sk[i* n + i]);
            if(q) {
                for(j = 0; j < n; j ++) {
                	m[j] -= q*((long)sk[i* n + j]);
                }
              k = 0;
            }
          k++;
          i = (i + 1) % n;
      	} while(k != n);
  	}


    FT feature[n][n][feature_count];
    long m[n];
    long samples = 0;

    inline FT f0(FT x, FT y)
    {
        return x * y;
    }

   inline FT f1(FT x, FT y)
    {
        return x * sqrt(abs(x)) * y;
    }

   inline FT f2(FT x, FT y)
    {
        return x * abs(x) * y;
    }


   inline FT f3(FT x, FT y)
    {
        return x * (x+1) * (x-1) * y;
    }


   inline FT f4(FT x, FT y)
    {
        FT xx = x*2;
        return (abs(xx) < 1) * xx * (xx+1) * (xx-1) * y;
    }

   inline FT f5(FT x, FT y)
    {
        FT xx = x*4;
        return (abs(xx) < 1) * xx * (xx+1) * (xx-1) * y;
    }

   inline FT f6(FT x, FT y)
    {
        FT xx = x*8;
        return (abs(xx) < 1) * xx * (xx+1) * (xx-1) * y;
    }


    void init_stats()
    {
        for (int d = 0; d < feature_count; ++d)
        {
            for (int i = 0; i < n; ++i)
            {
                for (int j = 0; j < n; ++j)
                {
                    feature[i][j][d] = 0;
                }
            }
        }
        samples = 0;
    }

    void sample(long* sk)
    {
        samples += 1;
        for (int i = 0; i < n; ++i)
        {
            m[i] = (rand() % (2 * M - 1)) - M + 1; // (-(M-1), M-1)
        }
        reductionS_D(m, sk);

        for (int i = 0; i < n; ++i)
        {
            for (int j = 0; j < n; ++j)
            {
                FT x = ((FT) m[i]) / D;
                FT y = ((FT) m[j]) / D;
				feature[i][j][0] += f0(x, y);
				feature[i][j][1] += f1(x, y);
                feature[i][j][2] += f2(x, y);
                feature[i][j][3] += f3(x, y);
                feature[i][j][4] += f4(x, y);
                feature[i][j][5] += f5(x, y);
                feature[i][j][6] += f6(x, y);
            }
        }
    }

    void sample_many(long* sk, long count)
    {
        long p = 1;
        for (long i = 0; i < count; ++i)
        {
            sample(sk);
            if (i == p)
            {
                cerr << i << " / " << count << " ";
                p *= 2;
            }
        }
        cerr << endl;
    }


    void export_feature_matrix(double* mat, int d)
    {
        FT f = D * 1./samples; // Renormalization factor (essentially for pretty printing)

        for (int i = 0; i < n; ++i)
        {
            for (int j = 0; j < n; ++j)
            {       
                mat[i*n + j] = feature[i][j][d] * f;
            }
        }
    }
}
