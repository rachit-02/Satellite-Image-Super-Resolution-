import torch
import torch.nn as nn
import torch.optim as optim
import os
import traceback
import requests
import argparse

from models.cga import CGA
from utils.dataloader import get_dataloader
from configs.config_150 import Config


# ================= TELEGRAM CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")


def send_telegram(msg):
    if BOT_TOKEN == "" or CHAT_ID == "":
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)


# ================= ARGUMENTS =================
parser = argparse.ArgumentParser()
parser.add_argument("--resume", type=str, default=None)
parser.add_argument("--exp-name", type=str, default="run_150_epochs")
args = parser.parse_args()


# ================= SAFE SAVE =================
def safe_save(state, path):
    temp_path = path + ".tmp"
    torch.save(state, temp_path)
    os.replace(temp_path, path)


# ================= TRAINING =================
def train():
    print("========== TRAINING STARTED ==========", flush=True)

    device = Config.device
    print(f"Using device: {device}", flush=True)
    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}", flush=True)

    send_telegram("Training Started")

    # ================= PATHS =================
    exp_dir = os.path.join("experiments", args.exp_name)
    checkpoints_dir = os.path.join(exp_dir, "checkpoints")
    logs_dir = os.path.join(exp_dir, "logs")

    os.makedirs(checkpoints_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    print(f"Experiment directory: {exp_dir}", flush=True)

    # ================= MODEL =================
    model = CGA().to(device)

    # ================= DATA =================
    train_loader = get_dataloader("train", batch_size=Config.batch_size)

    if len(train_loader) == 0:
        raise RuntimeError("Dataloader is empty!")

    # ================= LOSS + OPT =================
    criterion = nn.L1Loss().to(device)
    optimizer = optim.Adam(model.parameters(), lr=Config.lr)

    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    # ================= RESUME =================
    best_loss = float("inf")
    start_epoch = 0

    checkpoint_path = os.path.join(checkpoints_dir, "last_model.pth")

    # Priority: user resume path > auto checkpoint
    if args.resume is not None:
        checkpoint_path = args.resume

    if os.path.exists(checkpoint_path):
        print(f"[INFO] Loading checkpoint: {checkpoint_path}", flush=True)

        checkpoint = torch.load(checkpoint_path, map_location=device)

        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])

        start_epoch = checkpoint.get("epoch", -1) + 1
        best_loss = checkpoint.get("best_loss", best_loss)

        print(f"[INFO] Resuming from epoch {start_epoch}", flush=True)
        send_telegram(f"Resumed from epoch {start_epoch}")

    else:
        print("[INFO] No checkpoint found. Starting fresh training.", flush=True)

    # ================= TRAIN LOOP =================
    try:
        for epoch in range(start_epoch, Config.epochs):
            model.train()
            total_loss = 0.0

            print(f"\n----- Epoch {epoch+1}/{Config.epochs} -----", flush=True)

            for batch_idx, (lr, hr) in enumerate(train_loader):
                try:
                    lr = lr.to(device, non_blocking=True)
                    hr = hr.to(device, non_blocking=True)

                    optimizer.zero_grad(set_to_none=True)

                    with torch.amp.autocast(device_type=device.type, enabled=use_amp):
                        sr = model(lr)
                        loss = criterion(sr, hr)

                    if torch.isnan(loss):
                        print(f"[WARNING] NaN loss at batch {batch_idx}, skipping...", flush=True)
                        continue

                    scaler.scale(loss).backward()

                    # Gradient clipping (stability)
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

                    scaler.step(optimizer)
                    scaler.update()

                    total_loss += loss.item()

                except Exception as batch_error:
                    print(f"[ERROR] Skipping batch {batch_idx}: {batch_error}", flush=True)
                    continue

            avg_loss = total_loss / len(train_loader)

            msg = f"Epoch {epoch+1}/{Config.epochs} | Loss: {avg_loss:.6f}"
            print(msg, flush=True)
            send_telegram(msg)

            # ================= BEST MODEL =================
            if avg_loss < best_loss:
                best_loss = avg_loss
                best_path = os.path.join(checkpoints_dir, "best_model.pth")
                torch.save(model.state_dict(), best_path)

                print("[INFO] Best model updated", flush=True)
                send_telegram(f"Best Model Saved | Loss: {avg_loss:.6f}")

            # ================= SAVE CHECKPOINT =================
            safe_save({
                "epoch": epoch,
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "best_loss": best_loss
            }, os.path.join(checkpoints_dir, "last_model.pth"))

        print("\n========== TRAINING FINISHED ==========", flush=True)
        send_telegram("Training Finished Successfully")

        with open(os.path.join(exp_dir, "training_done.txt"), "w") as f:
            f.write("done")

    except Exception as e:
        error_msg = f"[FATAL ERROR] {str(e)}"
        print(error_msg, flush=True)
        traceback.print_exc()
        send_telegram(error_msg)


# ================= MAIN =================
if __name__ == "__main__":
    train()