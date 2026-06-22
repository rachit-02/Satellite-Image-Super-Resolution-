import os
import torch
from torch.utils.data import Dataset, DataLoader
import cv2

SCALE = 4


def is_image_file(filename):
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))


# ================= SAFE IMAGE LOADER =================
def read_image_safe(path):
    img = cv2.imread(path)
    if img is None:
        return None
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        return None
    return img


# ================= DATASET =================
class SRDataset(Dataset):
    def __init__(self, split="train"):
        self.lr_paths = []
        self.hr_paths = []

        if split in ["train", "val"]:
            base_path = f"data/raw/AID/{split}"
            lr_root = os.path.join(base_path, f"LR_x{SCALE}")
            hr_root = os.path.join(base_path, "HR")

            files = os.listdir(lr_root)
            print(f"📦 AID {split} files found: {len(files)}")

            valid_count = 0
            skipped_count = 0

            for img in files:
                if not is_image_file(img):
                    continue

                lr_path = os.path.join(lr_root, img)
                hr_path = os.path.join(hr_root, img)

                if not os.path.exists(hr_path):
                    skipped_count += 1
                    continue

                lr = read_image_safe(lr_path)
                hr = read_image_safe(hr_path)

                if lr is None or hr is None:
                    skipped_count += 1
                    continue

                # ✅ STRICT SIZE CHECK
                if hr.shape[0] != lr.shape[0] * SCALE or hr.shape[1] != lr.shape[1] * SCALE:
                    skipped_count += 1
                    continue

                self.lr_paths.append(lr_path)
                self.hr_paths.append(hr_path)
                valid_count += 1

            print(f"✅ Valid pairs: {valid_count}")
            print(f"❌ Skipped (corrupt/mismatch): {skipped_count}")

        elif split == "test":

            def add_pair(lr_path, hr_path):
                if not os.path.exists(hr_path):
                    return

                lr = read_image_safe(lr_path)
                hr = read_image_safe(hr_path)

                if lr is None or hr is None:
                    return

                self.lr_paths.append(lr_path)
                self.hr_paths.append(hr_path)

            # ---------- AID ----------
            base_path = "data/raw/AID/test"
            lr_root = os.path.join(base_path, f"LR_x{SCALE}")
            hr_root = os.path.join(base_path, "HR")

            for img in os.listdir(lr_root):
                if is_image_file(img):
                    add_pair(os.path.join(lr_root, img),
                             os.path.join(hr_root, img))

            # ---------- UCMerced ----------
            base_path = "data/processed/UCMerced/test"
            lr_root = os.path.join(base_path, "LR")
            hr_root = os.path.join(base_path, "HR")

            for cls in os.listdir(lr_root):
                lr_cls = os.path.join(lr_root, cls)
                hr_cls = os.path.join(hr_root, cls)

                if not os.path.isdir(lr_cls):
                    continue

                for img in os.listdir(lr_cls):
                    if is_image_file(img):
                        add_pair(os.path.join(lr_cls, img),
                                 os.path.join(hr_cls, img))

            # ---------- WHU ----------
            base_path = "data/processed/WHU/test"
            lr_root = os.path.join(base_path, "LR")
            hr_root = os.path.join(base_path, "HR")

            for img in os.listdir(lr_root):
                if is_image_file(img):
                    add_pair(os.path.join(lr_root, img),
                             os.path.join(hr_root, img))

            print(f"🧪 Total TEST samples: {len(self.lr_paths)}")

        print(f"📊 Final dataset size: {len(self.lr_paths)}")

    def __len__(self):
        return len(self.lr_paths)

    def __getitem__(self, idx):
        lr_path = self.lr_paths[idx]
        hr_path = self.hr_paths[idx]

        lr = read_image_safe(lr_path)
        hr = read_image_safe(hr_path)

        # ✅ HARD FAILSAFE (no recursion loop)
        if lr is None or hr is None:
            new_idx = (idx + 1) % len(self.lr_paths)
            lr_path = self.lr_paths[new_idx]
            hr_path = self.hr_paths[new_idx]

            lr = read_image_safe(lr_path)
            hr = read_image_safe(hr_path)

            if lr is None or hr is None:
                raise RuntimeError("Too many corrupted images in dataset")

        # Normalize
        lr = lr.astype("float32") / 255.0
        hr = hr.astype("float32") / 255.0

        lr = torch.from_numpy(lr).permute(2, 0, 1)
        hr = torch.from_numpy(hr).permute(2, 0, 1)

        return lr, hr


# ================= DATALOADER =================
def get_dataloader(split="train", batch_size=8):
    dataset = SRDataset(split)

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(split == "train"),
        num_workers=4,
        pin_memory=True,
        persistent_workers=True
    )