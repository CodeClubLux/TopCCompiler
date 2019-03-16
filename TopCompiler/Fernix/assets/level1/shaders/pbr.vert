#version 440 core
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

void main()
{
    if (transformUVs.x == 0 && transformUVs.y == 0) {
        TexCoords = aTexCoords;
    } else {
        TexCoords = vec2(aTexCoords.x * transformUVs.x, aTexCoords.y * transformUVs.y);
    }

    gl_Position = projection * view * model * vec4(aPos, 1.0);


	FragPos = vec3(model * vec4(aPos, 1.0));

	vec3 T = normalize(vec3(model * vec4(aTangent, 0.0)));
	vec3 N = normalize(vec3(model * vec4(aNormal, 0.0)));

	NORMAL = aNormal;

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