import re
import pathlib
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=pathlib.Path)
    parser.add_argument("output_dir", type=pathlib.Path)
    parser.add_argument("--filter", type=re.compile, help="A regex to filter filenames", default=re.compile('.*'))
    parser.add_argument("--format", help="A regex substition pattern", default=r"\g<0>")
    parser.add_argument("--rename", action="store_true")
    parser.add_argument("-y", action='store_true')
    args = parser.parse_args()

    for filepath in args.input_dir.glob("**/*"):
        if filepath.is_dir() or not re.fullmatch(args.filter, str(filepath.name)):
            continue
        try:
            # import pdb; pdb.set_trace()

            new_name = re.sub(args.filter, args.format, filepath.name) 
            relative_path = filepath.with_name(new_name).relative_to(args.input_dir)
            output_path: pathlib.Path = args.output_dir / relative_path
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if not args.y and input(f"Would you like to rename {filepath} to {output_path}? [y]/n: ") == "n":
                continue
            if args.rename:
                filepath.rename(str(output_path))
            else:
                output_path.write_bytes(filepath.read_bytes())
        except Exception as e:
            import sys
            print(e, file=sys.stderr)