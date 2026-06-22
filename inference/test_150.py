import os
import torch
import cv2
import numpy as np
import sys
import glob
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.cga import CGA
from utils.dataloader import get_dataloader
from utils.metrics import psnr, ssim
from configs.config_150 import Config


# ================= ARGUMENTS =================
parser = argparse.ArgumentParser()
parser.add_argument("--exp-name", type=str, default="run_150_epochs")
parser.add_argument("--model-path", type=str, default=None)
args = parser.parse_args()


# ================= UTILS =================
def tensor_to_image(t):
    t = t.squeeze(0).permute(1, 2, 0).cpu().numpy()
    t = np.clip(t, 0, 1)
    return (t * 255).astype("uint8")


def get_model_path():
    exp_checkpoint_dir = os.path.join("experiments", args.exp_name, "checkpoints")

    if args.model_path and os.path.exists(args.model_path):
        return args.model_path

    exp_best_path = os.path.join(exp_checkpoint_dir, "best_model.pth")
    exp_last_path = os.path.join(exp_checkpoint_dir, "last_model.pth")

    if os.path.exists(exp_best_path):
        return exp_best_path

    if os.path.exists(exp_last_path):
        print("Using last_model.pth instead", flush=True)
        return exp_last_path

    print("ERROR: No model file found!", flush=True)
    sys.exit(1)


# ================= LOAD MODEL =================
def load_model(device):
    print("Loading model...", flush=True)

    model = CGA().to(device)

    model_path = get_model_path()
    print(f"Using model: {model_path}", flush=True)

    checkpoint = torch.load(model_path, map_location=device)

    # 🔥 FIXED LOADING LOGIC
    if isinstance(checkpoint, dict):
        if "model" in checkpoint:
            model.load_state_dict(checkpoint["model"])
        elif "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
        else:
            model.load_state_dict(checkpoint)
    else:
        model.load_state_dict(checkpoint)

    print("Model loaded successfully", flush=True)
    model.eval()
    return model


# ================= TEST =================
def test():
    try:
        device = Config.device if torch.cuda.is_available() else torch.device("cpu")

        print(f"Running inference on: {device}", flush=True)
        if device.type == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}", flush=True)

        model = load_model(device)

        print("Creating dataloader...", flush=True)
        test_loader = get_dataloader("test", batch_size=1)

        try:
            length = len(test_loader)
            print(f"Test samples: {length}", flush=True)
        except:
            length = 0

        if length == 0:
            print("ERROR: Test dataloader is empty", flush=True)
            return

        # ================= SAVE DIR =================
        results_root = os.path.join("experiments", args.exp_name, "results")

        lr_dir = os.path.join(results_root, "lr")
        sr_dir = os.path.join(results_root, "sr")
        hr_dir = os.path.join(results_root, "hr")
        compare_dir = os.path.join(results_root, "compare")

        os.makedirs(lr_dir, exist_ok=True)
        os.makedirs(sr_dir, exist_ok=True)
        os.makedirs(hr_dir, exist_ok=True)
        os.makedirs(compare_dir, exist_ok=True)

        print(f"Saving results to: {results_root}", flush=True)

        total_psnr = 0
        total_ssim = 0
        count = 0

        print("\nRunning inference...\n", flush=True)

        with torch.no_grad():
            for i, (lr, hr) in enumerate(test_loader):
                lr = lr.to(device)
                hr = hr.to(device)

                sr = model(lr)

                sr = sr.clamp(0, 1)
                hr = hr.clamp(0, 1)

                # Convert to numpy
                sr_np = (sr.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
                hr_np = (hr.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)

                # Metrics
                p = psnr(sr_np, hr_np)
                s = ssim(sr_np, hr_np)

                total_psnr += p
                total_ssim += s
                count += 1

                print(f"[{i}] PSNR: {p:.2f}, SSIM: {s:.4f}", flush=True)

                # Save images (first 50 only)
                if i < 50:
                    lr_img = tensor_to_image(lr)
                    sr_img = tensor_to_image(sr)
                    hr_img = tensor_to_image(hr)

                    cv2.imwrite(os.path.join(lr_dir, f"{i:04d}.png"), cv2.cvtColor(lr_img, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(os.path.join(sr_dir, f"{i:04d}.png"), cv2.cvtColor(sr_img, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(os.path.join(hr_dir, f"{i:04d}.png"), cv2.cvtColor(hr_img, cv2.COLOR_RGB2BGR))

                    # Compare image
                    h, w = sr_img.shape[:2]
                    lr_resized = cv2.resize(lr_img, (w, h), interpolation=cv2.INTER_CUBIC)
                    combined = np.hstack([lr_resized, sr_img, hr_img])

                    cv2.imwrite(
                        os.path.join(compare_dir, f"{i:04d}.png"),
                        cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)
                    )

        # ================= FINAL METRICS =================
        if count > 0:
            avg_psnr = total_psnr / count
            avg_ssim = total_ssim / count

            print("\n========================", flush=True)
            print(f"Average PSNR: {avg_psnr:.2f}", flush=True)
            print(f"Average SSIM: {avg_ssim:.4f}", flush=True)
            print("========================", flush=True)
        else:
            print("No samples processed.", flush=True)

    except Exception as e:
        print("FATAL ERROR:", str(e), flush=True)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test()