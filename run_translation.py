import subprocess
import os
import argparse
from dotenv import load_dotenv
import time

from constants import RESET_PROMPT_FNAME

load_dotenv()
EXECUTABLE_PATH = os.environ["EXECUTABLE_PATH"]
MODEL_PATH = os.environ["MODEL_PATH"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial-prompt', type=str, default='')
    parser.add_argument('--folder', type=str)

    args = parser.parse_args()
    max_fname = ''
    prev_transcript_fname = None
    while True:
        files = [f for f in os.listdir(args.folder) if f.endswith('.wav')]
        if len(files) == 0:
            time.sleep(1)
            continue
        curr_max_fname = max(files)
        if curr_max_fname > max_fname:
            max_fname = curr_max_fname
            input_path = os.path.join(args.folder, max_fname)
            reset_prompt_path = os.path.join(args.folder, RESET_PROMPT_FNAME)
            if prev_transcript_fname is None:
                prompt = args.initial_prompt
            elif os.path.exists(reset_prompt_path):
                # sometimes previous file translation is bad, and negative feedback loop occurs,
                # when the next translation is also bad and no chance to improve
                prompt = args.initial_prompt
                os.remove(reset_prompt_path)
            else:
                path_prev_transcript = os.path.join(args.folder, prev_transcript_fname)
                with open(path_prev_transcript, 'r') as f:
                    prompt = '. '.join(line.strip() for line in f)
            cmd = [
                EXECUTABLE_PATH,
                '-m', MODEL_PATH,
                '-f', input_path,
                '-otxt',
                '-p', '1',
                '-t', '16',
                '-l', 'he',
                '--translate',
                '--prompt', prompt,
                '-np'
            ]
            subprocess.check_output(cmd, shell=False)
            prev_transcript_fname = max_fname + '.txt'
        else:
            time.sleep(1)


if __name__ == '__main__':
    main()
