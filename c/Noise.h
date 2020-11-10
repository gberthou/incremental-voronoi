#ifndef NOISE_H
#define NOISE_H

#include <cstdint>

#include "OpenSimplexNoise.h"

class Noise
{
    public:
        Noise(double zoom, int64_t seed);

        double operator()(double x, double y) const;

    private:
        OpenSimplexNoise simplexNoise;
        double zoom;
};

#endif

