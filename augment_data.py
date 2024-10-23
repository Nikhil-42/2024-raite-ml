import numpy as np
import argparse
import pathlib
import random
import cv2

def blur(image, bboxes):
    return cv2.blur(image, (2 * random.randint(1, 4) + 1, 2 * random.randint(1, 4) + 1)), bboxes

def brightness(image, bboxes):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    value = random.randint(0, 25)#whatever value you want to add
    hsv[:,:,2] = cv2.add(hsv[:,:,2], value)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image, bboxes

def exposure(image, bboxes):
    # Adjust brightness and contrast
    alpha = random.random() + 1.0  # Contrast control (1.0 for original)
    beta = random.random() * 30   # Brightness control (0 for original)
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta), bboxes

def speckle_noise(image, bboxes):
    np.random.seed(random.random())
    rands = np.random.random((*image.shape[:-1], 1))
    image *= (1 - (rands > 0.975))
    image = cv2.add(image, (rands < 0.025) * 255)
    return image, bboxes

def guassian_noise(image, bboxes):
    pass

def greyscale(image, bboxes):
    pass

def cutout(image, bboxes): 
    x, y, w, h = (random.random() for _ in range(4))

    while any(
        x < (x_center - width / 2) and
        y < (y_center - height / 2) and
        x+w > (x_center + width / 2) and
        y+h > (y_center + height / 2) 
            for _, x_center, y_center, width, height in bboxes
    ):
        x, y, w, h = (random.random() for _ in range(4))

    height, width, _ = image.shape

    image = cv2.rectangle(image, (int(x * width), int(y * height)), (int((x + w) * width), int((y + h) * height)), (0, 0, 0), -1)
    return image, bboxes

if __name__ == "__main__":
    import os
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument('--multiplicity', type=int, default=1)
    parser.add_argument('--blur', action='store_true')
    parser.add_argument('--brightness', action='store_true')
    parser.add_argument('--exposure', action='store_true')
    parser.add_argument('--speckle_noise', action='store_true')
    parser.add_argument('--cutout', action='store_true')
    args = parser.parse_args()

    input_data: pathlib.Path = args.input
    output_data: pathlib.Path = args.output
    assert (input_data / "labels").exists()

    for image_path in (input_data).glob("*.*"):
        new_name = f"{args.prefix}_{image_path.name}"
        
        label_path = input_data / "labels" / image_path.with_suffix('.txt').name
        print(f"Image: {image_path}")
        print(f"Label: {label_path}")
        if not label_path.exists():
            print("\tMissing Label")
        if not image_path.exists():
            print("\tMissing Image")

        if not label_path.exists() or not image_path.exists():
            continue
        
        bboxes = [
            tuple(
                (int(line.split()[0]), *(float(x) for x in line.split()[1:]))
            ) for line in label_path.read_text().splitlines()
        ]
        output_image_path = output_data / "images" / new_name
        output_label_path = (output_data / "labels" / new_name).with_suffix('.txt')
        print("\tCopying Image to", output_image_path)
        output_image_path.write_bytes(image_path.read_bytes())

        print("\tCopying Label to", output_label_path)
        
        new_bounding_boxes = ""
        for line in label_path.read_text().splitlines():
            class_id, x_center, y_center, width, height = line.split()
            if args.class_id is not None:
                class_id = args.class_id
            elif args.class_map is not None:
                class_id = args.class_map[int(class_id)]
            new_bounding_boxes = f"{class_id} {x_center} {y_center} {width} {height}\n"
        
        output_label_path.write_text(new_bounding_boxes)
    
    
    

    