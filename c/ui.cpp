#include <iostream>
#include <cstdlib>
#include <GL/gl.h>

#include "ui.h"

UI::UI(unsigned int width, unsigned int height, const char *title)
{
    display = XOpenDisplay(NULL);
    if(display == NULL)
    {
        std::cerr << "XOpenDisplay" << std::endl;
        exit(EXIT_FAILURE);
    }
        
    Window root = DefaultRootWindow(display);

    int attributes[] = {GLX_RGBA, GLX_DEPTH_SIZE, 24, GLX_DOUBLEBUFFER, None};
    XVisualInfo *visualInfo = glXChooseVisual(display, 0, attributes);
    if(visualInfo == NULL)
    {
        std::cerr << "glXChooseVisual" << std::endl;
        exit(EXIT_FAILURE);
    }

    Colormap cmap = XCreateColormap(display, root, visualInfo->visual, AllocNone);
    XSetWindowAttributes swa;
    swa.colormap = cmap;
    swa.event_mask = ExposureMask | KeyPressMask;
 
    window = XCreateWindow(display, root, 0, 0, width, height, 0, visualInfo->depth, InputOutput, visualInfo->visual, CWColormap | CWEventMask, &swa);

    XSelectInput(display, window, ExposureMask);

    XMapWindow(display, window);
    XFlush(display);
    XStoreName(display, window, title);
 
    glc = glXCreateContext(display, visualInfo, NULL, GL_TRUE);
    glXMakeCurrent(display, window, glc);
}

UI::~UI()
{
    glXMakeCurrent(display, None, NULL);
    glXDestroyContext(display, glc);
    XDestroyWindow(display, window);
    XCloseDisplay(display);
}

void UI::Refresh(void)
{
    glXSwapBuffers(display, window);
}

void UI::WaitUntilClose(void)
{
    for(;;)
        if(!PollEvent())
            break;
}

bool UI::PollEvent(void)
{
    if(XPending(display))
    {
        XEvent event;
        XNextEvent(display, &event);
        return event.type != DestroyNotify;
    }
    return true;
}

