from utils.dataloader import get_dataloader


print("🔍 Testing TRAIN loader...")
train_loader = get_dataloader("train", batch_size=2)

for lr, hr in train_loader:
    print("TRAIN LR:", lr.shape, lr.dtype)
    print("TRAIN HR:", hr.shape, hr.dtype)
    break


print("\n🔍 Testing TEST loader...")
test_loader = get_dataloader("test", batch_size=2)

for lr, hr in test_loader:
    print("TEST LR:", lr.shape, lr.dtype)
    print("TEST HR:", hr.shape, hr.dtype)
    break


print("\n✅ Dataloader working correctly")