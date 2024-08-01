# Song to Text

這個項目用於將 MP3 文件轉換為 WAV 文件，然後使用 Vosk 語音識別模型將音頻轉錄為文本。

## 資料夾結構

```plaintext
Song to Text/
├── models/
│   ├── vosk-model-small-cn-0.22/
│   ├── vosk-model-small-en-us-0.15/
│   └── vosk-model-small-ko-0.22/
├── audio/
│   ├── mp3/
│   │   ├── Black_people_carrying_coffins.mp3
│   │   ├── Love_Yourself.mp3
│   │   ├── Meow_Meow_Meow.mp3
│   │   └── 麻辣燙糖葫蘆Malatanghulu.mp3
│   └── wav/
│       ├── Black_people_carrying_coffins.wav
│       ├── Love_Yourself.wav
│       ├── Meow_Meow_Meow.wav
│       └── 麻辣燙糖葫蘆Malatanghulu.wav
├── scripts/
│   └── Song_to_Text.py
└── results/
    └── transcription.txt
```

## 安裝

1. 安裝 Python 3.6 或更高版本
2. 安裝必要的 Python 庫：

    ```bash
    pip install vosk pydub ffmpeg-python
    ```

3. 安裝 FFmpeg 並確保其在系統路徑中。可以從 [FFmpeg 官網](https://ffmpeg.org/download.html) 下載並安裝。

## 使用

1. 下載 Vosk 語音識別模型並解壓到 `models/` 資料夾中。模型可以從 [Vosk 模型下載頁面](https://alphacephei.com/vosk/models) 獲取。

    - [vosk-model-small-cn-0.22](https://your-s3-bucket-url/vosk-model-small-cn-0.22.zip)
    - [vosk-model-small-en-us-0.15](https://your-s3-bucket-url/vosk-model-small-en-us-0.15.zip)
    - [vosk-model-small-ko-0.22](https://your-s3-bucket-url/vosk-model-small-ko-0.22.zip)

2. 將 MP3 文件放入 `audio/mp3/` 資料夾中。

3. 執行 `scripts/Song_to_Text.py` 腳本：

    ```bash
    python scripts/Song_to_Text.py
    ```

4. 語音識別結果將保存在 `results/` 資料夾中，文件名與 MP3 文件名對應。

## 腳本說明

`Song_to_Text.py` 腳本會執行以下步驟：

1. 搜索 `audio/mp3/` 資料夾中的所有 MP3 文件。
2. 將 MP3 文件轉換為 WAV 文件並保存到 `audio/wav/` 資料夾中。
3. 使用 Vosk 語音識別模型對每個 WAV 文件進行轉錄。
4. 將轉錄結果保存到 `results/` 資料夾中，文件名與 MP3 文件名對應。

## 參考資料

- [Vosk 語音識別模型](https://alphacephei.com/vosk/models)
- [FFmpeg](https://ffmpeg.org/)
- [Pydub](https://github.com/jiaaro/pydub)

## 聯繫方式

如有任何問題或建議，請聯繫我：sky.ho@advantech.com.tw
```


