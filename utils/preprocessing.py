import os
import cv2

from utils.split_dataset import split_dataset
from utils.image_utils import generate_lr_image, save_image

# CONFIG
DATASET_NAME = "UCMerced"
RAW_PATH = f"data/raw/{DATASET_NAME}/Images"
PROCESSED_PATH = f"data/processed/{DATASET_NAME}"
SCALE = 4


def generate_lr_hr():
    for split in ["train", "val", "test"]:
        hr_dir = os.path.join(PROCESSED_PATH, split, "HR")
        lr_dir = os.path.join(PROCESSED_PATH, split, "LR")

        for root, _, files in os.walk(hr_dir):
            for file in files:
                if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue

                hr_path = os.path.join(root, file)
                img = cv2.imread(hr_path)

                if img is None:
                    print(f"⚠️ Skipping corrupted: {hr_path}")
                    continue

                lr_img = generate_lr_image(img, SCALE)

                relative_path = os.path.relpath(hr_path, hr_dir)
                lr_path = os.path.join(lr_dir, relative_path)

                save_image(lr_path, lr_img)


if __name__ == "__main__":
    print("Step 1: Splitting dataset...")
    split_dataset(RAW_PATH, PROCESSED_PATH)

    print("Step 2: Generating LR images...")
    generate_lr_hr()

    print("✅ Preprocessing complete!")