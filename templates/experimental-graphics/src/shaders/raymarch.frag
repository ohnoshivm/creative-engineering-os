// Raymarched blobs that merge with a smooth minimum; one follows the pointer.
precision highp float;
uniform vec2 uResolution;
uniform vec2 uPointer;     // -1..1
uniform float uTime;
uniform float uBlend;      // smooth-min radius
in vec2 vUv;
out vec4 fragColor;
// @common

float sdSphere(vec3 p, float r) { return length(p) - r; }

float map(vec3 p) {
  float d = sdSphere(p - vec3(uPointer * vec2(1.6, 1.0), 0.0), 0.55);
  for (int i = 0; i < 5; i++) {
    float fi = float(i);
    vec3 c = vec3(sin(uTime * 0.5 + fi * 1.7) * 1.4, cos(uTime * 0.37 + fi * 2.3) * 0.8, sin(uTime * 0.29 + fi) * 0.5);
    d = smin(d, sdSphere(p - c, 0.32 + 0.08 * fi), uBlend);
  }
  return d;
}

vec3 normalAt(vec3 p) {
  // Tetrahedron technique: 4 samples instead of 6.
  const vec2 k = vec2(1.0, -1.0);
  const float h = 0.0015;
  return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) + k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
}

void main() {
  vec2 uv = (vUv * 2.0 - 1.0) * vec2(uResolution.x / uResolution.y, 1.0);
  vec3 ro = vec3(0.0, 0.0, 4.0);
  vec3 rd = normalize(vec3(uv, -2.2));
  float t = 0.0; bool hit = false;
  for (int i = 0; i < 96; i++) {
    float d = map(ro + rd * t);
    if (d < 0.0008 * t) { hit = true; break; }
    t += d;
    if (t > 12.0) break;
  }
  vec3 bg = vec3(0.0045, 0.005, 0.006); // linear values; gamma-encoded once at the end
  vec3 col = bg;
  if (hit) {
    vec3 p = ro + rd * t;
    vec3 n = normalAt(p);
    vec3 l = normalize(vec3(-0.5, 0.8, 0.6));
    float diff = max(dot(n, l), 0.0);
    float fres = pow(1.0 - max(dot(n, -rd), 0.0), 3.0);
    vec3 base = mix(vec3(0.85, 0.12, 0.03), vec3(0.03, 0.18, 0.9), 0.5 + 0.5 * n.y); // linear
    col = base * (0.06 + 0.94 * diff) + fres * vec3(0.8, 0.85, 1.0) * 0.6;
  }
  col = pow(col, vec3(1.0 / 2.2));
  col += (ign(gl_FragCoord.xy) - 0.5) / 255.0;
  fragColor = vec4(col, 1.0);
}
