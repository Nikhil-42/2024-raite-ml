from ultralytics import YOLO
import argparse

import ultralytics
import ultralytics.utils
import ultralytics.utils.autobatch


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='yolo11n.pt', help='Initial weights or yaml path')
parser.add_argument('--data', type=str, default='drone_dataset', help='Name of the folder with a data.yaml file')
parser.add_argument('--overwrite', type=bool)
parser.add_argument('--epochs', type=int, default=200)
parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=640, help='train image size')

args = parser.parse_args()

# Load a model
# model = YOLO("yolov5n.yaml")  # build a new model from YAML
model = YOLO(args.model)  # load a pretrained model (recommended for training)
# model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data=f"{args.data}/data.yaml", batch=-1, epochs=args.epochs, imgsz=args.imgsz, cache=True, save_period=20, workers=8)
