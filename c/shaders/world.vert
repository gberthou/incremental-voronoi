#version 130
attribute vec2 apos;

/*uniform mat4 umodel;*/
uniform mat4 uview;
uniform mat4 uproj;

out mat4 gsMat;

void main()
{
    gsMat = uproj * uview;

    vec4 pos = /*umodel * */ vec4(apos.xy, 0.0, 1.0);
    gl_Position = gsMat * pos;
}
