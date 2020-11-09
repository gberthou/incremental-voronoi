#include <iostream>
#include <array>
#include <Python.h>
#include <glm/gtc/matrix_transform.hpp>

#include "gl.h"
#include "VoronoiExplorer.h"
#include "VoronoiGraph.h"
#include "VoronoiDisplay.h"
#include "ui.h"
#include "glutils.h"

static auto initPython()
{
    Py_Initialize();
    PyImport_ImportModule("math");
    PyImport_ImportModule("random");
    PyImport_ImportModule("struct");
    PyImport_ImportModule("opensimplex");

    PySys_SetPath(L"..");
    return PyImport_ImportModule("voronoi");
}

static void initGL(unsigned int width, unsigned int height)
{
    glViewport(0, 0, width, height);
    //glEnable(GL_DEPTH_TEST); 

    //glDepthFunc(GL_LEQUAL);
    glClearColor(1, 0, 1, 1);
}
 
int main(void)
{
    auto voronoiModule = initPython();

    VoronoiExplorer *voronoiExplorer = new VoronoiExplorer(voronoiModule, "world1", 4);
    Py_DECREF(voronoiModule);

    const unsigned int width = 800;
    const unsigned int height = 600;

    UI ui(width, height, "Test");

    initGL(width, height);
    glutils::ProgramWorld program("shaders/world.vert", "shaders/world.frag", "shaders/world.gs");
    glm::mat4 proj = glm::perspective(100.f, static_cast<float>(width)/height, .1f, 10.f);
    program.Apply();
    program.SetProj(proj);

    glm::vec3 eye(2, 2, 4);

    for(ssize_t y = 0; y < 4; ++y)
        for(ssize_t x = 0; x < 4; ++x)
            voronoiExplorer->LoadChunk({x, y});

    std::vector<VoronoiFace> faces;
    voronoiExplorer->LoadedShapes(faces);

    VGFloat graph;
    voronoiExplorer->GetGraph(graph);
    graph >> std::cout;

    VoronoiDisplay *display = new VoronoiDisplay(*voronoiExplorer, faces);

    while(ui.PollEvent())
    {
        glm::mat4 view = glm::lookAt(
            eye, 
            glm::vec3(eye.x+1e-6, eye.y, 0),
            glm::vec3(0, 0, 1)
        );

        program.Apply();
        program.SetView(view);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        display->Draw(program);
        ui.Refresh();
    }

    delete voronoiExplorer;
    
    return EXIT_SUCCESS;
}

