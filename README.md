# 🎵 Emotion-Based Music Recommender

This Python project uses your **facial emotion** to recommend music via the **Spotify API**. Using a webcam, the app detects your mood and recommends a track or builds a custom playlist based on your listening history.

> Built with: Python, OpenCV, Keras, Spotipy, Tkinter

---

## 🧠 Features

- Real-time emotion detection using your webcam
- Song or playlist recommendation using Spotify API
- Uses your Spotify listening history for smarter suggestions
- Toggle between playlist or single-song recommendation
- Option to preview songs before adding
- Album art and emotion logs saved locally
- Clean, dark-themed GUI inspired by Spotify

---

## 🖼️ Screenshots

### 🎭 Emotion Detection (Webcam Feed)
_Automatically detects your emotion using a pre-trained CNN model._
![Emotion Capture](https://github.com/user-attachments/assets/8af8647d-3c76-4197-bf0b-2b83c2b8aef6)
### 🎧 Song or Playlist Recommendation
_See album art and track name. Choose playlist mode or quick-play mode._
![Screenshot 2025-04-08 004809](https://github.com/user-attachments/assets/8a4fe479-3af9-4aea-8d67-ff3b80d1a609)
### 🎶 Playlist Preview with Accept/Reject
_Preview songs and decide which to add to your generated playlist._

![image](https://github.com/user-attachments/assets/5bbf49a0-90a6-49e2-b584-02389adfbf38)


### 📊 Emotion History Viewer
_View your past detected moods and timestamps._

![History](https://github.com/user-attachments/assets/7ac5c66e-db31-49a0-84a2-5292e1935989)


---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/emotion-music-recommender.git
cd emotion-music-recommender
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

> Dependencies: `opencv-python`, `numpy`, `keras`, `spotipy`, `pillow`, `requests`, `tkinter`

### 3. Add Required Files

- Your trained `emotion_model.h5` (use [FER-2013 dataset](https://www.kaggle.com/datasets/msambare/fer2013) to train)
- Your Spotify API credentials

### 4. Set Up Spotify API

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Note your **Client ID**, **Client Secret**
4. Set the redirect URI in your app settings:
   ```
   http://127.0.0.1:8080/callback
   ```

Replace the `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` variables in the code.

---

## 🧪 Running the App

```bash
python main.py
```

The GUI will launch automatically.

---

## 📁 File Structure

```
emotion-music-recommender/
├── main.py
├── emotion_model.h5
├── emotion_log.csv
├── requirements.txt
├── README.md
└── assets/
    ├── emotion-detection.png
    ├── recommend-track.png
    ├── playlist-preview.gif
    └── history-viewer.png
```

---

## 💡 Future Ideas

- Add live audio previews
- In-app Spotify authentication (without browser)
- Plot emotion history with charts

---

## 🙌 Acknowledgments

- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [OpenCV](https://opencv.org/)
- [FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)

---

## 📬 Contact

Made with love by kaushalthota
