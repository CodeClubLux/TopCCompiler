#version 440 core

out int FragColor;
uniform int id;

void main() {
    //FragColor = vec4(1,0,0,1);
    FragColor = id + 1;
}