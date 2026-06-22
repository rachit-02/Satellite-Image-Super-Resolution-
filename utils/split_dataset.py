import os
import random
import shutil


def is_image_file(filename):
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))


def split_dataset(input_dir, output_dir, train_ratio=0.7, val_ratio=0.2):
    classes = os.listdir(input_dir)

    for cls in classes:
        cls_path = os.path.join(input_dir, cls)
        if not os.path.isdir(cls_path):
            continue

        images = [f for f in os.listdir(cls_path) if is_image_file(f)]
        random.shuffle(images)

        n = len(images)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:]
        }

        for split, files in splits.items():
            for file in files:
                src = os.path.join(cls_path, file)
                dst = os.path.join(output_dir, split, "HR", cls, file)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(src, dst)