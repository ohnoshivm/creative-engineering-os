uniform float uTime;
uniform float uTension;
uniform float uPhase;
uniform vec2 uPointer;
varying vec2 vUv;
varying float vHeight;
varying vec3 vSurfaceNormal;
float heightAt(vec2 p) {
  float bend = exp(-length(p-uPointer*2.5)*0.55);
  return sin(p.x*1.5 + uTime*.55 + uPhase*3.) * cos(p.y*1.3 + uPhase*2.) * (.25+uTension*.65) + bend*uPointer.y*.65;
}
void main() {
  vUv = uv;
  vec3 p = position;
  p.z = heightAt(p.xy);
  float e = .015;
  float dx = (heightAt(p.xy+vec2(e,0.))-heightAt(p.xy-vec2(e,0.)))/(2.*e);
  float dy = (heightAt(p.xy+vec2(0.,e))-heightAt(p.xy-vec2(0.,e)))/(2.*e);
  vSurfaceNormal=normalize(normalMatrix*vec3(-dx,-dy,1.));
  vHeight=p.z;
  gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
}
