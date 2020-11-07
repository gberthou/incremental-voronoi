#ifndef GLUTILS_H
#define GLUTILS_H

#include <string>
#include <vector>

#include <GL/gl.h>
#include <glm/mat4x4.hpp>

namespace glutils
{
    class Shader
    {
        public:
            Shader(GLenum type, const std::string &filename);
            ~Shader();

            void AttachTo(GLuint programID) const;

        private:
            GLuint shader;
    };

    class Program
    {
        public:
            Program();
            ~Program();

            void EmplaceShader(GLenum type, const std::string &filename);
            void Finalize() const;
            GLuint Get() const;

            virtual void Apply() const = 0;

        protected:
            GLuint program;
            std::vector<Shader> shaders;
    };

    class ProgramWorld : public Program
    {
        public:
            ProgramWorld(const std::string &vertname, const std::string &fragname, const std::string &geoname);
            virtual void Apply() const;
            void BindVAO() const;

            // Assumes: Apply() first
            //void SetModel(const glm::mat4 &model) const;
            // Assumes: Apply() first
            void SetView(const glm::mat4 &view) const;
            // Assumes: Apply() first
            void SetProj(const glm::mat4 &proj) const;
            // Assumes: Apply() first
            void SetColor(const GLfloat *color) const;
            // Assumes: Apply() first
            void SetCentrum(const GLfloat *centrum) const;

        private:
            GLint apos;
            //GLint umodel;
            GLint uview;
            GLint uproj;
            GLint ucolor;
            GLint ucentrum;
    };

    class Texture
    {
    };
}

#endif

