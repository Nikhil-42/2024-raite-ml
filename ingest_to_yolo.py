import argparse
import pathlib
import re

# Example usage
# python ingest_to_yolo.py data/\[01\]\ Training\ Only/20241021_RAITE_pumba/ data/ugv_dataset_v7/train/ --prefix 20241021_RAITE_pumba --class_id 6
# python ingest_to_yolo.py data/\[01\]\ Training\ Only/20241021_RAITE_spot/ data/ugv_dataset_v7/train/ --prefix 20241021_RAITE_spot --class_map {2: 4}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument("--filter", type=re.compile, help="A regex to filter filenames", default=re.compile('.*'))

    class_id_args = parser.add_mutually_exclusive_group()
    class_id_args.add_argument("--class_id", type=int, default=None)
    class_id_args.add_argument("--class_map", type=eval, default=None)

    parser.add_argument("--prefix", type=str)
    args = parser.parse_args()
    
    input_data: pathlib.Path = args.input
    output_data: pathlib.Path = args.output
    label_input_data = input_data # pathlib.Path('/blue/jshin2/iyer.nikhil/_ugv_dataset_v8/train')
    assert (label_input_data / "labels").exists()
    for image_path in (input_data / "images").glob("*.*"):
        if re.fullmatch(args.filter, image_path.name) is None:
            print("Ignoring", image_path)
            continue
        new_name = f"{args.prefix}_{image_path.name}"
        
        label_path = label_input_data / "labels" / image_path.with_suffix('.txt').name
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
            if args.class_id is not None:
                class_id = args.class_id
            elif args.class_map is not None:
                class_id = args.class_map[int(class_id)]
            new_bounding_boxes += f"{class_id} {x_center} {y_center} {width} {height}\n"
        output_label_path.write_text(new_bounding_boxes)
    