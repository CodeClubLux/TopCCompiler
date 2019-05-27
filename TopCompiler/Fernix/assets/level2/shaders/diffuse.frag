out vec4 FragColor;

in vec2 TexCoords;
in vec3 FragPos;
in mat3 TBN;
in vec3 NORMAL;

uniform samplerCube irradianceMap;
uniform samplerCube prefilterMap;
uniform sampler2D   brdfLUT;

uniform vec3 viewPos;

struct Material {
	vec3 diffuse;
};

struct DirLight {
	vec3 direction;
    vec3 color;
};

struct PointLight {
	vec3 position;
    vec3 color;
};

uniform Material material;

uniform DirLight dirLight;
#define MAX_NR_POINT_LIGHTS 4

uniform int NR_POINT_LIGHTS;
uniform PointLight pointLights[MAX_NR_POINT_LIGHTS];

const float PI = 3.14159265359;

vec3 viewDir;
vec3 norm;

vec3 CalcDirLight(DirLight light, vec3 N, vec3 V) {
	vec3 L = normalize(-light.direction);
	float diff = max(dot(N, L), 0.0);

    return diff * material.diffuse;
}

vec3 CalcPointLight(PointLight light, vec3 N, vec3 WorldPos, vec3 V)
{
    vec3 L = normalize(light.position - WorldPos);
	float diff = max(dot(N, L), 0.0);

	return diff * material.diffuse;
}

void main()
{
    // properties
    viewDir = normalize(viewPos - FragPos);
    norm = NORMAL;

	vec3 Lo = vec3(0.0);

    // phase 1: Directional lighting
    Lo += CalcDirLight(dirLight, norm, viewDir);
    // phase 2: Point lights
    for(int i = 0; i < NR_POINT_LIGHTS; i++) {
        Lo += CalcPointLight(pointLights[i], norm, FragPos, viewDir);
	}

	vec3 ambient = material.diffuse * 0.3;

    vec3 color = ambient + Lo;

    FragColor = vec4(color, 1);
}