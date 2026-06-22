import os
import cv2

HR_DIR = "data/processed/WHU/test/HR"
LR_DIR = "data/processed/WHU/test/LR"

os.makedirs(LR_DIR, exist_ok=True)

for img_name in os.listdir(HR_DIR):
    if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    img_path = os.path.join(HR_DIR, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"⚠️ Skipping corrupted: {img_path}")
        continue

    h, w = img.shape[:2]

    # Avoid zero size
    if h < 4 or w < 4:
        continue

    lr = cv2.resize(img, (w // 4, h // 4), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(os.path.join(LR_DIR, img_name), lr)

print("✅ WHU preprocessing done")