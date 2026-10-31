"""Add this room's engine extensions to the page build.py just wrote.

    python3 build/patch.py index.html

Everything here is generic (no room-specific geometry), so it survives a new config.js and can be
re-applied after the skill's engine changes. Each edit asserts its anchor appears exactly once, so a
changed engine fails loudly instead of silently dropping a feature.

What it adds:
  * walk      a first-person view inside the room: W A S D / arrows, drag or pointer lock to look
  * builders  wallshelf, pegboard, beanbag, curtain, sconce, guitar, skateboard
  * box       honours `mount`, so a box can hang on a wall (a window AC, a basket over a wardrobe)
  * prints    art print styles 'tapestry' and 'board' (a whiteboard)
  * fan       ROOM.fan: {c, span, drop, blades} draws a ceiling fan, shown with the ceiling
"""
import sys

# ---------------------------------------------------------------- walk mode

WALK = r"""
/* ---------- walk: a first-person view from inside the room (W A S D or the arrows, drag or pointer lock to look) ---------- */
var WALK = {x: RC[0], z: RC[1], yaw: 0, pitch: 0, eye: 64, fov: 72, keys: {}, look: null, t0: 0};
var WKEY = {w: 'f', s: 'b', a: 'l', d: 'r', arrowup: 'f', arrowdown: 'b', arrowleft: 'tl', arrowright: 'tr', shift: 'run'};
function walkFree(x, z, r){ /* inside the walls and clear of the furniture, by r */
  var p = [x, z], i;
  if (!inPoly(p, OUT)) return false;
  for (i = 0; i < WALLS.length; i++){ var w = WALLS[i], t = dot(sub(p, w.a), w.d); if (t > -r && t < w.L + r && -dot(sub(p, w.a), w.n) < r) return false; }
  function clearOf(c, rot, bw, bd){ var a = (rot || 0) * Math.PI / 180, dx = x - c[0], dz = z - c[1];
    return Math.abs(dx * Math.cos(a) + dz * Math.sin(a)) > bw / 2 + r || Math.abs(-dx * Math.sin(a) + dz * Math.cos(a)) > bd / 2 + r; }
  var ids = placed(LAYOUTS[cur]);
  for (i = 0; i < ids.length; i++){ var it = ITEMS[ids[i]], q = place()[ids[i]]; if (it && !it.floor && !clearOf(q, q[2], it.w, it.d)) return false; }
  for (i = 0; i < FIXED.length; i++){ var f = FIXED[i].f; if (!clearOf(f.c, f.rot, f.w, f.d)) return false; }
  return true; }
function walkStart(){ /* the first clear spot on the way in from the first door, looking into the open middle */
  var dr = OPEN.filter(function(o){ return o.type === 'door'; })[0], op = EVAL[cur].open,
      aim = op && op.size ? [op.x + op.size / 2, op.y + op.size / 2] : RC,
      from = dr ? add(dr.cc, mul(dr.w.n, -16)) : aim, c = null, t, p;
  for (t = 0; t <= 1.0001 && !c; t += 0.08){ p = add(from, mul(sub(aim, from), t)); if (walkFree(p[0], p[1], 11)) c = p; }
  if (!c) c = aim; var v = sub(aim, c); if (len(v) < 2) v = sub(aim, from);
  WALK.x = c[0]; WALK.z = c[1]; WALK.yaw = len(v) > 0.5 ? Math.atan2(v[0], -v[1]) * 180 / Math.PI : 0; WALK.pitch = 0; }
function walkCam(){ var y = WALK.yaw * Math.PI / 180, p = WALK.pitch * Math.PI / 180, pos = V(WALK.x, WALK.eye, WALK.z);
  persp.position.copy(pos); persp.up.set(0, 1, 0); persp.lookAt(pos.clone().add(V(Math.sin(y) * Math.cos(p), Math.sin(p), -Math.cos(y) * Math.cos(p))));
  persp.fov = WALK.fov; persp.aspect = MV.w / MV.h; persp.near = 1; persp.far = 4000; persp.updateProjectionMatrix(); }
function walkStep(now){ var dt = Math.min(0.08, (now - (WALK.t0 || now)) / 1000), K = WALK.keys, moved = 0; WALK.t0 = now;
  var tn = (K.tr ? 1 : 0) - (K.tl ? 1 : 0); if (tn){ WALK.yaw += tn * 85 * dt; moved = 1; }
  var f = (K.f ? 1 : 0) - (K.b ? 1 : 0), s = (K.r ? 1 : 0) - (K.l ? 1 : 0);
  if (f || s){ var y = WALK.yaw * Math.PI / 180, v = (K.run ? 62 : 32) * dt / Math.hypot(f, s);   /* inches a second: a stroll, or a stride with shift */
    var dx = (Math.sin(y) * f + Math.cos(y) * s) * v, dz = (-Math.cos(y) * f + Math.sin(y) * s) * v;
    if (walkFree(WALK.x + dx, WALK.z, 11)) WALK.x += dx; if (walkFree(WALK.x, WALK.z + dz, 11)) WALK.z += dz; moved = 1; }   /* one axis at a time, so you slide along a wall */
  if (moved) dirty3 = true; return moved; }
function walkLook(dx, dy){ WALK.yaw += dx * 0.17; WALK.pitch = Math.max(-72, Math.min(72, WALK.pitch - dy * 0.15)); dirty3 = true; }
function enterWalk(){ if (mode === 'photo') exitPhoto(); mode = 'walk'; CEIL.visible = true; select(null); walkStart(); WALK.keys = {}; WALK.t0 = 0;
  $('#walkBar').hidden = false; $('#zoomCtl').hidden = true; mc.style.cursor = 'crosshair'; planDirty = true; attachGizmo();
  cutTargets(); SEG.forEach(function(sg){ sg.cut = sg.target; applyCut(sg); }); shadowsDirty = dirty3 = true; renderViews(); }
function exitWalk(){ mode = 'model'; CEIL.visible = false; WALK.keys = {}; WALK.look = null;
  if (document.pointerLockElement === mc) document.exitPointerLock();
  $('#walkBar').hidden = true; $('#zoomCtl').hidden = false; mc.style.cursor = 'default'; planDirty = true; attachGizmo();
  cutTargets(); shadowsDirty = dirty3 = true; renderViews(); }
mc.addEventListener('pointerdown', function(e){ if (mode !== 'walk') return; WALK.look = {x: e.clientX, y: e.clientY};
  if (e.pointerType === 'mouse' && mc.requestPointerLock) mc.requestPointerLock(); else mc.setPointerCapture(e.pointerId); });
mc.addEventListener('pointermove', function(e){ if (mode !== 'walk' || !WALK.look || document.pointerLockElement === mc) return;
  walkLook(e.clientX - WALK.look.x, e.clientY - WALK.look.y); WALK.look = {x: e.clientX, y: e.clientY}; });
['pointerup', 'pointercancel', 'pointerleave'].forEach(function(t){ mc.addEventListener(t, function(){ if (mode === 'walk') WALK.look = null; }); });
document.addEventListener('mousemove', function(e){ if (mode === 'walk' && document.pointerLockElement === mc) walkLook(e.movementX, e.movementY); });
window.addEventListener('keydown', function(e){ if (mode !== 'walk' || /INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
  if (e.key === 'Escape'){ exitWalk(); return; } var k = WKEY[e.key.toLowerCase()]; if (k){ WALK.keys[k] = 1; e.preventDefault(); } });
window.addEventListener('keyup', function(e){ var k = WKEY[e.key.toLowerCase()]; if (k) WALK.keys[k] = 0; });
window.addEventListener('blur', function(){ WALK.keys = {}; });
[].forEach.call($('#walkPad').children, function(b){ var k = b.dataset.k, on = function(e){ e.preventDefault(); WALK.keys[k] = 1; }, off = function(){ WALK.keys[k] = 0; };
  b.addEventListener('pointerdown', on); ['pointerup', 'pointerleave', 'pointercancel'].forEach(function(t){ b.addEventListener(t, off); }); });
$('#walkExit').onclick = exitWalk;
"""

EDITS = [
    # ---- the walk block itself, before the photo match
    ("\n/* photo match: a perspective camera where the phone stood, the photo laid over the model */",
     WALK + "\n/* photo match: a perspective camera where the phone stood, the photo laid over the model */"),

    # ---- a Walk button beside the corner views
    ("b.onclick = function(){ goView(v[0]); }; box.appendChild(b); }); }",
     "b.onclick = function(){ goView(v[0]); }; box.appendChild(b); });\n"
     "  var wb = el('button', mode === 'walk' ? 'on' : '', 'Walk'); wb.title = 'Walk through the room: W A S D, drag to look';\n"
     "  wb.onclick = function(){ if (mode === 'walk') exitWalk(); else enterWalk(); }; box.appendChild(wb); }"),

    # ---- a corner view leaves the walk
    ("function goView(name, instant){ curView = name;",
     "function goView(name, instant){ if (mode === 'walk') exitWalk(); curView = name;"),

    # ---- walk renders through the photo camera, full pane
    ("function render3d(){ mountVis(); syncDecals(); if (mode === 'photo'){",
     "function render3d(){ mountVis(); syncDecals(); if (mode === 'walk'){ walkCam(); post(persp, MV.w, MV.h); }\n"
     "  else if (mode === 'photo'){"),

    # ---- step the walk each frame; a held key keeps the loop awake
    ("function loop(now){ requestAnimationFrame(loop); var active = false;",
     "function loop(now){ requestAnimationFrame(loop); var active = false; if (mode === 'walk' && walkStep(now)) active = true;"),

    # ---- walls stand, the ceiling is on and the room lights itself, as through a photo's camera
    ("SEG.forEach(function(sg){ sg.target = mode === 'photo' ? RH :",
     "SEG.forEach(function(sg){ sg.target = mode === 'photo' || mode === 'walk' ? RH :"),
    ("OBJ[k].visible = mode === 'photo' || !best ||",
     "OBJ[k].visible = mode === 'photo' || mode === 'walk' || !best ||"),
    ("var col = LOOK === 'colour', ph = col && mode === 'photo'; LIT = {mode: mode, look: LOOK};",
     "var col = LOOK === 'colour', ph = col && (mode === 'photo' || mode === 'walk'); LIT = {mode: mode, look: LOOK};"),
    ("if (LOOK !== 'colour' || mode !== 'photo'){ envDirty = 0; return; }",
     "if (LOOK !== 'colour' || (mode !== 'photo' && mode !== 'walk')){ envDirty = 0; return; }"),

    # ---- the map-style camera keeps out of the way
    ("mc.addEventListener('pointerdown', function(e){ if (mode === 'photo' || GIZ.some",
     "mc.addEventListener('pointerdown', function(e){ if (mode === 'photo' || mode === 'walk' || GIZ.some"),
    ("if (!mdrag){ if (mode !== 'photo' && e.pointerType === 'mouse')",
     "if (!mdrag){ if (mode !== 'photo' && mode !== 'walk' && e.pointerType === 'mouse')"),
    ("mc.addEventListener('wheel', function(e){ if (mode === 'photo') return;",
     "mc.addEventListener('wheel', function(e){ if (mode === 'walk'){ e.preventDefault(); WALK.fov = Math.max(38, Math.min(95, WALK.fov + e.deltaY * 0.02)); dirty3 = true; return; }\n"
     "  if (mode === 'photo') return;"),

    # ---- the bar, and the Walk button's room in the markup
    ('<div class="ctl tl" id="photoBar" hidden>',
     '<div class="ctl tl" id="walkBar" hidden><span>Walk</span>'
     '<span class="seg" id="walkPad"><button data-k="l" aria-label="Left">&#9664;</button><button data-k="f" aria-label="Forward">&#9650;</button>'
     '<button data-k="b" aria-label="Back">&#9660;</button><button data-k="r" aria-label="Right">&#9654;</button></span>'
     '<span class="hint">W A S D &middot; drag to look</span><button id="walkExit">Exit</button></div>\n'
     '    <div class="ctl tl" id="photoBar" hidden>'),
    (".ctl.tl input{width:90px;accent-color:var(--ink)}",
     ".ctl.tl input{width:90px;accent-color:var(--ink)}\n"
     "#walkBar .hint{color:var(--ink-3)}\n"
     "#walkBar button{height:26px}\n"
     "@media (max-width:760px){#walkBar .hint{display:none}#walkBar button{height:32px;min-width:34px}}"),

    # ---- #debug&walk opens in the walk, with the camera from the hash (for captures)
    ("if (HASH.photo && PH[+HASH.photo - 1]) enterPhoto(+HASH.photo - 1);",
     "if (HASH.photo && PH[+HASH.photo - 1]) enterPhoto(+HASH.photo - 1);\n"
     "if (HASH.walk){ enterWalk(); ['x', 'z', 'yaw', 'pitch', 'eye', 'fov'].forEach(function(k){ if (HASH['w' + k] != null) WALK[k] = +HASH['w' + k]; }); dirty3 = true; }"),
    ("enterPhoto: enterPhoto, exitPhoto: exitPhoto,",
     "enterPhoto: enterPhoto, exitPhoto: exitPhoto, walk: {enter: enterWalk, exit: exitWalk, state: WALK, cam: walkCam},"),

    # ---- #debug&photo=N&bare&over=0.5: the same bare frame with the photo laid back over it, for tuning a camera
    ("$('#phOp').value = 0; $('#photo').style.opacity = 0; sizeModel(); } }",
     "$('#phOp').value = 0; $('#photo').style.opacity = 0; sizeModel();\n"
     "    if (HASH.over != null){ $('#phOp').value = HASH.over; $('#photo').style.opacity = HASH.over; } } }"),

    # ---------------------------------------------------------------- finishes
    ("else m = stdMat({roughness: 0.5});   /* paint */",
     "else if (kind === 'peg') m = stdMat({map: PEGT, roughness: 0.72});\n"
     "  else m = stdMat({roughness: 0.5});   /* paint */"),
    ("var CLAY = canvasTex(128, 128, 6, 6,",
     "var PEGT = canvasTex(96, 96, 3, 3, function(g, W, H){ var i, j; g.fillStyle = grey(226); g.fillRect(0, 0, W, H);   /* hardboard, holes an inch apart */\n"
     "  for (i = 0; i < 3; i++) for (j = 0; j < 3; j++){ g.fillStyle = grey(96); g.beginPath(); g.arc((i + 0.5) * W / 3, (j + 0.5) * H / 3, W * 0.038, 0, 6.283); g.fill(); } });\n"
     "var CLAY = canvasTex(128, 128, 6, 6,"),

    # ---- the finish roles the new types carry
    ("function build(it){ var g = new T.Group();",
     "Object.assign(SURF, {wallshelf: ['wood', 'metal'], pegboard: ['peg', 'wood'], beanbag: ['fabric', 'fabric'], curtain: ['fabric', 'brass'],\n"
     "  sconce: ['metal', 'shade'], guitar: ['paint', 'dark'], skateboard: ['dark', 'paint']});\n"
     "Object.assign(SECOND, {wallshelf: 'Brackets', pegboard: 'Shelf and hooks', beanbag: 'Seam', curtain: 'Rod', sconce: 'Shade', guitar: 'Mount', skateboard: 'Trucks'});\n"
     "Object.assign(KINDS, {beanbag: [['fabric'], ['fabric']], curtain: [['fabric'], ['paint', 'wood']], pegboard: [['wood', 'paint'], ['wood', 'paint']],\n"
     "  wallshelf: [['wood', 'paint'], ['paint']], sconce: [['paint', 'wood'], ['paint']], guitar: [['paint', 'wood'], ['paint']], skateboard: [['paint', 'wood'], ['paint']]});\n"
     "Object.assign(TYPE_COLORS, {wallshelf: [0xcfae86, 0x3e3f3d], pegboard: [0xc9a06a, 0x8a6443], beanbag: [0x9db2c4, 0x9db2c4], curtain: [0x7f8c63, 0xb58f55],\n"
     "  sconce: [0xe6e4df, 0xf3f0ea], guitar: [0x6b4a94, 0x2b2b2b], skateboard: [0x3e3f3d, 0xd6aa98]});\n"
     "function build(it){ var g = new T.Group();"),

    # ---- MAIN is defined down in the configurator, so it takes its own edit, after it
    ("fireplace: 'Surround', media: 'Wood'};",
     "fireplace: 'Surround', media: 'Wood'};\n"
     "Object.assign(MAIN, {wallshelf: 'Boards', pegboard: 'Board', beanbag: 'Fabric', curtain: 'Fabric', sconce: 'Fitting', guitar: 'Body', skateboard: 'Deck'});"),

    # ---------------------------------------------------------------- new builders
    ("  box: function(g, it){ part(g, it.w, it.h || 30, it.d, 0, 0, 0, 1); }",
     r"""  wallshelf: function(g, it){ /* one floating board on small brackets, or several between two end panels */
    var w = it.w, d = it.d || 9, y0 = it.mount || 48, n = Math.max(1, it.shelves || 1), t = 1.25, span = Math.max(0, (it.h || t) - t), gp = n > 1 ? span / (n - 1) : 0;
    for (var i = 0; i < n; i++){ var y = y0 + gp * i; part(g, n > 1 ? w - 2 : w, t, d, 0, y, 0, 1, {r: 0.2});
      if (n === 1) [-1, 1].forEach(function(s){ part(g, 0.9, 2.6, d - 2, s * (w / 2 - 2.5), y - 2.6, -0.5, 2, {edge: false, noShadow: true}); }); }
    if (n > 1) [-1, 1].forEach(function(s){ part(g, 1, span + t, d, s * (w / 2 - 0.5), y0, 0, 1); }); },
  pegboard: function(g, it){ /* a perforated board, a row of pegs and a small shelf on two of them */
    var w = it.w, h = it.h, d = it.d || 3, y = it.mount || 40, z0 = -d / 2, n = Math.max(3, Math.round(w / 7)), r = rnd(Math.round(w * 7 + h));
    part(g, w, h, 0.7, 0, y, z0 + 0.35, 1, {kind: 'peg', edge: 0.4});
    for (var i = 0; i < n; i++){ var x = -w / 2 + (i + 0.5) * w / n, c = cyl(g, 0.22, 0.22, 2.1, x, y + h * (0.34 + r() * 0.52) - 1.05, z0 + 1.75, 2, {seg: 10, noShadow: true}); c.rotation.x = Math.PI / 2; }
    part(g, w * 0.44, 0.8, Math.max(2.5, d - 1.2), -w * 0.2, y + h * 0.15, z0 + 0.7 + Math.max(2.5, d - 1.2) / 2, 2, {r: 0.2}); },
  beanbag: function(g, it){ /* a slumped bag: a wide seat and a smaller back resting on it */
    var w = it.w, d = it.d || it.w, h = it.h || 26;
    function blob(sx, sy, sz, x, y, z, role){ var m = new T.Mesh(new T.SphereGeometry(1, 28, 18), WM); m.scale.set(sx, sy, sz); m.position.set(x, y, z);
      m.castShadow = m.receiveShadow = true; m.userData.role = role; g.add(m); return m; }
    blob(w / 2, h * 0.42, d / 2, 0, h * 0.42, 0, 1); blob(w * 0.35, h * 0.4, d * 0.3, 0, h * 0.6, -d * 0.19, 1);
    blob(w * 0.26, h * 0.1, d * 0.26, 0, h * 0.8, d * 0.05, 2); },
  curtain: function(g, it){ /* a pleated panel on a rod */
    var w = it.w, d = it.d || 7, h = it.h || 84, y = it.mount || 0, n = Math.max(3, Math.round(w / 5)), pw = w / n * 1.35, r = rnd(Math.round(w * 3 + h));
    for (var i = 0; i < n; i++){ var x = -w / 2 + (i + 0.5) * w / n, fd = pw * (0.75 + r() * 0.4);
      cyl(g, fd / 2, fd / 2, h - 2.5, x, y, -d / 2 + fd / 2, 1, {seg: 14}); }
    part(g, w, 0.9, 0.9, 0, y + h - 0.9, -d / 2 + 0.45, 2, {edge: false}); },
  sconce: function(g, it){ /* a wall light: a backplate and a soft box shade with a bulb in it */
    var w = it.w, h = it.h || 6, d = it.d || 5, y = it.mount || 72, z0 = -d / 2;
    part(g, w * 0.34, h * 0.8, 0.7, 0, y + h * 0.1, z0 + 0.35, 1, {r: 0.2});
    part(g, w, h, d - 0.7, 0, y, z0 + 0.7 + (d - 0.7) / 2, 2, {r: Math.min(1.2, h / 3), kind: 'shade', noShadow: true}); },
  guitar: function(g, it){ /* a hollow body on a wall mount: two bouts, a neck and a head */
    var w = it.w, h = it.h || 40, d = it.d || 5, y = it.mount || 38, z0 = -d / 2, th = Math.min(3, d - 1.8), r = w / 2, bt = y + r + w * 0.38 + 0.84 * r;
    part(g, w * 0.82, 2.6, 1.4, 0, y + w * 0.96, z0 + 0.7, 2, {r: 0.4});
    [[y + r, r], [y + r + w * 0.38, r * 0.84]].forEach(function(b){ var c = cyl(g, b[1], b[1], th, 0, b[0] - th / 2, z0 + 1.2 + th / 2, 1, {seg: 30}); c.rotation.x = Math.PI / 2; });
    part(g, 2.2, Math.max(2, h - 4.4 - (bt - y)), th * 0.8, 0, bt, z0 + 1.3, 1, {r: 0.3});
    part(g, 3.2, 4.4, th * 0.7, 0, y + h - 4.4, z0 + 1.3, 2, {r: 0.4}); },
  skateboard: function(g, it){ /* a deck stood on its tail against the wall */
    var w = it.w || 9, h = it.h || 32, d = it.d || 10, lean = 0.22, cs = Math.cos(lean), sn = Math.sin(lean), t = 0.7;
    var m = part(g, w, h, t, 0, (h * cs + t * sn) / 2 - h / 2, -d / 2 + (h * sn + t * cs) / 2, 1, {r: 1.4}); m.rotation.x = -lean;
    [0.22, 0.78].forEach(function(f){ var y = h * f * cs, z = -d / 2 + (h * sn + t * cs) / 2 + (h / 2 - h * f) * sn, L = w * 0.72;
      var c = cyl(g, 0.9, 0.9, L, 0, y - L / 2, z + 1, 2, {seg: 12, noShadow: true}); c.rotation.z = Math.PI / 2; }); },
  box: function(g, it){ part(g, it.w, it.h || 30, it.d, 0, it.mount || 0, 0, 1); }"""),

    # ---- a door with closed:true is drawn shut in the wall plane (the swing checks still apply)
    ("var c = add(add(o.hinge, mul(u, o.width / 2)), mul(along, 0.9));\n"
     "      m.position.set(c[0], 0, c[1]); m.rotation.y = -Math.atan2(u[1], u[0]);",
     "var c = o.closed ? add(o.cc, mul(w.n, 1.6)) : add(add(o.hinge, mul(u, o.width / 2)), mul(along, 0.9)), lv = o.closed ? w.d : u;\n"
     "      m.position.set(c[0], 0, c[1]); m.rotation.y = -Math.atan2(lv[1], lv[0]);"),

    # ---------------------------------------------------------------- prints
    ("    else { g.fillStyle = '#f2eee6'; g.fillRect(0, 0, cw, ch);",
     r"""    else if (style === 'tapestry'){ var cx = cw * 0.56, cy = ch * 0.46, R0 = Math.min(cw, ch) * 0.32, k, a, ink = c2, fld = c1;   /* a sun and a crescent moon on a night field */
      g.fillStyle = rgb(fld, 1); g.fillRect(0, 0, cw, ch);
      g.strokeStyle = rgb(ink, 1, 0.45); g.lineWidth = p * 0.1;
      for (k = 1; k <= 3; k++){ g.beginPath(); g.arc(cx, cy, R0 * (0.75 + k * 0.3), 0, 6.283); g.stroke(); }
      g.strokeStyle = rgb(ink, 1); g.lineWidth = p * 0.2;
      for (k = 0; k < 28; k++){ a = k * 0.2244; g.beginPath(); g.moveTo(cx + Math.cos(a) * R0 * 0.46, cy + Math.sin(a) * R0 * 0.46);
        g.lineTo(cx + Math.cos(a) * R0 * (k % 2 ? 0.63 : 0.78), cy + Math.sin(a) * R0 * (k % 2 ? 0.63 : 0.78)); g.stroke(); }
      g.fillStyle = rgb(ink, 1); g.beginPath(); g.arc(cx, cy, R0 * 0.42, 0, 6.283); g.fill();
      var mx = cw * 0.3; g.beginPath(); g.arc(mx, cy, R0 * 0.52, 0, 6.283); g.fill();
      g.fillStyle = rgb(fld, 1); g.beginPath(); g.arc(mx + R0 * 0.25, cy, R0 * 0.52, 0, 6.283); g.fill();
      g.fillStyle = rgb(ink, 1); for (k = 0; k < 90; k++){ var sx = r() * cw, sy = r() * ch; if (Math.hypot(sx - cx, sy - cy) < R0 * 1.1) continue;
        g.beginPath(); g.arc(sx, sy, p * (0.05 + r() * 0.12), 0, 6.283); g.fill(); } }
    else if (style === 'board'){ g.fillStyle = '#f8f8f6'; g.fillRect(0, 0, cw, ch); g.strokeStyle = rgb(c2, 0.8, 0.8); g.lineWidth = p * 0.09; g.lineCap = 'round';   /* a whiteboard someone has doodled on */
      for (var b = 0; b < 16; b++){ var x0 = cw * (0.08 + r() * 0.8), y0 = ch * (0.14 + r() * 0.7), s = Math.min(cw, ch) * (0.035 + r() * 0.045);
        g.beginPath(); g.arc(x0, y0, s, r() * 3, 2.4 + r() * 3.4); g.stroke();
        g.beginPath(); g.moveTo(x0 - s * 0.8, y0 + s); g.lineTo(x0 + s * (0.3 + r()), y0 + s * (1.1 + r() * 0.5)); g.stroke(); } }
    else { g.fillStyle = '#f2eee6'; g.fillRect(0, 0, cw, ch);"""),
    ("mm = mir ? 0 : Math.min(w, h) * (it.print === 'poster' ? 0.04 : 0.12), z = -d / 2;",
     "mm = mir ? 0 : Math.min(w, h) * (/^(poster|tapestry|board)$/.test(it.print) ? 0.03 : 0.12), z = -d / 2;"),
    ("var mm = Math.min(it.w, it.h) * (it.print === 'poster' ? 0.04 : 0.12);",
     "var mm = Math.min(it.w, it.h) * (/^(poster|tapestry|board)$/.test(it.print) ? 0.03 : 0.12);"),

    # ---------------------------------------------------------------- the ceiling fan, shown with the ceiling
    ("function paintRoom(){ var col = LOOK === 'colour';",
     r"""var FAN = (function(){ var f = R.fan; if (!f) return null; /* a ceiling fan: it hangs from the slab and shows whenever the ceiling does */
  var g = new T.Group(), n = f.blades || 3, drop = f.drop || 12, hub = RH - drop, span = f.span || 48, bl = span / 2 - 3.5;
  function m(geo, x, y, z, ry){ var o = new T.Mesh(geo, WM); o.position.set(x, y, z); if (ry) o.rotation.y = ry; o.castShadow = o.receiveShadow = true; g.add(o); return o; }
  m(new T.CylinderGeometry(1.9, 1.9, 2.6, 18), f.c[0], RH - 1.3, f.c[1]);
  m(new T.CylinderGeometry(0.55, 0.55, drop - 4.6, 10), f.c[0], RH - 2.6 - (drop - 4.6) / 2, f.c[1]);
  m(new T.CylinderGeometry(3.4, 3.4, 3.4, 22), f.c[0], hub + 1.7, f.c[1]);
  m(new T.CylinderGeometry(2.4, 3.3, 2.2, 22), f.c[0], hub - 0.7, f.c[1]);
  var geo = new T.BoxGeometry(bl, 0.34, 5.4);
  for (var i = 0; i < n; i++){ var a = i * 6.2832 / n + (f.phase || 0);
    m(geo, f.c[0] + Math.cos(a) * (bl / 2 + 3), hub + 0.7, f.c[1] + Math.sin(a) * (bl / 2 + 3), -a); }
  g.position.y = -RH; CEIL.add(g); return g; })();
function paintRoom(){ var col = LOOK === 'colour';"""),
]


def main(path):
    src = open(path).read()
    for old, new in EDITS:
        n = src.count(old)
        if n != 1:
            sys.exit('patch: anchor found %d times, expected 1:\n  %s' % (n, old[:110]))
        src = src.replace(old, new, 1)
    open(path, 'w').write(src)
    print('patched', path, len(src), 'bytes,', len(EDITS), 'edits')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
