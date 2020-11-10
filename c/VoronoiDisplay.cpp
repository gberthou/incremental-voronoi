#include "gl.h"
#include "VoronoiDisplay.h"

template<typename F>
VoronoiDisplay<F>::VoronoiDisplay(
    const F &noiseFunction,
    const std::vector<VoronoiFace> &voronoiFaces
)
{
    size_t vertexIndex = 0;

    for(const auto &voronoiFace : voronoiFaces)
    {
        if(voronoiFace.size() < 4)
            continue;

        DisplayFace face(voronoiFace.size() + 1);
        size_t i = 0;
        size_t offset = vertexIndex;
        for(const auto &pos : voronoiFace)
        {
            vertexData.push_back(pos.x);
            vertexData.push_back(pos.y);

            face.centrum[0] += pos.x;
            face.centrum[1] += pos.y;

            face.indices[i++] = vertexIndex++;
        }
        face.centrum[0] /= voronoiFace.size();
        face.centrum[1] /= voronoiFace.size();

        face.indices[i] = offset;

        float intensity = noiseFunction(face.centrum[0], face.centrum[1]);

        face.color = {intensity, intensity, intensity};
        faces.push_back(face);
    }

    glGenBuffers(1, &vertexBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
    glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(float), vertexData.data(), GL_STATIC_DRAW);
}

template<typename F>
VoronoiDisplay<F>::~VoronoiDisplay()
{
    glDeleteBuffers(1, &vertexBuffer);
}

template<typename F>
void VoronoiDisplay<F>::Draw(const glutils::ProgramWorld &program) const
{
    program.Apply();
    program.BindVAO();

    for(const auto &face : faces)
    {
        const auto &indices = face.indices;
        program.SetCentrum(face.centrum.data());
        program.SetColor(face.color.data());
        glDrawElementsBaseVertex(GL_LINE_STRIP, indices.size(), GL_UNSIGNED_INT, indices.data(), 0);
    }
}

/*
void VoronoiDisplay::centrumOf(const std::vector<GLuint> &faceIndices, std::array<float, 2> &centrum) const
{
    size_t offsetffset = 2 * faceIndices[0];
    centrum[0] = vertexData[offset    ];
    centrum[1] = vertexData[offset + 1];

    for(size_t i = 1; i+1 < faceIndices.size(); ++i)
    {
        offset = 2 * faceIndices[i];
        centrum[0] += vertexData[offset    ];
        centrum[1] += vertexData[offset + 1];
    }
    centrum[0] /= faceIndices.size() - 1;
    centrum[1] /= faceIndices.size() - 1;
}
*/

#include "VoronoiDisplayImplementation.h"

