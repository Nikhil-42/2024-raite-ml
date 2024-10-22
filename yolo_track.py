from ultralytics import YOLO
import sys

model = YOLO(sys.argv[1])
model.track(sys.argv[2], show=True)