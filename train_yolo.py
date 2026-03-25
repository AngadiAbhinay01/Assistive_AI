from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="data/filtered_dataset/data.yaml",
    epochs=30,
    imgsz=640,
    batch=8   # since CPU
)