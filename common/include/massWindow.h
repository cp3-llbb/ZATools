#pragma once

#include <string>
#include <vector>
#include <memory>
#include <map>
#include <cassert>
#include <TGraph2D.h>

#include "math.h"
#include <utility>
#include <fstream>


typedef std::pair<double, double> pair_d;
class massWindow {

    public:
        //massWindow(std::string filename);
        massWindow(double xc, double yc, double p00, double p01, double p10, double p11);
        int getNumberOfEllipses(std::string filename);
        double radius(double px, double py);
        double getValue (int n, int m, pair_d point);
        pair_d applyGlobalTransformation(pair_d ref, pair_d point);
        pair_d applyLocalTranformation(pair_d point);
        bool isInEllipse(double center_x, double center_y, double size, double point_x, double point_y);
        double isInEllipse_noSize(double center_x, double center_y, double point_x, double point_y);

    private:
        std::string m_filename;
        std::vector<std::vector<TGraph2D>> m_matrix;
        double m_xc, m_yc; //center of the ellipse
        double m_p00, m_p01, m_p10, m_p11;
};
