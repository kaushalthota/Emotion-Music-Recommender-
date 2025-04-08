import cv2
import numpy as np
from keras.models import load_model
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from collections import Counter
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import requests
import io
import csv
from datetime import datetime
import os

# Load pre-trained emotion detection model
emotion_model = load_model('emotion_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Spotify credentials
SPOTIPY_CLIENT_ID = 'ac8fbe7635054a7595f805b6850a23f1'
SPOTIPY_CLIENT_SECRET = '15967711f9b14c688d8731bfad7ff54f'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080/callback'

# Initialize Spotipy with required scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='ac8fbe7635054a7595f805b6850a23f1',
    client_secret='15967711f9b14c688d8731bfad7ff54f',
    redirect_uri='http://127.0.0.1:8080/callback',
    scope='user-library-read user-read-recently-played user-top-read playlist-modify-public'
))

# Emotion to genre mapping
emotion_genres = {
    'Angry': 'metal',
    'Disgust': 'punk',
    'Fear': 'ambient',
    'Happy': 'pop',
    'Sad': 'acoustic',
    'Surprise': 'indie',
    'Neutral': 'classical'
}

# GUI Setup
root = tk.Tk()
root.title("Emotion-Based Music Recommender")
root.geometry("640x820")
root.configure(bg='#121212')

style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', background='#121212', foreground='white', font=('Arial', 12))
style.configure('TButton', background='#1DB954', foreground='black', font=('Arial', 11, 'bold'))
style.configure('TCheckbutton', background='#121212', foreground='white', font=('Arial', 11))
style.configure('TOptionMenu', background='#1DB954', foreground='black')

header = ttk.Label(root, text="Mood-Based Music Recommender", font=('Arial', 18, 'bold'), foreground='#1DB954')
header.pack(pady=20)

instructions = ttk.Label(root, text="Playlist Mode: Creates a playlist from your emotion & listening history.\nSong Mode: Recommends a single track for instant listening.", justify="center")
instructions.pack(pady=5)

status_label = ttk.Label(root, text="Press 'Detect Emotion' to Start")
status_label.pack(pady=5)

loading_label = ttk.Label(root, text="")
loading_label.pack(pady=2)

emotion_result = tk.StringVar()
emotion_display = ttk.Label(root, textvariable=emotion_result, font=("Arial", 16))
emotion_display.pack(pady=10)

cover_label = tk.Label(root, bg='#121212')
cover_label.pack(pady=10)

preview_frame = tk.Frame(root, bg='#121212')
preview_frame.pack(pady=10)
preview_label = ttk.Label(preview_frame, text="")
preview_label.pack()
preview_image_label = tk.Label(preview_frame, bg='#121212')
preview_image_label.pack(pady=5)

controls_frame = tk.Frame(root, bg='#121212')
controls_frame.pack(pady=10)

track_count_var = tk.StringVar(value="10")
tt_label = ttk.Label(controls_frame, text="Tracks in Playlist:")
tt_label.grid(row=0, column=0, padx=5, sticky='w')
track_count_menu = ttk.OptionMenu(controls_frame, track_count_var, *[str(i) for i in range(5, 26, 5)])
track_count_menu.grid(row=0, column=1, padx=5, sticky='w')

mode_toggle = tk.BooleanVar(value=False)
mode_button = ttk.Checkbutton(controls_frame, text="Playlist Mode", variable=mode_toggle)
mode_button.grid(row=1, column=0, columnspan=2, sticky='w', pady=5)

preview_toggle = tk.BooleanVar(value=False)
preview_button = ttk.Checkbutton(controls_frame, text="Preview Songs Before Adding", variable=preview_toggle)
preview_button.grid(row=2, column=0, columnspan=2, sticky='w', pady=5)

current_emotion = ["Neutral"]


def get_recently_played_tracks(limit=50):
    try:
        recently_played = sp.current_user_recently_played(limit=limit)
        return recently_played['items']
    except Exception as e:
        print(f"Error fetching recently played tracks: {e}")
        return []


def analyze_user_genres(recent_tracks):
    genre_counter = Counter()
    for item in recent_tracks:
        track = item['track']
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genres = artist_info.get('genres', [])
        genre_counter.update(genres)
    sorted_genres = [genre for genre, count in genre_counter.most_common()]
    return sorted_genres


def save_emotion_to_csv(emotion):
    with open("emotion_log.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), emotion])


def create_playlist(emotion, track_limit, preview=False):
    recent_tracks = get_recently_played_tracks()
    user_genres = analyze_user_genres(recent_tracks)
    genre = user_genres[0] if user_genres else emotion_genres.get(emotion, 'pop')

    username = sp.current_user()['id']
    playlist_name = f"{emotion} Vibes Playlist"
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True)

    results = sp.search(q=f'genre:{genre}', type='track', limit=int(track_limit))
    track_uris = []

    for track in results['tracks']['items']:
        name = track['name']
        artist = track['artists'][0]['name']
        preview_url = track['external_urls']['spotify']
        if preview:
            preview_label.config(text=f"Previewing: {name} by {artist}\n{preview_url}")
            album_cover_url = track['album']['images'][0]['url']
            response = requests.get(album_cover_url)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data)).resize((120, 120))
            img = ImageTk.PhotoImage(img)
            preview_image_label.config(image=img)
            preview_image_label.image = img
            root.update()
            response = messagebox.askyesno("Preview Track", f"Add {name} by {artist}?\nPreview: {preview_url}")
            if not response:
                continue
        track_uris.append(track['uri'])

    preview_label.config(text="")
    preview_image_label.config(image="")

    if track_uris:
        sp.user_playlist_add_tracks(user=username, playlist_id=playlist['id'], tracks=track_uris)
        messagebox.showinfo("Playlist Created", f"Created playlist: {playlist_name}")
    else:
        messagebox.showinfo("No Tracks", "No tracks added to the playlist.")


def show_history():
    if not os.path.exists("emotion_log.csv"):
        messagebox.showinfo("No History", "No emotion history found.")
        return

    with open("emotion_log.csv", mode='r') as file:
        history = file.read()
        top = tk.Toplevel(root)
        top.title("Emotion History")
        top.geometry("500x300")
        text = tk.Text(top, wrap="word", bg='black', fg='white')
        text.insert("1.0", history)
        text.pack(expand=True, fill="both")


def detect_emotion():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    captured_frame = None
    detected_emotion = 'Neutral'

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi = roi_gray.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)

            preds = emotion_model.predict(roi)[0]
            detected_emotion = emotion_labels[np.argmax(preds)]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            captured_frame = frame.copy()
            break

        cv2.imshow('Detecting Emotion - Press Q to Exit', frame)
        if captured_frame is not None or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if captured_frame is not None:
        cv2.imshow('Detected Emotion - Press Q to Close', captured_frame)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return detected_emotion


def recommend_music(emotion, user_genres):
    genre = user_genres[0] if user_genres else emotion_genres.get(emotion, 'pop')

    results = sp.search(q=f'genre:{genre}', type='track', limit=10)
    tracks = results['tracks']['items']

    if not tracks:
        messagebox.showinfo("No Tracks", "No tracks found to recommend.")
        return

    random.shuffle(tracks)
    track = tracks[0]
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    track_url = track['external_urls']['spotify']
    album_cover_url = track['album']['images'][0]['url']

    status_label.config(text=f"Playing: {track_name} by {artist_name}")
    webbrowser.open(track_url)

    response = requests.get(album_cover_url)
    img_data = response.content
    img = Image.open(io.BytesIO(img_data)).resize((150, 150))
    img = ImageTk.PhotoImage(img)
    cover_label.config(image=img)
    cover_label.image = img


def start_detection():
    status_label.config(text="Detecting emotion...")
    loading_label.config(text="Loading... Please wait")

    def run():
        user_emotion = detect_emotion()
        current_emotion[0] = user_emotion
        emotion_result.set(f"Emotion: {user_emotion}")
        save_emotion_to_csv(user_emotion)

        recent_tracks = get_recently_played_tracks()
        user_genres = analyze_user_genres(recent_tracks)

        if mode_toggle.get():
            create_playlist(user_emotion, track_count_var.get(), preview=preview_toggle.get())
        else:
            recommend_music(user_emotion, user_genres)

        loading_label.config(text="")

    threading.Thread(target=run).start()


button_frame = tk.Frame(root, bg='#121212')
button_frame.pack(pady=20)

detect_button = ttk.Button(button_frame, text="Detect Emotion", command=start_detection)
detect_button.grid(row=0, column=0, padx=10)

history_button = ttk.Button(button_frame, text="View History", command=show_history)
history_button.grid(row=0, column=1, padx=10)

root.mainloop()
def recommend_from_recently_played():
    try:
        recent_tracks = get_recently_played_tracks(limit=50)

        if not recent_tracks:
            print("No recently played tracks found.")
            return

        artist_counter = Counter()
        track_ids = []

        for item in recent_tracks:
            track = item['track']
            artist_name = track['artists'][0]['name']
            artist_id = track['artists'][0]['id']
            track_ids.append(track['id'])
            artist_counter[artist_id] += 1

        # Pick the top 3 most frequent artists you've listened to recently
        top_artist_ids = [artist for artist, _ in artist_counter.most_common(3)]

        print("\n🎧 Songs recommended based on your last 50 plays:\n")

        for artist_id in top_artist_ids:
            top_tracks = sp.artist_top_tracks(artist_id)['tracks']
            for track in top_tracks[:3]:  # Limit to 3 tracks per artist
                name = track['name']
                artist = track['artists'][0]['name']
                url = track['external_urls']['spotify']
                print(f"{name} by {artist}")
                print(f"   🔗 {url}\n")

    except Exception as e:
        print("Error getting recommendations:", e)
