#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 viewPos;

/* Sun */
uniform vec3 sunDirection;
uniform vec3 sunColor;
uniform float sunIntensity;

/* Environment */
uniform samplerCube skybox;

void main()
{
    vec3 N = normalize(Normal);
    vec3 V = normalize(viewPos - FragPos);
    vec3 L = normalize(-sunDirection);
    vec3 H = normalize(V + L);

    /* Ambient from skybox */
    vec3 ambient = texture(skybox, N).rgb * 0.25;

    /* Diffuse */
    float diff = max(dot(N, L), 0.0);
    vec3 diffuse = diff * sunColor;

    /* Specular (Blinn-Phong) */
    float spec = pow(max(dot(N, H), 0.0), 64.0);
    vec3 specular = spec * sunColor * 0.5;

    vec3 color =
        ambient +
        (diffuse + specular) * sunIntensity;

    /* Tone map + gamma */
    color = color / (color + vec3(1.0));
    color = pow(color, vec3(1.0 / 2.2));

    FragColor = vec4(color, 1.0);
}
