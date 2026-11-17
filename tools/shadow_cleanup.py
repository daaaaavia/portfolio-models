# shadow_cleanup.py: turns a shadow-catcher render into a clean shadow texture for the web.
# Run in Blender's Scripting tab after rendering the shadow (Film > Transparent, RGBA PNG).
# - keeps only the alpha (the shadow) and makes the colour pure black
# - fades the alpha to zero toward the edges so the square plane never shows
# Then use the saved image on the shadow plane's material (Alpha output -> Principled Alpha).

import bpy
import numpy as np

# ===== SETTINGS: change these =====
RAW = r"C:\Users\Admin\OneDrive\Portfolio Remake\web-export\shadow_raw.png"   # shadow-catcher render (RGBA PNG)
OUT = r"C:\Users\Admin\OneDrive\Portfolio Remake\web-export\chair_shadow.png"  # cleaned texture to save
IMAGE_NAME = "chair_shadow"  # name of the image inside Blender
FADE_START = 0.70  # fraction of the way from centre to edge where the fade begins (0 to 1)
FADE_END = 0.98    # fraction where the shadow is fully gone (0 to 1)
# ===== END SETTINGS =====

src = bpy.data.images.load(RAW, check_existing=False)
w, h = src.size
px = np.empty(w * h * 4, dtype=np.float32)
src.pixels.foreach_get(px)
alpha = px.reshape(h, w, 4)[..., 3].copy()
bpy.data.images.remove(src)

# Radial fade: 1 inside FADE_START, smoothly down to 0 at FADE_END.
yy, xx = np.mgrid[0:h, 0:w]
r = np.sqrt(((xx + 0.5) / w - 0.5) ** 2 + ((yy + 0.5) / h - 0.5) ** 2) / 0.5
t = np.clip((r - FADE_START) / (FADE_END - FADE_START), 0, 1)
alpha *= 1 - t * t * (3 - 2 * t)

out = np.zeros((h, w, 4), dtype=np.float32)
out[..., 3] = alpha
img = bpy.data.images.get(IMAGE_NAME)
if img:
    bpy.data.images.remove(img)
img = bpy.data.images.new(IMAGE_NAME, w, h, alpha=True)
img.pixels.foreach_set(out.ravel())
img.filepath_raw = OUT
img.file_format = "PNG"
img.save()
print("saved", OUT, "max alpha", float(alpha.max()))
