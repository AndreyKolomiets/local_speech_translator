import pyaudio
import wave
import os
from dotenv import load_dotenv

load_dotenv()


def write_one_batch(batch_num):
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
                        input_device_index=0)  # МОЖЕТ НЕ РАБОТАТЬ БЕЗ ПОДКЛЮЧЕННОЙ КАМЕРЫ!
    
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
    output_path = os.path.join(os.environ['FOLDER'], output_filename)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {output_path}")


if __name__ == '__main__':
    bn = 1
    while True:
        write_one_batch(bn)
        bn += 1
