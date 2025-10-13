import argparse
import json
import os

from pathlib import Path


def _define_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('--what', 
                             type=str,
                             required=True,
                             help='what to update [mips,matches]')

    args_parser.add_argument('-i', '--input', 
                             type=str,
                             required=True,
                             help='input path')

    args_parser.add_argument('-o', '--output', 
                             type=str,
                             required=True,
                             help='output path')
    
    return args_parser


def _update_match_files(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f'Update {input_path} -> {output_path}')

    updated_files = 0
    for path in input_path.rglob("*.json"):   # recursive: use glob("*.json") for non-recursive
        updated_files = updated_files + _update_match_file(path, output_path)
    
    print (f'Updated {updated_files} files from {input_path}')
    

def _update_match_file(input_file, output_dir):
    input_filename = os.path.basename(input_file)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        input_image = data.get("inputImage")
        results = data.get("results")

        if input_image.get("alignmentSpace") == 'JRC2018_Unisex_20x_HR':
            input_image['anatomicalArea'] = 'Brain'
        elif input_image.get("alignmentSpace") == 'JRC2018_VNC_Unisex_40x_DS':
            input_image['anatomicalArea'] = 'VNC'
        else:
            print(f'Invalid alignment space found for input image {input_image} in {path}')
        
        for result_image in results:
            if result_image.get("alignmentSpace") == 'JRC2018_Unisex_20x_HR':
                result_image['anatomicalArea'] = 'Brain'
            elif result_image.get("alignmentSpace") == 'JRC2018_VNC_Unisex_40x_DS':
                result_image['anatomicalArea'] = 'VNC'
            else:
                print(f'Invalid alignment space found for result image {result_image} in {path}')

        # Compute relative output path
        target = Path(f'{output_dir}/{input_filename}')
        target.parent.mkdir(parents=True, exist_ok=True)

        print(f'Write {target}')
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return 1

    except (json.JSONDecodeError, OSError) as e:
        print(f"❌ Error processing {input_file}: {e}")
        return 0
    

def _update_mips_files(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f'Update {input_path} -> {output_path}')

    updated_files = 0
    for path in input_path.rglob("*.json"):   # recursive: use glob("*.json") for non-recursive
        updated_files = updated_files + _update_mips_file(path, output_path)
    
    print (f'Updated {updated_files} files from {input_path}')


def _update_mips_file(input_file, output_dir):
    try:
        input_filename = os.path.basename(input_file)
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = data.get("results")

        for result_image in results:
            print(f'Update MIP: {result_image['id']}')
            if result_image.get("alignmentSpace") == 'JRC2018_Unisex_20x_HR':
                result_image['anatomicalArea'] = 'Brain'
            elif result_image.get("alignmentSpace") == 'JRC2018_VNC_Unisex_40x_DS':
                result_image['anatomicaArea'] = 'VNC'
            else:
                print(f'Invalid alignment space found for result image {result_image} in {path}')

        # Compute relative output path
        target = Path(f'{output_dir}/{input_filename}')
        target.parent.mkdir(parents=True, exist_ok=True)

        print(f'Write {target}')
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return 1
    except (json.JSONDecodeError, OSError) as e:
        print(f"❌ Error processing {input_file}: {e}")
        return 0
    

if __name__ == '__main__':
    args_parser = _define_args()
    args = args_parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if args.what == 'mips':
        if input_path.is_file():
            _update_mips_file(input_path, args.output)
        else:
            _update_mips_files(input_path, args.output)
        
    elif args.what == 'matches':
        if input_path.is_file():
            _update_match_files(input_path, args.output)
        else:
            _update_match_files(input_path, args.output)
    else:
        print(f'Invalid {args.what} - valid values are: mips, matches')