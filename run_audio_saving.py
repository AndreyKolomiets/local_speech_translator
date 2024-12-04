import pyaudio
import wave
import os
import argparse
from dotenv import load_dotenv

load_dotenv()


def get_default_input_device_index() -> int:
    audio_mock = pyaudio.PyAudio()
    device_idx = 0
    while True:
        info = audio_mock.get_device_info_by_index(device_index=device_idx)
        if info['name'] == os.environ['DEFAULT_INPUT_DEVICE_NAME']:
            return info['index']
        device_idx += 1


def write_one_batch(batch_num, input_device_index, folder):
    # Parameters
    FORMAT = pyaudio.paInt16  # Audio format
    CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
    RATE = 16000  # Sample rate (samples per second)
    CHUNK = 1024  # Number of frames per buffer
    RECORD_SECONDS = 30  # Duration of recording in seconds
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Open stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=input_device_index)  # МОЖЕТ НЕ РАБОТАТЬ БЕЗ ПОДКЛЮЧЕННОЙ КАМЕРЫ!
    
    print("Recording...")
    
    frames = []
    
    # Record audio
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Finished recording.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    
    # Terminate the PortAudio interface
    audio.terminate()
    
    # Save the recorded data as a WAV file
    output_filename = f'output{batch_num:03d}.wav'
    output_path = os.path.join(folder, output_filename)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device-index', type=int, default=-1)
    parser.add_argument('--folder', type=str)
    args = parser.parse_args()
    bn = 1
    if args.device_index == -1:
        device_index = get_default_input_device_index()
    else:
        device_index = args.device_index
    while True:
        write_one_batch(bn, input_device_index=device_index, folder=args.folder)
        bn += 1
