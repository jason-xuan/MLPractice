using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Regression
{
    class LinearRegression
    {
        /// <summary>
        /// feature data, it's a m*n array like:
        /// X0        X1        X2       X3
        /// 1.0       1.0       2.0      1.2
        /// 1.0       2.0       1.0      1.2
        /// 1.0       3.0       0.0     -0.8
        /// 1.0       4.0       1.0      1.0
        /// 1.0       5.0      -1.0      0.9
        /// 1.0       6.0       0.0      1.0
        /// 1.0       7.0      -2.0      1.0
        /// </summary>
        private List<List<double>> X;

        /// <summary>
        /// number of examples
        /// </summary>
        private int m;

        /// <summary>
        /// number of features + 1
        /// </summary>
        private int n;

        /// <summary>
        /// number to predit, it's length is m.
        /// </summary>
        private List<double> y;

        /// <summary>
        /// the learning parameter theta, it's length is n.
        /// </summary>
        private List<double> theta;

        /// <summary>
        /// learning rate for grade decent
        /// </summary>
        private double alpha = 0.001;

        /// <summary>
        /// number of iterations
        /// </summary>
        private double iterations = 10000;

        /// <summary>
        /// random number generator
        /// </summary>
        private Random random = new Random();

        public LinearRegression(double alpha=0.001,double iterations=10000)
        {
            this.alpha = alpha;
            this.iterations = iterations;
        }

        /// <summary>
        /// apply a hypothesis to one row of data with current theta.
        /// </summary>
        /// <param name="x">
        /// an example's data, it's length is n
        /// </param>
        /// <returns></returns>
        private double Hypothesis(List<double> x)
        {
            double result = 0;
            for (int i = 0; i < n; i++)
            {
                result += x[i] * theta[i];
            }
            //Console.WriteLine("Hypothesis of X: {0}", result);
            return result;
        }

        /// <summary>
        /// calculate the loss value with current theta.
        /// </summary>
        /// <returns></returns>
        private double Cost()
        {
            //Console.WriteLine("begin calculating cost");

            double cost = 0;

            for (int i = 0; i < m; i++)
            {
                cost += Math.Pow(Hypothesis(X[i]) - y[i], 2);
            }

            cost = cost / (2 * m);

            //Console.WriteLine("end calculating cost");

            return cost;
        }

        /// <summary>
        /// initialize all values for calculate
        /// </summary>
        /// <param name="X"></param>
        /// <param name="y"></param>
        private void Init(List<List<double>> X, List<double> y)
        {
            this.X = X;
            this.y = y;

            m = X.Count;
            n = X[0].Count;

            // check if matrix
            foreach (var example in X)
            {
                if (example.Count != n)
                {
                    throw new Exception("X is not a matrix.");
                }
            }

            theta = new List<double>(n);

            // initialize theta with random values.
            for (int i = 0; i < n; i++)
            {
                theta.Add(random.NextDouble());
                //theta.Add(0);
            }

            Normalize();
        }

        /// <summary>
        /// normalize feature matrix with z-scope algorithm.
        /// </summary>
        private void Normalize()
        {
            // iter all features with z-scope
            for (int j = 1; j < n; j++)
            {
                // calculate mean
                double mean = 0;
                for (int i = 0; i < m; i++)
                {
                    mean += X[i][j];
                }
                mean = mean / m;

                // calculate delta
                double delta = 0;
                for (int i = 0; i < m; i++)
                {
                    delta += Math.Pow(X[i][j]-mean,2);
                }
                delta = delta / m;

                // normalize
                for (int i = 0; i < m; i++)
                {
                    X[i][j] = (X[i][j] - mean) / delta;
                }
            }

            Console.WriteLine("Normalized: ");

            for (int i = 0; i < m; i++)
            {
                Console.WriteLine("{0}, {1}, {2}, {3}", X[i][0], X[i][1], X[i][2], X[i][3]);
            }

        }

        /// <summary>
        /// apply the LinearRegression to X and y with grade decent.
        /// notice: parameters must be initialized!!!
        /// </summary>
        /// <returns></returns>
        public List<double> GradeDecent(List<List<double>> X, List<double> y)
        {
            // initialize
            Init(X, y);

            // main iteration of grade decent
            for (int k = 0; k < iterations; k++)
            {
                // update theta[j]

                //Console.WriteLine("theta: {0}, {1}, {2}, {3}", theta[0], theta[1], theta[2], theta[3]);

                for (int j = 0; j < n; j++)
                {
                    double sigma = 0;

                    for (int i = 0; i < m; i++)
                    {
                        sigma += (Hypothesis(X[i]) - y[i]) * X[i][j];
                    }

                    theta[j] -= alpha * sigma / m;
                }
                if (k % 100 == 0) 
                {
                    Console.WriteLine("Iteration {0}, loss: {1}", k, Cost());
                }
                
            }
            return theta;
        }

        /// <summary>
        /// a simple method to test the algorithm with ternary linear regression.
        /// </summary>
        static void Test()
        {
            List<List<double>> X = new List<List<double>>(){
       new List<double>(){1,        0,         0,         0},
       new List<double>(){1,        13,       169,      2197},
       new List<double>(){1,        34,      1156,     39304},
       new List<double>(){1,        47,      2209,    103823},
       new List<double>(){1,        67,      4489,    300763},
       new List<double>(){1,        97,      9409,    912673},
       new List<double>(){1,       122,     14884,   1815848},
       new List<double>(){1,       150,     22500,   3375000},
       new List<double>(){1,       164,     26896,   4410944},
       new List<double>(){1,       229,     52441,  12008989},
       new List<double>(){1,       291,     84681,  24642171},
       new List<double>(){1,       351,    123201,  43243551},
       new List<double>(){1,       364,    132496,  48228544},
       new List<double>(){1,       422,    178084,  75151448},
       new List<double>(){1,       493,    243049, 119823157}};

            List<double> y = new List<double> { 54, 75, 97, 108, 120, 136, 145, 161, 164, 185, 211, 243, 271, 296, 320 };

            // init

            //for (int i = 0; i < x.Count; i++)
            //{
            //    var example = new List<double> { 1, x[i], Math.Pow(x[i], 2), Math.Pow(x[i], 3) };
            //    X.Add(example);
            //}

            // call function


            var liner = new LinearRegression(1, 100000);
            var theta = liner.GradeDecent(X, y);

            // write result
            for (int i = 0; i < theta.Count; i++)
            {
                Console.Write("{0}, ", theta[i]);
            }
            Console.WriteLine();
        }


        static void Main(string[] args)
        {
            Test();
        }
    }
}
