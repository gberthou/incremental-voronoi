#ifndef VORONOI_UTILS_H
#define VORONOI_UTILS_H

#include <cstddef>
#include <vector>

struct VoronoiChunkKey
{
    ssize_t keyx, keyy;

    bool operator==(const VoronoiChunkKey &other) const
    {
        return keyx == other.keyx && keyy == other.keyy;
    }

    bool operator<(const VoronoiChunkKey &other) const
    {
        return keyx < other.keyx
            || (keyx == other.keyx && keyy < other.keyy);
    }
};

struct VoronoiNodeKey
{
    VoronoiChunkKey chunkkey;
    size_t id;

    bool operator==(const VoronoiNodeKey &other) const
    {
        return chunkkey == other.chunkkey && id == other.id;
    }

    bool operator<(const VoronoiNodeKey &other) const
    {
        return chunkkey < other.chunkkey
            || (chunkkey == other.chunkkey && id < other.id);
    }
};

struct VoronoiPosition
{
    VoronoiPosition(double a, double b):
        x(a),
        y(b)
    {
    }

    double x, y;
};

typedef std::vector<VoronoiPosition> VoronoiFace;

#endif

