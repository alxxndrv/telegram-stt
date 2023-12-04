import subprocess
from convert import ogg_to_wav
import os


def run_command(filename: str):
    try:
        result = subprocess.run(
            ['./whisper', '-f', filename, '-m', 'ggml-medium.bin',
                '--language', 'russian', '-otxt'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"


def transcribe(filename: str):
    if filename.endswith('.ogg') or filename.endswith('.oga'):
        filename_wav = ogg_to_wav(filename)
        os.remove(filename)
        filename = filename_wav

    if not filename.endswith('.wav'):
        raise ValueError("Unsupported file format")

    run_command(filename)
    os.remove(filename)

    output_file = filename + '.txt'

    contents = open(output_file).read()

    os.remove(output_file)

    return contents


if __name__ == '__main__':
    print(run_command('files/file_3.wav'))
