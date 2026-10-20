precision highp float;
uniform float uLines;
varying vec2 vUv;
varying float vHeight;
varying vec3 vSurfaceNormal;
void main() {
  float light=.5+.5*dot(normalize(vSurfaceNormal),normalize(vec3(-.4,.8,1.)));
  vec3 color=mix(vec3(.035,.075,.38),vec3(.13,.34,.95),light);
  float contour=abs(fract(vUv.y*uLines)-.5);
  float line=1.-smoothstep(.035,.035+fwidth(vUv.y*uLines)*1.3,contour);
  color=mix(color,vec3(.65,.8,1.),line*.72);
  float dither=fract(dot(gl_FragCoord.xy,vec2(.06711056,.00583715)))*.003;
  gl_FragColor=vec4(color+dither,1.);
  #include <colorspace_fragment>
}
