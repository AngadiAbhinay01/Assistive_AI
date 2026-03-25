import cv2
from ultralytics import YOLO
from modules.voice_engine import speak
import time
import threading

# Load trained YOLO model
model = YOLO("best.pt")

# Class names (must match your dataset.yaml)
CLASS_NAMES = ["battery", "breadboard", "led", "jumper_wire"]

# Settings
CONF_THRESHOLD = 0.5   # Increased to avoid false detections
BOX_SIZE_THRESHOLD = 50  # Ignore small noisy detections

def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.daemon = True
    thread.start()

def start_camera():
    speak_async("Camera started. Press Q or ESC to exit camera.")
    cap = cv2.VideoCapture(0)

    last_spoken = ""
    last_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            h, w, _ = frame.shape

            # Define center region (focus area)
            cx, cy = w // 2, h // 2
            box_size = 150
            x_min, y_min = cx - box_size, cy - box_size
            x_max, y_max = cx + box_size, cy + box_size

            # Draw center guide box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Run YOLO detection
            results = model(frame, stream=True)

            VALID_DETECTION = False
            detected_label = ""

            for r in results:
                if r.boxes is None:
                    continue

                for box in r.boxes:
                    conf = float(box.conf[0])

                    # ❌ Skip low confidence
                    if conf < CONF_THRESHOLD:
                        continue

                    cls_id = int(box.cls[0])
                    label = CLASS_NAMES[cls_id]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # ❌ Skip very small detections (noise)
                    box_width = x2 - x1
                    box_height = y2 - y1
                    if box_width < BOX_SIZE_THRESHOLD or box_height < BOX_SIZE_THRESHOLD:
                        continue

                    # Center of detected object
                    obj_cx = (x1 + x2) // 2
                    obj_cy = (y1 + y2) // 2

                    # ❌ Skip if not in center region
                    if not (x_min < obj_cx < x_max and y_min < obj_cy < y_max):
                        continue

                    # ✅ Valid detection
                    VALID_DETECTION = True
                    detected_label = label

                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}",
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2)

            current_time = time.time()

            # 🎯 SPEAK LOGIC
            if VALID_DETECTION:
                if detected_label != last_spoken or (current_time - last_time > 2):
                    speak_async(detected_label)
                    last_spoken = detected_label
                    last_time = current_time
            else:
                # No valid detection → say unknown
                if (current_time - last_time) > 3:
                    speak_async("Unknown object")
                    last_spoken = ""
                    last_time = current_time

            # Show frame
            cv2.imshow("Camera - Press Q or ESC to exit", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

            time.sleep(0.05)

    finally:
        cap.release()
        cv2.destroyAllWindows()
        speak_async("Camera closed")