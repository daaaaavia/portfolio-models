# tools

| File | Run it in | What it does |
| --- | --- | --- |
| `shadow_cleanup.py` | Blender → Scripting tab | Turns a shadow-catcher render into a clean shadow texture: black colour, alpha only, faded to zero at the edges. Paths and fade are in its settings block. |
| `make-unlit.mjs` | Node.js | Marks named materials in a GLB as unlit (`KHR_materials_unlit`), e.g. the baked shadow plane. |

`make-unlit.mjs` needs two packages, installed once in this folder:

```bash
npm install @gltf-transform/core@4.1.1 @gltf-transform/extensions@4.1.1
```

Then:

```bash
node make-unlit.mjs in.glb out.glb shadow_web
```
