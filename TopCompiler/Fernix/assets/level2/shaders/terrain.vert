layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aBitangent;

out vec2 TexCoords;
out vec3 Normal;
out vec3 FragPos;
out mat3 TBN;
out vec3 NORMAL;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec2 transformUVs;

struct Material {
	sampler2D diffuse;
	sampler2D metallic;
	sampler2D roughness;
	sampler2D normal;
};

uniform Material material;
uniform sampler2D displacement;
uniform vec2 displacement_offset;
uniform vec2 displacement_scale;

uniform float max_height;

void main()
{
    TexCoords = vec2(aTexCoords.x, aTexCoords.y);
    //TexCoords = vec2(aTexCoords.x * transformUVs.x, aTexCoords.y * transformUVs.y);

    vec2 displacement_tex = (vec2(aTexCoords.y, 1.0 - aTexCoords.x) * displacement_scale) + vec2(displacement_offset.x, displacement_offset.y);
    float height = texture(displacement, displacement_tex).x;
    height *= max_height / 30.0f;

    gl_Position = projection * view * model * vec4(aPos + vec3(0,height,0), 1.0);


    vec3 T = normalize(vec3(model * vec4(aTangent, 0.0)));
	vec3 N = normalize(vec3(model * vec4(aNormal, 0.0)));

	// re-orthogonalize T with respect to N
	//T = normalize(T - dot(T, N) * N);
	// then retrieve perpendicular vector B with the cross product of T and N
	vec3 B = cross(N, T);

	// TBN must form a right handed coord system.
    // Some models have symetric UVs. Check and fix.
    if (dot(cross(N, T), B) < 0.0)
		T = T * -1.0;

	TBN = mat3(T, B, N);
}