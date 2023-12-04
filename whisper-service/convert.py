import ffmpeg


def ogg_to_wav(input_ogg_file, output_wav_file=None, sample_rate=16000):
    if output_wav_file is None:
        output_wav_file = input_ogg_file.removesuffix(
            '.ogg').removesuffix('.oga') + '.wav'

    (ffmpeg
        .input(input_ogg_file)
        .output(output_wav_file, ar=sample_rate)
        .run())

    return output_wav_file


if __name__ == '__main__':
    pass
