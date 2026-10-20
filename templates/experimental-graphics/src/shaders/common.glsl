// Shared helpers. Integer-style hash (stable across GPUs, unlike sin-fract on mediump).
float hash12(vec2 p) {
  vec3 p3 = fract(vec3(p.xyx) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}
// Polynomial smooth minimum (k = blend radius) — organic unions of SDFs.
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}
// Interleaved gradient noise for dithering the final colour (kills banding).
float ign(vec2 fragCoord) { return fract(52.9829189 * fract(dot(fragCoord, vec2(0.06711056, 0.00583715)))); }
