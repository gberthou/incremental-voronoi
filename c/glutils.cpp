#include <iostream>
#include <fstream>
#include <sstream>

#include <glm/gtc/type_ptr.hpp>
#include "gl.h"

#include "glutils.h"

static std::string readFile(const std::string &filename)
{
    std::ifstream f(filename.c_str());
    std::stringstream s;
    s << f.rdbuf();
    return s.str();
}

namespace glutils
{
    Shader::Shader(GLenum type, const std::string &filename):
        shader(glCreateShader(type))
    {
        if(shader == 0) // Error
        {
            // TODO
        }

        std::string content = readFile(filename);
        const GLchar *stringArray[1] = {content.c_str()};
        glShaderSource(shader, 1, stringArray, NULL);
        glCompileShader(shader);

        GLint success = 0;
        glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
        if(success == GL_FALSE)
        {
            GLsizei maxlength = 0;
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &maxlength);

            std::string s(maxlength, 0);
            glGetShaderInfoLog(shader, maxlength, &maxlength, s.data());
            std::cerr << "Error while compiling '" << filename << "'"
                      << std::endl << s << std::endl;
        }
    }

    Shader::~Shader()
    {
        glDeleteShader(shader);
    }

    void Shader::AttachTo(GLuint programID) const
    {
        glAttachShader(programID, shader);
    }


    Program::Program():
        program(glCreateProgram())
    {
    }

    Program::~Program()
    {
        glDeleteProgram(program);
    }

    void Program::EmplaceShader(GLenum type, const std::string &filename)
    {
        shaders.emplace_back(type, filename).AttachTo(program);
    }

    void Program::Finalize() const
    {
        glLinkProgram(program);
        glValidateProgram(program);
    }

    GLuint Program::Get() const
    {
        return program;
    }

    ProgramWorld::ProgramWorld(const std::string &vertname, const std::string &fragname, const std::string &geoname)
    {
        EmplaceShader(GL_VERTEX_SHADER, vertname);
        EmplaceShader(GL_FRAGMENT_SHADER, fragname);
        EmplaceShader(GL_GEOMETRY_SHADER, geoname);
        Finalize();

        apos      = glGetAttribLocation(program, "apos");
        //umodel    = glGetUniformLocation(program, "umodel");
        uview     = glGetUniformLocation(program, "uview");
        uproj     = glGetUniformLocation(program, "uproj");
        ucolor    = glGetUniformLocation(program, "ucolor");
        ucentrum  = glGetUniformLocation(program, "ucentrum");
        
        glEnableVertexAttribArray(apos);
    }

    void ProgramWorld::Apply() const
    {
        glUseProgram(program);
    }

    void ProgramWorld::BindVAO() const
    {
        glVertexAttribPointer(apos, 2, GL_FLOAT, GL_FALSE, 2*sizeof(GLfloat), 0);
    }

    /*
    void ProgramWorld::SetModel(const glm::mat4 &model) const
    {
        glUniformMatrix4fv(umodel, 1, GL_FALSE, glm::value_ptr(model));
    }
    */

    void ProgramWorld::SetView(const glm::mat4 &view) const
    {
        glUniformMatrix4fv(uview, 1, GL_FALSE, glm::value_ptr(view));
    }

    void ProgramWorld::SetProj(const glm::mat4 &proj) const
    {
        glUniformMatrix4fv(uproj, 1, GL_FALSE, glm::value_ptr(proj));
    }

    void ProgramWorld::SetColor(const GLfloat *color) const
    {
        glUniform3fv(ucolor, 1, color);
    }

    void ProgramWorld::SetCentrum(const GLfloat *centrum) const
    {
        glUniform2fv(ucentrum, 1, centrum);
    }
}

