from ultralytics import YOLO

model = YOLO("runs/detect/train5/weights/best.pt")

results = model("data/filtered_dataset/test/images", show=True)