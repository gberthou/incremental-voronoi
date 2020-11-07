#version 330 core

layout(lines) in;
layout(triangle_strip, max_vertices = 3) out;

uniform vec2 ucentrum;

in mat4 gsMat[];

void main()
{
    gl_Position = gl_in[0].gl_Position;
    EmitVertex();
    gl_Position = gl_in[1].gl_Position;
    EmitVertex();
    gl_Position = gsMat[0] * vec4(ucentrum, 0., 1.);
    EmitVertex();
    EndPrimitive();
}

