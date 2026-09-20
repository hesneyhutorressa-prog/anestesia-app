from PIL import Image
import numpy as np

img = Image.open("app/static/img/logo.png").convert("RGBA")
data = np.array(img)

r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3

alpha_new = np.clip((brightness - 10) / 50 * 255, 0, 255).astype(np.uint8)
data[:,:,3] = np.minimum(a, alpha_new)

out = Image.fromarray(data, "RGBA")
out.save("app/static/img/logo_watermark.png")
print("Listo: app/static/img/logo_watermark.png")