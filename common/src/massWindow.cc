#include "massWindow.h"
#include <iostream>
#include <json/json.h>
#include <math.h>
#include <TRandom.h>


// The purpose of this class is to see if a specific point falls inside an
// ellipse or not.
// This is done by converting ellipses to circles. I.e., given
// (x, y) point on the ellipse, get
// (x', y') point on the circle.
// |x'|     |M11  M12|   |x|      x' = M11*x + M12*y
// |  |  =  |        | * | | --> 
// |y'|     |M21  M22|   |y|      y' = M21*x + M22*y
// - Default constructor massWindow(...):    initializes the variables.
// - radius(...):                            computes rho.
// Next three functions: not used anymore
// - getValue(...):                          returns the interpolated value of the transformation matrix in a given point.
// - applyGlobalTransformation(...):         returns the coordinates (x', y').
// - isInEllipse(...):                       returns true if a point is inside the circle (false if outside).


massWindow::massWindow(double xc, double yc, double p00, double p01, double p10, double p11) : m_xc(xc), m_yc(yc), m_p00(p00), m_p01(p01), m_p10(p10), m_p11(p11)
{}

int massWindow::getNumberOfEllipses(std::string filename) {

    int n_ellipse = 0;
    std::ifstream ifile(filename);
    Json::Reader reader;
    Json::Value text;
    if (!ifile) std::cout << "ERROR OPENING FILE" << std::endl;
    if (ifile && reader.parse(ifile, text)) {
        n_ellipse = text.size();
    }
    std::cout << "n_ellipse: " << n_ellipse << std::endl;
    return n_ellipse;
}



double massWindow::radius(double px, double py)
{
    const double dx = px - m_xc;
    const double dy = py - m_yc;
    const double p1 = m_p00*dx + m_p01*dy;
    const double p2 = m_p10*dx + m_p11*dy;
    const double dist = std::sqrt(p1*p1 + p2*p2);
    return ( dist > 3 ? 3.2 : dist ); //This is for the overflow bin. Set a value that falls into the last bin (between 3 and 3.5)
}


/*
Old code, left for reference but not used
//Returns the [n,m] component of the gauge matrix at point (mA,mH)
double massWindow::getValue (int n, int m, pair_d point){
    //std::cout << "Entering getValue()" << std::endl;

    double interpolation = m_matrix[n][m].Interpolate(point.first, point.second);
    //std::cout << "interpolation: " << interpolation << std::endl;

    double a_closestEllipse = 0;
    double b_closestEllipse = 0;
    double theta_closestEllipse = 0;
    double dist = 0;
    if (interpolation == 0) {
        dist = 1000000000;
        std::ifstream ifile(m_filename);
        Json::Reader reader;
        Json::Value text;
        if (ifile && reader.parse(ifile, text)) {
            for (int i=0; i<text.size(); i++) {
                const double mbb = text[i][0].asDouble();
                const double mllbb = text[i][1].asDouble();
                const double a = text[i][2].asDouble();
                const double b = text[i][3].asDouble();
                const double theta = text[i][4].asDouble();
                const double MA = text[i][5].asDouble();
                const double MH = text[i][6].asDouble();
                std::cout << "a: " << a << std::endl;
                if (MA > 0 && MH > 0 && theta > 0 && a > 0 && b > 0) {
                    double distance = sqrt(pow(point.first-mbb, 2)+pow(point.second-mllbb, 2));
                    std::cout << "distance: " << distance << std::endl;
                    if (distance < dist){
                        dist = distance;
                        a_closestEllipse = a;
                        b_closestEllipse = b;
                        theta_closestEllipse = theta;
                    }
                }
                // If no min dist found:
                if (dist == 1000000000) interpolation = 0.;
                else {
                    if (n==0 && m==0) interpolation = cos(theta_closestEllipse)/sqrt(a_closestEllipse);
                    else if (n==0 && m==1) interpolation = sin(theta_closestEllipse)/sqrt(a_closestEllipse);
                    else if (n==1 && m==0) interpolation = -sin(theta_closestEllipse)/sqrt(b_closestEllipse);
                    else if (n==1 && m==1) interpolation = cos(theta_closestEllipse)/sqrt(b_closestEllipse);
                }
            }
        }
    }
    std::cout << "interpolation: " << interpolation << std::endl;
    return interpolation;
    std::cout << "Exiting getValue()" << std::endl;
}


pair_d massWindow::applyGlobalTransformation(pair_d ref, pair_d point) {

    std::cout << "Entered applyGlobalTransformation" << std::endl;

    double m1 = this->getValue(0,0,ref)*point.first + this->getValue(0,1,ref)*point.second;
    std::cout << "m1: " << m1 << std::endl;
    double m2 = this->getValue(1,0,ref)*point.first + this->getValue(1,1,ref)*point.second;
    std::cout << "m2: " << m2 << std::endl;
    return std::make_pair(m1, m2);
    std::cout << "Exiting applyGlobalTransformation" << std::endl;
}


pair_d massWindow::applyLocalTranformation(pair_d point) {

    return this->applyGlobalTransformation(point,point);   
}


bool massWindow::isInEllipse(double center_x, double center_y, double size, double point_x, double point_y){
    
    double m1diff = point_x - center_x;
    double m2diff = point_y - center_y;
    pair_d mdiff = std::make_pair(m1diff, m2diff);
    pair_d center = std::make_pair(center_x, center_y);
    pair_d param = this->applyGlobalTransformation(center, mdiff);
    return sqrt(pow(param.first,2) + pow(param.second,2)) <= size;
}


double massWindow::isInEllipse_noSize(double center_x, double center_y, double point_x, double point_y){
    std::cout << "Entering isInEllipse_noSize" << std::endl;
    std::cout << "center_x: " << center_x << std::endl;
    std::cout << "center_y: " << center_y << std::endl;
    std::cout << "point_x: " << point_x << std::endl;
    std::cout << "point_y: " << point_y << std::endl;
    
    double m1diff = point_x - center_x;
    std::cout << "m1diff: " << m1diff << std::endl;
    double m2diff = point_y - center_y;
    std::cout << "m2diff: " << m2diff << std::endl;
    pair_d mdiff = std::make_pair(m1diff, m2diff);
    pair_d center = std::make_pair(center_x, center_y);
    pair_d param = this->applyGlobalTransformation(center, mdiff);
    double dist = sqrt(pow(param.first,2) + pow(param.second,2));
    if (dist > 3.)
        dist = 3.2; //This is for the overflow bin. Set a value that falls into the last bin (between 3 and 3.5)
    std::cout << "dist: " << dist << std::endl;
    return dist;
}
*/
