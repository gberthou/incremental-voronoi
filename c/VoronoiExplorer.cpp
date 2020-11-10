#include <Python.h>

#include "VoronoiExplorer.h"
#include "VoronoiGraph.h"

static VoronoiKey keyOfPointItem(PyObject *pointitem)
{
    auto key = PyObject_GetAttrString(pointitem, "key");
    auto _keyx = PyTuple_GetItem(key, 0);
    auto _keyy = PyTuple_GetItem(key, 1);
    ssize_t keyx = PyLong_AsSsize_t(_keyx);
    ssize_t keyy = PyLong_AsSsize_t(_keyy);
    //Py_DECREF(_keyx);
    //Py_DECREF(_keyy);
    Py_DECREF(key);
    return {keyx, keyy};
}

template<typename T, typename F>
VoronoiExplorer<T, F>::VoronoiExplorer(PyObject *voronoiModule, const std::string &filename, size_t density)
{
    auto constructor = PyObject_GetAttrString(voronoiModule, "VoronoiExplorer");

    auto _filename = PyUnicode_FromString(filename.c_str());
    auto _density = PyLong_FromSize_t(density);
    auto args = PyTuple_Pack(2, _filename, _density);
    _self = PyObject_CallObject(constructor, args);
    _loadChunk      = PyObject_GetAttrString(_self, "load_chunk");
    _unloadChunk    = PyObject_GetAttrString(_self, "unload_chunk");
    _keepOnlyChunks = PyObject_GetAttrString(_self, "keep_only_chunks");
    _loadedShapes   = PyObject_GetAttrString(_self, "loaded_shapes");

    auto _pointset  = PyObject_GetAttrString(_self, "pointset");
    _pointsetitems  = PyObject_GetAttrString(_pointset, "point_items");

    Py_DECREF(_pointset);
    Py_DECREF(args);
    Py_DECREF(_filename);
    Py_DECREF(_density);
    Py_DECREF(constructor);
}

template<typename T, typename F>
VoronoiExplorer<T, F>::~VoronoiExplorer()
{
    Py_DECREF(_self);
    Py_DECREF(_loadChunk);
    Py_DECREF(_unloadChunk);
    Py_DECREF(_keepOnlyChunks);
    Py_DECREF(_loadedShapes);

    Py_DECREF(_pointsetitems);
}

template<typename T, typename F>
void VoronoiExplorer<T, F>::LoadChunk(const VoronoiKey &key)
{
    auto keyx = PyLong_FromSsize_t(key.keyx);
    auto keyy = PyLong_FromSsize_t(key.keyy);
    auto tuple = PyTuple_Pack(2, keyx, keyy);
    auto args = PyTuple_Pack(1, tuple);

    PyObject_CallObject(_loadChunk, args);

    Py_DECREF(args);
    Py_DECREF(tuple);
    Py_DECREF(keyx);
    Py_DECREF(keyy);
}

template<typename T, typename F>
void VoronoiExplorer<T, F>::UnloadChunk(const VoronoiKey &key)
{
    auto keyx = PyLong_FromSsize_t(key.keyx);
    auto keyy = PyLong_FromSsize_t(key.keyy);
    auto tuple = PyTuple_Pack(2, keyx, keyy);
    auto args = PyTuple_Pack(1, tuple);

    PyObject_CallObject(_unloadChunk, args);

    Py_DECREF(args);
    Py_DECREF(tuple);
    Py_DECREF(keyx);
    Py_DECREF(keyy);
}

template<typename T, typename F>
void VoronoiExplorer<T, F>::KeepOnlyChunks(const std::vector<VoronoiKey> &keys)
{
    auto keyset = PySet_New(NULL);
    for(const auto &key : keys)
    {
        auto keyx = PyLong_FromSsize_t(key.keyx);
        auto keyy = PyLong_FromSsize_t(key.keyy);
        auto tuple = PyTuple_Pack(2, keyx, keyy);
        PySet_Add(keyset, tuple);

        Py_DECREF(tuple);
        Py_DECREF(keyx);
        Py_DECREF(keyy);
    }
    auto args = PyTuple_Pack(1, keyset);
    
    PyObject_CallObject(_keepOnlyChunks, args);

    Py_DECREF(args);
    Py_DECREF(keyset);
}

template<typename T, typename F>
void VoronoiExplorer<T, F>::LoadedShapes(std::vector<VoronoiFace> &faces)
{
    auto list = PyObject_CallObject(_loadedShapes, NULL);
    Py_ssize_t size = PyList_Size(list);

    faces.clear();
    faces.reserve(size);

    for(Py_ssize_t i = 0; i < size; ++i)
    {
        auto shape = PyList_GetItem(list, i);
        auto vertices = PyObject_GetAttrString(shape, "vertices");
        if(!PyList_Check(vertices))
        {
            Py_DECREF(vertices);
            Py_DECREF(shape);
            continue;
        }
        Py_ssize_t lenVertices = PyList_Size(vertices);

        VoronoiFace face;

        for(Py_ssize_t j = 0; j < lenVertices; ++j)
        {
            auto vertex = PyList_GetItem(vertices, j);
            auto _x = PyTuple_GetItem(vertex, 0);
            auto _y = PyTuple_GetItem(vertex, 1);
            double x = PyFloat_AsDouble(_x);
            double y = PyFloat_AsDouble(_y);

            face.emplace_back(x, y);

            Py_DECREF(_x);
            Py_DECREF(_y);
            Py_DECREF(vertex);
        }
        Py_DECREF(vertices);
        Py_DECREF(shape);

        faces.push_back(face);
    }
}

template<typename T, typename F>
void VoronoiExplorer<T, F>::GetGraph(VoronoiGraph<T> &graph, const F &noiseFunction)
{
    auto it = PyObject_GetIter(_pointsetitems);
    PyObject *pointitem;

    while((pointitem = PyIter_Next(it)))
    {
        auto key = keyOfPointItem(pointitem);

        auto others = PyObject_GetAttrString(pointitem, "others");
        auto itothers = PyObject_GetIter(others);
        Py_DECREF(others);

        PyObject *other;

        while((other = PyIter_Next(itothers)))
        {
            auto otheritem = PyObject_GetAttrString(other, "item");
            Py_DECREF(other);
            auto otherkey = keyOfPointItem(otheritem);
            Py_DECREF(otheritem);

            VoronoiEdge edge(key, otherkey);
            graph.TryInsertEdge(edge, noiseFunction((key.keyx + otherkey.keyx) / 2., (key.keyy + otherkey.keyy) / 2.));
        }

        Py_DECREF(itothers);
        Py_DECREF(pointitem);
    }

    Py_DECREF(it);
}

template<typename T, typename F>
size_t VoronoiExplorer<T, F>::GetSeed()
{
    auto chunkDatabase = PyObject_GetAttrString(_self, "chunk_database");
    auto _seed = PyObject_GetAttrString(chunkDatabase, "seed");
    size_t ret = PyLong_AsSize_t(_seed);
    Py_DECREF(_seed);
    Py_DECREF(chunkDatabase);

    return ret;
}

#include "VoronoiExplorerImplementation.h"

