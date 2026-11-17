// Marks named materials as unlit (KHR_materials_unlit) so they ignore scene lighting.
// Usage: node make-unlit.mjs <in.glb> <out.glb> <materialName> [<materialName> ...]
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS, KHRMaterialsUnlit } from "@gltf-transform/extensions";

const [input, output, ...names] = process.argv.slice(2);
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(input);
const unlitExt = doc.createExtension(KHRMaterialsUnlit);
const unlit = unlitExt.createUnlit();
let n = 0;
for (const mat of doc.getRoot().listMaterials()) {
  if (names.includes(mat.getName())) {
    mat.setExtension("KHR_materials_unlit", unlit);
    console.log(`unlit: ${mat.getName()} alphaMode=${mat.getAlphaMode()} baseColor=${mat.getBaseColorFactor()}`);
    n++;
  }
}
if (!n) throw new Error("no material matched " + names.join(", "));
await io.write(output, doc);
