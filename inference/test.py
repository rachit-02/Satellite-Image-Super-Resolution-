import os
import torch
import cv2
import numpy as np
import sys
import glob
import json
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.cga import CGA
from utils.dataloader import get_dataloader
from utils.metrics import psnr, ssim


def tensor_to_image(t):
    t = t.squeeze(0).permute(1, 2, 0).cpu().numpy()
    t = np.clip(t, 0, 1)
    return (t * 255).astype("uint8")


# ✅ MODEL FINDER
def get_model_path():
    if os.path.exists("checkpoints/best_model.pth"):
        return "checkpoints/best_model.pth"

    if os.path.exists("checkpoints/last_model.pth"):
        print("⚠️ Using last_model.pth instead", flush=True)
        return "checkpoints/last_model.pth"

    paths = glob.glob("experiments/*/checkpoints/best_model.pth")
    if len(paths) > 0:
        return paths[0]

    print("❌ ERROR: No model file found!", flush=True)
    sys.exit(1)


def load_model(device):
    print("🔍 Loading model...", flush=True)

    model = CGA().to(device)

    model_path = get_model_path()
    print(f"📂 Using model: {model_path}", flush=True)

    checkpoint = torch.load(model_path, map_location=device)

    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    print("✅ Model loaded", flush=True)
    model.eval()
    return model


def test():
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print(f"🚀 Running inference on: {device}", flush=True)
        if device.type == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}", flush=True)

        model = load_model(device)

        print("🔍 Creating dataloader...", flush=True)
        test_loader = get_dataloader("test", batch_size=1)

        print("DEBUG: Dataloader created", flush=True)

        try:
            length = len(test_loader)
            print("Length of test_loader:", length, flush=True)
        except Exception as e:
            print("❌ Could not get length:", e, flush=True)
            length = 0

        if length == 0:
            print("❌ ERROR: Dataloader is empty", flush=True)
            return

        os.makedirs("results/lr", exist_ok=True)
        os.makedirs("results/sr", exist_ok=True)
        os.makedirs("results/hr", exist_ok=True)
        os.makedirs("results/compare", exist_ok=True)

        total_psnr = 0
        total_ssim = 0
        count = 0

        print("\n🔍 Running inference...\n", flush=True)

        with torch.no_grad():
            for i, (lr, hr) in enumerate(test_loader):
                count += 1

                lr = lr.to(device)
                hr = hr.to(device)

                sr = model(lr)

                sr = sr.clamp(0, 1)
                hr = hr.clamp(0, 1)

                # Metrics
                sr_np = (sr.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
                hr_np = (hr.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).clip(0, 255).astype(np.uint8)

                p = psnr(sr_np, hr_np)
                s = ssim(sr_np, hr_np)

                total_psnr += p
                total_ssim += s

                print(f"[{i}] PSNR: {p:.2f}, SSIM: {s:.4f}", flush=True)

                lr_img = tensor_to_image(lr)
                sr_img = tensor_to_image(sr)
                hr_img = tensor_to_image(hr)

                if i < 50:
                    cv2.imwrite(f"results/lr/lr_{i:04d}.png", cv2.cvtColor(lr_img, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(f"results/sr/sr_{i:04d}.png", cv2.cvtColor(sr_img, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(f"results/hr/hr_{i:04d}.png", cv2.cvtColor(hr_img, cv2.COLOR_RGB2BGR))

                    # ✅ FIX: resize LR to match SR/HR
                    h, w = sr_img.shape[:2]
                    lr_resized = cv2.resize(lr_img, (w, h), interpolation=cv2.INTER_CUBIC)

                    combined = np.hstack([lr_resized, sr_img, hr_img])

                    cv2.imwrite(
                        f"results/compare/compare_{i:04d}.png",
                        cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)
                    )

        avg_psnr = total_psnr / count
        avg_ssim = total_ssim / count

        print("\n========================", flush=True)
        print(f"Average PSNR: {avg_psnr:.2f}", flush=True)
        print(f"Average SSIM: {avg_ssim:.4f}", flush=True)
        print("========================", flush=True)

        # Save metrics to JSON for dashboard
        import json
        metrics = {
            'psnr': float(round(avg_psnr, 2)),
            'ssim': float(round(avg_ssim, 4)),
            'total_images': int(count),
            'last_updated': str(datetime.datetime.now())
        }
        os.makedirs("results", exist_ok=True)
        with open("results/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
        print("📊 Metrics saved to results/metrics.json", flush=True)

    except Exception as e:
        print("❌ FATAL ERROR:", str(e), flush=True)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test()