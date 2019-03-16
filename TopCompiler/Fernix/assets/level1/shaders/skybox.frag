#version 440 core
out vec4 FragColor;

in vec3 localPos;

uniform samplerCube environmentMap;

void main()
{
    vec3 envColor = texture(environmentMap, localPos).rgb; //texture(environmentMap, localPos).rgb;

    //envColor = envColor / (envColor + vec3(1.0));
    //envColor = pow(envColor, vec3(1.0/2.2));

    vec3 skytop = vec3(67, 175, 242) / 300;
    vec3 skyhorizon = vec3(80, 190, 256) / 260;

    vec3 pointOnSphere = normalize(localPos);
    float a = pointOnSphere.y;
    FragColor = vec4(mix(skyhorizon, skytop, a), 1.0);

    //FragColor = vec4(vec3(67, 175, 242) / 256, 1.0);
}