import argparse
import pathlib

# Example usage
# python ingest_to_yolo.py data/\[01\]\ Training\ Only/20241021_RAITE_pumba/ data/ugv_dataset_v7/train/ --prefix 20241021_RAITE_pumba --class_id 6
# python ingest_to_yolo.py data/\[01\]\ Training\ Only/20241021_RAITE_spot/ data/ugv_dataset_v7/train/ --prefix 20241021_RAITE_spot --class_id 4
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument("--class_id", type=int, default=None)
    parser.add_argument("--prefix", type=str)
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
        
        output_image_path = output_data / "images" / new_name
        output_label_path = (output_data / "labels" / new_name).with_suffix('.txt')
        print("\tCopying Image to", output_image_path)
        output_image_path.write_bytes(image_path.read_bytes())

        print("\tCopying Label to", output_label_path)
        
        new_bounding_boxes = ""
        for line in label_path.read_text().splitlines():
            class_id, x_center, y_center, width, height = line.split()
            class_id = args.class_id if args.class_id is not None else class_id
            new_bounding_boxes = f"{class_id} {x_center} {y_center} {width} {height}\n"
        
        output_label_path.write_text(new_bounding_boxes)
    