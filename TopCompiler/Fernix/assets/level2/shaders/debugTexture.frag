out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D tex;

void main() {
    FragColor = vec4(texture(tex, TexCoords).xyz, 1);
}