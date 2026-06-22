import torch


class Config:
    # Auto-select device: GPU if available, otherwise CPU.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Training
    epochs = 50
    batch_size = 8
    lr = 1e-4

    # Model
    scale = 4