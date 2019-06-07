out vec4 FragColor;

in vec2 TexCoords;
in vec3 NDC;

uniform sampler2D depthPrepass;
uniform sampler2D depthMap;
uniform float gCascadeEndClipSpace[2];

uniform vec3 viewPos;
uniform vec3 sunColor;
uniform vec3 sunPosition;
uniform vec3 sunDirection;

#define G_SCATTERING 0.1
#define NB_STEPS 20
#define NB_MAX_STEPS 25
#define PI 3.14159265359
#define scatterColor 0.1

uniform mat4 toWorld;
uniform mat4 toLight;
uniform vec3 camPosition;

uniform int cascadeLevel;
uniform float endCascade;

//code inspired by http://www.alexandre-pestana.com/volumetric-lights/
float ComputeScattering(float lightDotView) {
    float result = 1.0f - G_SCATTERING * G_SCATTERING;
    result /= (4.0f * PI * pow(1.0f + G_SCATTERING * G_SCATTERING - (2.0f * G_SCATTERING) *  lightDotView, 1.5f));

    return result;
}

vec3 getWorldPosition(float fragDepth) {
    vec4 FragPosLightSpace = toWorld * vec4(NDC.x, NDC.y, fragDepth, 1.0);
    FragPosLightSpace /= FragPosLightSpace.w;

    return FragPosLightSpace.xyz;
}

float inShadow(vec3 worldSpace) {
    vec4 fragPosLightSpace = toLight * vec4(worldSpace, 1.0);

    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;

    float bias = 0.003; //max(0.03 * (1.0 - dot(normal, dirLightDirection)), 0.003);
    float currentDepth = projCoords.z;

    float pcfDepth = texture(depthMap, projCoords.xy ).r;

    return (currentDepth - bias) > pcfDepth ? 1.0f : 0.0f;
}

void main()
{
    float fragDepth = texture(depthPrepass, TexCoords).r;

    fragDepth = (fragDepth * 2) - 1.0;
    //fragDepth += 0.01;

    float currentDepth = -1f;

    vec3 endRayPosition = getWorldPosition(fragDepth);

    vec3 startPosition = camPosition;

    vec3 rayVector = endRayPosition.xyz - startPosition;

    float rayLength = length(rayVector);
    vec3 rayDirection = rayVector / rayLength;

    float stepLength = rayLength / NB_STEPS;
    float stepDistance = (fragDepth + 1.0) / NB_STEPS;

    vec3 step = rayDirection * stepLength;

    float ditherPattern[4][4] = {{ 0.0f, 0.5f, 0.125f, 0.625f},
    { 0.75f, 0.22f, 0.875f, 0.375f},
    { 0.1875f, 0.6875f, 0.0625f, 0.5625},
    { 0.9375f, 0.4375f, 0.8125f, 0.3125}};

    float ditherValue = ditherPattern[int(gl_FragCoord.x) % 4][int(gl_FragCoord.y) % 4];

    // Offset the start position.
    startPosition += step * ditherValue;

    vec3 currentPosition = startPosition;

    vec3 accumFog = 0.0f.xxx;


    for (int i = 0; i < NB_STEPS; i++)
    {
        if (gCascadeEndClipSpace[0] <= currentDepth && currentDepth <= gCascadeEndClipSpace[1] && currentDepth != 1.0) {
            if (inShadow(currentPosition) < 0.5) {
                vec3 sDirection = normalize(currentPosition - sunPosition);
                accumFog += ComputeScattering(dot(rayDirection, sunDirection)).xxx * scatterColor;
                //accumFog += vec3(1.0f);
            }
        }
        currentPosition += step;
        currentDepth += stepDistance;
    }
    accumFog /= NB_STEPS;

    float depthFromCamera = length(currentPosition - camPosition);
    accumFog *= depthFromCamera * (200.0 / endCascade);
    accumFog += vec3(0.6, 0.6, 1) * 0.0001 * depthFromCamera;

    FragColor = vec4(accumFog, 1.0);
    //FragColor = vec4(vec3(fragDepth) * 0.3, 1.0);
    //FragColor = vec4(vec3(normalize(sunDirection)), 1.0);
    //FragColor = vec4(vec3(rayDirection), 1.0);

    /*if (gCascadeEndClipSpace[0] <= fragDepth && fragDepth <= gCascadeEndClipSpace[1]) {
        if (fragDepth != 1.0) {
            FragColor = vec4(vec3(inShadow(endRayPosition)), 1);
        }
        //FragColor = vec4(vec3(inShadow(endRayPosition)), 1);
        //FragColor = vec4(vec3(cascadeLevel / 3.0), 1.0);
    } else {
        FragColor = vec4(vec3(0), 1.0);
    }
    */
}

