#include "VoronoiGraph.h"

template<typename T>
VoronoiGraph<T>::VoronoiGraph()
{
}

template<typename T>
bool VoronoiGraph<T>::TryInsertEdge(const VoronoiEdge &edge, const T &data)
{
    VoronoiEdge k = edge.arrange();
    return edges.insert(std::make_pair(k, data)).second;
}

template<typename T>
std::ostream &VoronoiGraph<T>::operator>>(std::ostream &os)
{
    for(const auto &it : edges)
        os << '(' << it.first.a.keyx << ", " << it.first.a.keyy << ") -> (" << it.first.b.keyx << ", " << it.first.b.keyy << "): " << it.second << std::endl;
    return os;
}

template class VoronoiGraph<double>;


