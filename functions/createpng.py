from PIL import Image

# Ảnh trắng 1x1 pixel
img = Image.new("RGB", (640, 360), color="white")
img.save("empty.jpg", "JPEG")