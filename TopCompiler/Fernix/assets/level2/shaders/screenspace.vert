layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aBitangent;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 viewPos;

out vec2 TexCoords;
out vec3 NDC;

void main()
{
    gl_Position = model * vec4(aPos, 1.0);
    TexCoords = aTexCoords;

    NDC = (gl_Position / gl_Position.w).xyz;
}