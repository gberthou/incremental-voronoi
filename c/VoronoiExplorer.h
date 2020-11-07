#ifndef VORONOI_EXPLORER_H
#define VORONOI_EXPLORER_H

#include <vector>
#include <string>

#include <Python.h>

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

class VoronoiExplorer
{
    public:
        VoronoiExplorer(PyObject *voronoiModule, const std::string &filename, size_t density);
        ~VoronoiExplorer();

        struct Key {
            ssize_t keyx, keyy;
        };

        void LoadChunk(const Key &key);
        void UnloadChunk(const Key &key);
        void KeepOnlyChunks(const std::vector<Key> &keys);
        void LoadedShapes(std::vector<VoronoiFace> &faces);

        double GetNoiseAt(double x, double y);

    private:
        PyObject *_self;
        PyObject *_loadChunk;
        PyObject *_unloadChunk;
        PyObject *_keepOnlyChunks;
        PyObject *_loadedShapes;
        PyObject *_noise;
        PyObject *_noiseGet;
};

#endif

