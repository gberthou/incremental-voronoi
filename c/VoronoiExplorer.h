#ifndef VORONOI_EXPLORER_H
#define VORONOI_EXPLORER_H

#include <vector>
#include <string>

#include <Python.h>

#include "VoronoiUtils.h"
#include "VoronoiGraph.h"

template<typename T, typename F>
class VoronoiExplorer
{
    public:
        VoronoiExplorer(PyObject *voronoiModule, const std::string &filename, size_t density);
        ~VoronoiExplorer();

        void LoadChunk(const VoronoiKey &key);
        void UnloadChunk(const VoronoiKey &key);
        void KeepOnlyChunks(const std::vector<VoronoiKey> &keys);
        void LoadedShapes(std::vector<VoronoiFace> &faces);

        void GetGraph(VoronoiGraph<T> &graph, const F &noiseFunction);

        size_t GetSeed();

    private:
        PyObject *_self;
        PyObject *_loadChunk;
        PyObject *_unloadChunk;
        PyObject *_keepOnlyChunks;
        PyObject *_loadedShapes;

        PyObject *_pointsetitems;
};

#endif

