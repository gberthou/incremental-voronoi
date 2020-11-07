#include <vector>
#include <array>
#include <GL/gl.h>

#include "VoronoiExplorer.h"
#include "glutils.h"

class VoronoiDisplay
{
    public:
        VoronoiDisplay(
            VoronoiExplorer &explorer,
            const std::vector<VoronoiFace> &voronoiFaces
        );
        ~VoronoiDisplay();

        void Draw(const glutils::ProgramWorld &program) const;

    private:
        struct DisplayFace
        {
            DisplayFace(size_t nindices):
                indices(nindices),
                centrum{0, 0},
                color{1, 1, 1}
            {
            }

            DisplayFace(const DisplayFace &other):
                indices(other.indices),
                centrum(other.centrum),
                color(other.color)
            {
            }

            std::vector<GLuint> indices;
            std::array<float, 2> centrum;
            std::array<float, 3> color;
        };

        //void centrumOf(const std::vector<GLuint> &faceIndices, std::array<float, 2> &centrum) const;

        std::vector<float> vertexData;
        std::vector<DisplayFace> faces;
        GLuint vertexBuffer;
};

