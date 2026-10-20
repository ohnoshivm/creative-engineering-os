precision highp float;
uniform sampler2D uTex;
in vec2 vUv;
out vec4 fragColor;
// @common
void main() {
  vec3 c = texture(uTex, vUv).rgb + vec3(0.04, 0.045, 0.05);
  c += (ign(gl_FragCoord.xy) - 0.5) / 255.0;
  fragColor = vec4(c, 1.0);
}
