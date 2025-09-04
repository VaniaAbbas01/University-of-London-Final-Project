import ffmpeg, io, librosa

def decode_audio_file(buffer):
    out, _ = (
        ffmpeg.input('pipe:0')
        .output('pipe:1', format='wav')
        .run(input=buffer.read(), capture_stdout=True, capture_stderr=True)
    )
    return out

def buffer_to_waveform(buffer):
    buffer = io.BytesIO(buffer)
    buffer.seek(0)
    y, sr = librosa.load(buffer, sr=None)
    return y, sr

def find_audio_duration(audio_path):
    try:
        probe = ffmpeg.probe(audio_path)
        return float(probe['format']['duration'])
    except Exception as e:
        print(f"Error: {e}")
        return None

def allowed_file(filename, allowed_ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext
