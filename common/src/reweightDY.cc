#include "reweightDY.h"
#include <math.h>
#include <algorithm>

double computeDYweight(double a, double b) {
    double weight = 0;
    double mjj_weight = 0;
    double mlljj_weight = 0;
    
    mjj_weight = (1.13022 + (-0.00206761)*a + (7.0697e-06)*pow(a,2) + (-6.26383e-09)*pow(a,3) + (-2.42928e-12)*pow(a,4) + (3.84415e-15)*pow(a,5));
    mlljj_weight = ((b < 1400.) ? (1.3976 + (-0.00503213)*b + (2.31508e-05)*pow(b,2) + (-5.03318e-08)*pow(b,3) + (5.57681e-11)*pow(b,4) + (-3.03564e-14)*pow(b,5) + (6.40372e-18)*pow(b,6)) : 1.);
    weight = mjj_weight*mlljj_weight;

    return weight;
}

double computeMjjweight(double a) {
    double mjj_weight = 0;
    
    mjj_weight = (1.13022 + (-0.00206761)*a + (7.0697e-06)*pow(a,2) + (-6.26383e-09)*pow(a,3) + (-2.42928e-12)*pow(a,4) + (3.84415e-15)*pow(a,5));

    return mjj_weight;
}

double computeMlljjweight(double a) {
    double mlljj_weight = 0;
    
    mlljj_weight = ((a < 1400.) ? (1.3976 + (-0.00503213)*a + (2.31508e-05)*pow(a,2) + (-5.03318e-08)*pow(a,3) + (5.57681e-11)*pow(a,4) + (-3.03564e-14)*pow(a,5) + (6.40372e-18)*pow(a,6)) : 1.);

    return mlljj_weight;
}
