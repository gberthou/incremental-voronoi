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
        os << '('
           << it.first.a.chunkkey.keyx << ", " << it.first.a.chunkkey.keyy << ", " << it.first.a.id
           << ") -> ("
           << it.first.b.chunkkey.keyx << ", " << it.first.b.chunkkey.keyy << ", " << it.first.b.id
           << "): " << it.second << std::endl;
    return os;
}

template class VoronoiGraph<double>;


