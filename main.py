import cv2
import numpy as np
import torch
from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small').eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
midas.to(device)
transform = torch.hub.load('intel-isl/MiDaS', 'transforms').small_transform

cap = cv2.VideoCapture(0)
focal = 600
base_z = 1.0

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_tensor = transform(rgb).to(device)

    with torch.no_grad():
        depth = midas(input_tensor)
        depth = torch.nn.functional.interpolate(depth.unsqueeze(1), size=frame.shape[:2], mode="bicubic").squeeze()

    depth_norm = depth.cpu().numpy()
    depth_norm = cv2.normalize(depth_norm, None, 0, 1, cv2.NORM_MINMAX)

    for result in results:
        if result.masks is not None:
            for mask, box in zip(result.masks.xy, result.boxes.xyxy):
                x1, y1, x2, y2 = map(int, box)
                contour = mask.reshape((-1, 1, 2)).astype(np.int32)
                area_px = cv2.contourArea(contour)
                depth_roi = depth_norm[y1:y2, x1:x2]
                if depth_roi.size == 0: continue
                z = base_z / np.median(depth_roi)
                width_m = (x2 - x1) * z / focal
                height_m = (y2 - y1) * z / focal
                area_m = width_m * height_m

                if area_m < 0.1:
                    label, color = "Small", (0, 255, 0)
                elif area_m < 0.3:
                    label, color = "Medium", (0, 165, 255)
                else:
                    label, color = "Large", (0, 0, 255)

                cv2.polylines(frame, [contour], True, color, 2)
                cv2.putText(frame, f"{label} {area_m:.2f}m²", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('Size Measurement', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
