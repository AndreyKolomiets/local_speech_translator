import subprocess
import os
import argparse
from dotenv import load_dotenv
import time

load_dotenv()

EXECUTABLE_PATH = '/Users/andrey/whisper.cpp/build/bin/main'
MODEL_PATH = '/Users/andrey/whisper.cpp/models/ggml-large-v3.bin'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial-prompt', type=str, default='')
    parser.add_argument('--folder', type=str)

    args = parser.parse_args()
    max_fname = ''
    prompt = args.initial_prompt
    while True:
        files = [f for f in os.listdir(args.folder) if f.endswith('.wav')]
        if len(files) == 0:
            time.sleep(1)
            continue
        curr_max_fname = max(files)
        if curr_max_fname > max_fname:
            max_fname = curr_max_fname
            input_path = os.path.join(args.folder, max_fname)
            cmd = f'{EXECUTABLE_PATH} -m {MODEL_PATH} -f {input_path}  -otxt -p 1 -t 16 -l he --translate --prompt "{prompt}"'
            subprocess.check_output(cmd, shell=True)
            # text_path = input_path + '.txt'
            # with open(text_path, 'r') as f:
            #     for line in f:
            #         print(line)
        else:
            time.sleep(1)


if __name__ == '__main__':
    main()
