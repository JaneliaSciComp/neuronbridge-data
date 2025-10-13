import argparse
import json

from pathlib import Path

def _define_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('-i', '--input', 
                             type=str,
                             required=True,
                             help='input path')

    args_parser.add_argument('-o', '--output', 
                             type=str,
                             required=True,
                             help='output path')
    
    return args_parser


def _update_result_files(input_dir, output_dir):
    """
    Reads JSON files from input_dir, updates the 'anatomicalArea' field,
    and writes them to output_dir.

    Args:
        input_dir (str | Path): Directory containing input JSON files.
        output_dir (str | Path): Directory to write modified files to.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f'Update ${input_dir} -> {output_dir}')

    updated_files = 0
    for path in input_dir.rglob("*.json"):   # recursive: use glob("*.json") for non-recursive
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            input_image = data.get("inputImage")
            results = data.get("results")

            if input_image.get("alignmentSpace") == 'JRC2018_Unisex_20x_HR':
                input_image['anatomicalArea'] = 'Brain'
            elif input_image.get("alignmentSpace") == 'JRC2018_VNC_Unisex_40x_DS':
                input_image['anatomicaArea'] = 'VNC'
            else:
                print(f'Invalid alignment space found for input image {input_image} in {path}')
            
            for result_image in results:
                if input_image.get("alignmentSpace") == 'JRC2018_Unisex_20x_HR':
                    input_image['anatomicalArea'] = 'Brain'
                elif input_image.get("alignmentSpace") == 'JRC2018_VNC_Unisex_40x_DS':
                    input_image['anatomicaArea'] = 'VNC'
                else:
                    print(f'Invalid alignment space found for result image {input_image} in {path}')

            # Compute relative output path
            relative_path = path.relative_to(input_dir)
            target = output_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)

            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            updated_files = updated_files + 1

        except (json.JSONDecodeError, OSError) as e:
            print(f"❌ Error processing {path}: {e}")
    
    print (f'Updated {updated_files} files in {input_dir}')


if __name__ == '__main__':
    args_parser = _define_args()
    args = args_parser.parse_args()

    _update_result_files(args.input, args.output):