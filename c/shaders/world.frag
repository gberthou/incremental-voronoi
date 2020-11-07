#version 130

uniform vec3 ucolor;

void main()
{
    gl_FragColor = vec4(ucolor.xyz, 1.);
}
