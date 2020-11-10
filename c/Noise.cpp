#include "Noise.h"

Noise::Noise(double zoom, int64_t seed):
    simplexNoise(seed),
    zoom(zoom)
{
}

double Noise::operator()(double x, double y) const
{
    return simplexNoise.Evaluate(x * zoom, y * zoom);
}

