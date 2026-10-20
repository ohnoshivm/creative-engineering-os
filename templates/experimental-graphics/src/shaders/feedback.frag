// Ping-pong feedback: last frame is advected along a curl-like field and faded; the pointer injects ink.
precision highp float;
uniform sampler2D uPrev;
uniform vec2 uResolution;
uniform vec2 uPointer;   // 0..1
uniform float uTime;
uniform float uInject;
in vec2 vUv;
out vec4 fragColor;
// @common

vec2 field(vec2 p) {
  float a = sin(p.x * 6.0 + uTime * 0.6) + cos(p.y * 5.0 - uTime * 0.4);
  return vec2(cos(a), sin(a)) * 0.0016;
}

void main() {
  vec2 uv = vUv;
  vec4 prev = texture(uPrev, uv - field(uv));
  float aspect = uResolution.x / uResolution.y;
  vec2 d = (uv - uPointer) * vec2(aspect, 1.0);
  float ink = exp(-dot(d, d) * 900.0) * uInject;
  vec3 inkCol = 0.5 + 0.5 * cos(6.2831 * (uTime * 0.05 + vec3(0.0, 0.33, 0.67)));
  vec3 col = prev.rgb * 0.985 + ink * inkCol;
  fragColor = vec4(col, 1.0);
}
