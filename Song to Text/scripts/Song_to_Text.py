import subprocess
import wave
from vosk import Model, KaldiRecognizer
import json
import os
import glob

# 設定資料夾路徑
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "models", "vosk-model-small-en-us-0.15")
mp3_dir = os.path.join(base_dir, "..", "audio", "mp3")
wav_dir = os.path.join(base_dir, "..", "audio", "wav")
result_dir = os.path.join(base_dir, "..", "results")

# 轉換 MP3 到 WAV
def convert_mp3_to_wav(input_path, output_path):
    command = ["ffmpeg", "-i", input_path, output_path]
    subprocess.run(command, check=True)

# 查找所有 MP3 文件
mp3_files = glob.glob(os.path.join(mp3_dir, "*.mp3"))

for mp3_path in mp3_files:
    mp3_file = os.path.basename(mp3_path)
    wav_file = os.path.splitext(mp3_file)[0] + ".wav"
    wav_path = os.path.join(wav_dir, wav_file)

    convert_mp3_to_wav(mp3_path, wav_path)

    model = Model(model_path)

    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    result_text = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            result_text.append(result.get('text', ''))

    final_result = json.loads(rec.FinalResult())
    result_text.append(final_result.get('text', ''))

    full_text = ' '.join(result_text)

    # 將結果保存到文件
    result_file = os.path.splitext(mp3_file)[0] + "_transcription.txt"
    result_path = os.path.join(result_dir, result_file)

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(full_text)
