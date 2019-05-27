out vec4 FragColor;

in vec2 TexCoords;
in vec3 NDC;

uniform sampler2D depthPrepass;
uniform sampler2D volumetricMap;
uniform sampler2D frameMap;

void main()
{

    float upSampledDepth = texture(depthPrepass, TexCoords).x;

    vec3 color = 0.0f.xxx;
    float totalWeight = 0.0f;

    vec2 screenCoordinates = gl_FragCoord.xy;

    // Select the closest downscaled pixels.

    vec2 texelSize = vec2(1.0) / textureSize(volumetricMap, 0);

    float xOffset = (int(gl_FragCoord.x) % 2 == 0 ? -1.0 : 1.0) / textureSize(volumetricMap, 0).x; //int(screenCoordinates.x) % 2 == 0 ? -1 : 1;
    float yOffset = (int(gl_FragCoord.y) % 2 == 0 ? -1.0 : 1.0) / textureSize(volumetricMap, 0).y;

    for (float a = -1.5; a <= 1.5; a += 1.0) {
        for (float b = -1.5; b <= 1.5; b += 1.0) {
            vec2 offsetTexCoords = TexCoords + vec2(a, b) * texelSize;
            vec3 downscaledColor = texture(volumetricMap, offsetTexCoords).xyz;
            color += downscaledColor;
        }
    }

    /*
    vec2 offsets[] = {vec2(0, 0),
    vec2(0, yOffset),
    vec2(xOffset, 0),
    vec2(xOffset, yOffset)};


    for (int i = 0; i < 4; i ++)
    {

        vec2 offsetTexCoords = TexCoords + offsets[i];
        vec3 downscaledColor = texture(volumetricMap, offsetTexCoords).xyz;
        float downscaledDepth = texture(depthPrepass, offsetTexCoords).r;

        float currentWeight = 1.0f;
        currentWeight *= max(0.0f, 1.0f - (0.05f) * abs(downscaledDepth - upSampledDepth));

        color += downscaledColor; // * currentWeight;
        totalWeight += currentWeight;
    }
    */

    vec3 volumetricLight;
    const float epsilon = 0.0001f;
    volumetricLight.xyz = color/ 16; //(totalWeight + epsilon);

    vec3 currentFrame = texture(frameMap, vec2(TexCoords.x, TexCoords.y)).xyz;

    currentFrame = currentFrame / (currentFrame + vec3(1.0));
    currentFrame = pow(currentFrame, vec3(1.0/2.2));

    currentFrame = currentFrame * (volumetricLight);

    //currentFrame = currentFrame / (currentFrame + vec3(1.0));
    //currentFrame = pow(currentFrame, vec3(1.0/2.2));

    //currentFrame = vec3(0.5);
    //currentFrame = vec3(0.5);

    FragColor = vec4(currentFrame, 1.0);

    //FragColor = vec4(vec3(texture(volumetricMap, vec2(TexCoords.x, TexCoords.y)).xyz) * 0.2, 1.0f);
}
