#ifndef VORONOI_GRAPH_H
#define VORONOI_GRAPH_H

#include <iostream>
#include <map>

#include "VoronoiUtils.h"

struct VoronoiEdge
{
    VoronoiNodeKey a, b;

    VoronoiEdge(const VoronoiNodeKey &x, const VoronoiNodeKey &y):
        a(x),
        b(y)
    {
    }

    VoronoiEdge invert() const
    {
        return {b, a};
    }

    VoronoiEdge arrange() const
    {
        VoronoiEdge other = invert();
        return *this < other ? *this : other;
    }

    bool operator<(const VoronoiEdge &other) const
    {
        return a < other.a
            || (a == other.a && b < other.b);
    }
};

template<typename T>
class VoronoiGraph
{
    public:
        VoronoiGraph();
        
        bool TryInsertEdge(const VoronoiEdge &edge, const T &data);

        std::ostream &operator>>(std::ostream &os);

    private:
        std::map<VoronoiEdge, T> edges;
};

#endif

