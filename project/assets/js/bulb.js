// Lampadina 3D (Three.js) che compare accanto alla mano alzata.
import * as THREE from "../vendor/three.module.min.js";

// ---- 3D light bulb that appears by the raised hand ----
const W = 1080;
const H = 1920;
const canvas = document.getElementById("bulb3d");
const renderer = new THREE.WebGLRenderer({
  canvas,
  alpha: true,
  antialias: true,
  preserveDrawingBuffer: true,
});
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
const FOV = 30;
const camera = new THREE.PerspectiveCamera(FOV, W / H, 10, 10000);
const dist = H / 2 / Math.tan(THREE.MathUtils.degToRad(FOV / 2));
camera.position.set(0, 0, dist);
// Pixel (px, py) on the frame -> world point on the z = 0 plane.
const toWorld = (px, py) => new THREE.Vector3(px - W / 2, H / 2 - py, 0);

scene.add(new THREE.HemisphereLight(0xfff4e0, 0x404a40, 1.4));
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(400, 600, 900);
scene.add(key);

const bulb = new THREE.Group();
scene.add(bulb);
const inner = new THREE.Group(); // spins / tilts
bulb.add(inner);

// Glass: lathe profile of a classic bulb (units = px, total ~230 tall)
const R = 70;
const prof = [new THREE.Vector2(29, -40), new THREE.Vector2(30, -22)];
for (let i = 0; i <= 28; i++) {
  const a = THREE.MathUtils.degToRad(-50 + (i / 28) * 140);
  prof.push(new THREE.Vector2(Math.max(0.01, Math.cos(a) * R), Math.sin(a) * R + 40));
}
const glassMat = new THREE.MeshPhysicalMaterial({
  color: 0xffe08a,
  emissive: 0xffb81f,
  emissiveIntensity: 0,
  roughness: 0.08,
  metalness: 0,
  clearcoat: 1,
  clearcoatRoughness: 0.05,
  transparent: true,
  opacity: 0.55,
  side: THREE.DoubleSide,
});
const glass = new THREE.Mesh(new THREE.LatheGeometry(prof, 48), glassMat);
inner.add(glass);

// Filament
const filMat = new THREE.MeshStandardMaterial({
  color: 0x8a6a30,
  emissive: 0xffaa22,
  emissiveIntensity: 0,
});
const pts = [];
for (let i = 0; i <= 40; i++) {
  const u = i / 40;
  pts.push(
    new THREE.Vector3(
      -22 + 44 * u,
      46 + Math.sin(u * Math.PI * 6) * 7,
      Math.cos(u * Math.PI * 6) * 7,
    ),
  );
}
const fil = new THREE.Mesh(
  new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 2.2, 8),
  filMat,
);
inner.add(fil);
for (const x of [-22, 22]) {
  const wire = new THREE.Mesh(
    new THREE.CylinderGeometry(1.4, 1.4, 70, 6),
    new THREE.MeshStandardMaterial({ color: 0x777777, metalness: 0.6, roughness: 0.4 }),
  );
  wire.position.set(x * 0.8, 12, 0);
  wire.rotation.z = x > 0 ? 0.25 : -0.25;
  inner.add(wire);
}

// Screw base
const metal = new THREE.MeshStandardMaterial({
  color: 0xc9ccd1,
  metalness: 0.9,
  roughness: 0.28,
});
const base = new THREE.Mesh(new THREE.CylinderGeometry(29, 26, 52, 40), metal);
base.position.y = -66;
inner.add(base);
for (let i = 0; i < 4; i++) {
  const ring = new THREE.Mesh(new THREE.TorusGeometry(29 - i * 0.8, 3.4, 10, 40), metal);
  ring.rotation.x = Math.PI / 2;
  ring.position.y = -48 - i * 12;
  inner.add(ring);
}
const tip = new THREE.Mesh(
  new THREE.SphereGeometry(14, 24, 12, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2),
  new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.5, roughness: 0.5 }),
);
tip.position.y = -92;
inner.add(tip);

const bulbLight = new THREE.PointLight(0xffc44d, 0, 600, 1.2);
bulbLight.position.set(0, 46, 40);
inner.add(bulbLight);

// Glow halo + rays (camera-facing, additive). Texture drawn procedurally.
const gc = document.createElement("canvas");
gc.width = gc.height = 256;
const g2 = gc.getContext("2d");
const grad = g2.createRadialGradient(128, 128, 0, 128, 128, 128);
grad.addColorStop(0, "rgba(255,240,180,1)");
grad.addColorStop(0.25, "rgba(255,210,90,0.65)");
grad.addColorStop(0.6, "rgba(255,180,40,0.18)");
grad.addColorStop(1, "rgba(255,170,30,0)");
g2.fillStyle = grad;
g2.fillRect(0, 0, 256, 256);
const glowTex = new THREE.CanvasTexture(gc);
glowTex.colorSpace = THREE.SRGBColorSpace;
const glow = new THREE.Sprite(
  new THREE.SpriteMaterial({
    map: glowTex,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0,
  }),
);
glow.scale.set(380, 380, 1);
glow.position.set(0, 40, -10);
bulb.add(glow);

const rays = new THREE.Group();
rays.position.set(0, 40, 0);
bulb.add(rays);
const rayMat = new THREE.MeshBasicMaterial({
  color: 0xffd23f,
  transparent: true,
  opacity: 0,
  depthWrite: false,
});
const NR = 9;
for (let i = 0; i < NR; i++) {
  // fan of rays over the top of the bulb (skip the bottom, where the base is)
  const a = THREE.MathUtils.degToRad(-60 + (i / (NR - 1)) * 300);
  const ray = new THREE.Mesh(new THREE.PlaneGeometry(9, 38), rayMat);
  const pivot = new THREE.Group();
  pivot.rotation.z = a;
  ray.position.y = 118;
  pivot.add(ray);
  rays.add(pivot);
}

// Hand track on the rough cut (px), measured frame by frame.
const TRACK = [
  [2.58, 20, 330],
  [2.7, 30, 255],
  [2.8, 60, 255],
  [3.0, 60, 240],
  [3.1, 75, 270],
  [3.3, 90, 270],
  [3.4, 90, 285],
  [3.5, 105, 315],
  [3.6, 120, 450],
];
const OFFSET = [175, -60]; // bulb sits up-right of the fist, never on the face
const handAt = (t) => {
  if (t <= TRACK[0][0]) return [TRACK[0][1], TRACK[0][2]];
  for (let i = 1; i < TRACK.length; i++) {
    if (t <= TRACK[i][0]) {
      const [t0, x0, y0] = TRACK[i - 1];
      const [t1, x1, y1] = TRACK[i];
      const k = (t - t0) / (t1 - t0);
      const e = k * k * (3 - 2 * k);
      return [x0 + (x1 - x0) * e, y0 + (y1 - y0) * e];
    }
  }
  const l = TRACK[TRACK.length - 1];
  return [l[1], l[2]];
};

const T_IN = 2.62;
const T_OUT = 3.42;
const clamp01 = (v) => Math.min(1, Math.max(0, v));
const backOut = (k) => {
  const s = 2.2;
  return 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2);
};
// Switch-on: flicker then full brightness
const litAt = (t) => {
  const u = t - (T_IN + 0.06);
  if (u < 0) return 0;
  if (u < 0.05) return 0.9;
  if (u < 0.09) return 0.1;
  if (u < 0.13) return 1;
  if (u < 0.16) return 0.35;
  return 1;
};

function renderAt(t) {
  let s = 0;
  if (t >= T_IN && t < T_OUT) s = backOut(clamp01((t - T_IN) / 0.22));
  else if (t >= T_OUT) s = 1 - Math.pow(clamp01((t - T_OUT) / 0.12), 2);
  s = Math.max(0, s);
  bulb.visible = s > 0.001;

  if (bulb.visible) {
    const [hx, hy] = handAt(t);
    const p = toWorld(hx + OFFSET[0], hy + OFFSET[1]);
    bulb.position.copy(p);
    bulb.scale.setScalar(s);
    const lt = t - T_IN;
    inner.rotation.y = -0.5 + lt * 1.6;
    inner.rotation.z = 0.28 + Math.sin(lt * 5) * 0.06;
    inner.rotation.x = 0.18;
    rays.rotation.z = 0.28;

    const lit = litAt(t);
    glassMat.emissiveIntensity = 0.1 + 1.6 * lit;
    glassMat.opacity = 0.55 + 0.3 * lit;
    filMat.emissiveIntensity = 0.2 + 5 * lit;
    bulbLight.intensity = 60000 * lit;
    glow.material.opacity = 0.95 * lit;
    const pulse = 1 + 0.06 * Math.sin(lt * 18);
    glow.scale.set(380 * pulse, 380 * pulse, 1);
    const rayK = clamp01((t - (T_IN + 0.24)) / 0.12);
    rayMat.opacity = 0.95 * lit * rayK;
    rays.scale.setScalar(0.7 + 0.3 * rayK + 0.04 * Math.sin(lt * 14));
  }
  renderer.render(scene, camera);
}

window.__renderers = window.__renderers || [];
window.__renderers.push(renderAt);
renderAt(window.__hfThreeTime || 0);
