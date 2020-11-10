#ifndef VORONOI_UTILS_H
#define VORONOI_UTILS_H

#include <cstddef>
#include <vector>

struct VoronoiKey {
    ssize_t keyx, keyy;

    bool operator==(const VoronoiKey &other) const
    {
        return keyx == other.keyx && keyy == other.keyy;
    }

    bool operator<(const VoronoiKey &other) const
    {
        return keyx < other.keyx
            || (keyx == other.keyx && keyy < other.keyy);
    }
};

struct Position
{
    Position(double a, double b):
        x(a),
        y(b)
    {
    }

    double x, y;
};

typedef std::vector<Position> VoronoiFace;

#endif

