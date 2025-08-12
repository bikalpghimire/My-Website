from PIL import Image
import os

input_folder = "img"   # folder containing your images
output_folder = "images_webp"  # folder for converted files

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # add formats if needed
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGB")  # ensure correct format
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".webp")
        img.save(output_path, "webp", quality=80)  # adjust quality if you like
        print(f"Converted: {filename} → {output_path}")

print("✅ All images converted to WebP!")
