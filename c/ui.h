#ifndef UI_H
#define UI_H

#include <X11/X.h>
#include <X11/Xlib.h>
#include <GL/glx.h>

class UI
{
    public:
        UI(unsigned int width, unsigned int height, const char *title);
        ~UI();

        void Refresh(void);
        void WaitUntilClose(void);
        bool PollEvent(void);

    private:
        Display *display;
        Window window;
        GLXContext glc;
};

#endif

