# Spotify → YouTube Music Playlist Exporter 🎵

Export your **Spotify Liked Songs** to a **YouTube Music playlist** automatically!

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Spotify](https://img.shields.io/badge/Spotify-API-green.svg)](https://developer.spotify.com/)
[![YouTube Music](https://img.shields.io/badge/YouTube%20Music-API-red.svg)](https://music.youtube.com/)

## ✨ Features

- ✅ **Spotify Liked Songs** → **YouTube Music playlist** (one-click)
- 🔍 **`yt-dlp`** finds best matching YouTube videos automatically
- ⚙️ **config.json** for all credentials (or interactive setup)
- 🧪 **Test mode** (`max_songs: 10`) for debugging
- 📱 Works with **Authorization + Cookie** (no OAuth hassle)

## 📦 Quick Start

```bash
# 1. Install requirements
pip install spotipy ytmusicapi pandas

# 2. Download yt-dlp.exe
 https://github.com/yt-dlp/yt-dlp/releases (Windows)
# OR: pip install yt-dlp (cross-platform)

# 3. Run
python spotify_to_ytmusic.py


# 1. Install requirements

pip install spotipy ytmusicapi pandas

# 2. Download yt-dlp.exe

# https://github.com/yt-dlp/yt-dlp/releases (Windows)

# OR: pip install yt-dlp (cross-platform)

# 3. Run

python spotify_to_ytmusic.py

```

---

## ⚙️ Configuration (`config.json`)

**First run creates this file automatically:**

```

{
  "spotify": {
    "client_id": "",
    "client_secret": ""
  },
  "ytmusic": {
    "authorization": "",
    "cookie": ""
  },
  "test_mode": {
    "max_songs": 10
  }
}

```

### Two setup options:

#### **Option 1: Edit `config.json` manually** ✅

Fill all values → save → run script

#### **Option 2: Interactive prompts** ✅

Leave empty → script asks for missing values on first run

---

## 🎯 Required Credentials

### 1. Spotify API Credentials

**Where:** [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

```

1. Login → Create App → "Playlist Exporter"
2. Settings → Redirect URI: http://127.0.0.1:8888/callback
3. Copy Client ID \& Client Secret
```

**config.json:**
```

"spotify": {
"client_id": "abc123yourspotifyclientid",
"client_secret": "xyz789yourspotifyclientsecret"
}

```

### 2. YouTube Music Headers **(ONLY 2 FIELDS!)**

**Where:** Browser DevTools → Network → `browse` request

```

1. https://music.youtube.com (logged in)
2. F12 → Network → scroll/click → find "browse"
3. Right-click → Copy → Copy as cURL
4. https://curlconverter.com → Python
5. Copy ONLY these 2 lines:
```

**From cURL converter:**
```

{
"Authorization": "SAPISIDHASH 1abc123longtoken...",
"Cookie": "LOGIN_INFO=...; VISITOR_INFO1_LIVE=...; YSC=...; ..."
}

```

**config.json:**
```

"ytmusic": {
"authorization": "SAPISIDHASH 1abc123longtoken...",
"cookie": "LOGIN_INFO=...; VISITOR_INFO1_LIVE=...; YSC=...; ..."
}

```

### 3. Test Mode

```

"test_mode": {
"max_songs": 10
}

```

- **`10`** = Test first **10 songs** (~2min, perfect for debugging)
- **`0`** = **ALL** liked songs (~30-60min for large libraries)

---

## 🔧 Auto-generated `headers_auth.json`

**Script creates this from your 2 values:**

```

{
"Accept": "*/*",
"Authorization": "SAPISIDHASH 1abc123...",
"Content-Type": "application/json",
"X-Goog-AuthUser": "0",
"x-origin": "https://music.youtube.com",
"Cookie": "LOGIN_INFO=...; VISITOR_INFO1_LIVE=..."
}

```

**Used by:** `YTMusic("headers_auth.json")`

---

## 🚀 Complete Workflow

```

Spotify Liked Songs (847 songs)
↓
yt-dlp ytsearch1:"Artist - Title"
↓
spotify_liked_songs_847songs.txt (723 URLs)
↓
ytmusicapi + headers_auth.json
↓
🎉 YouTube Music: "My Spotify Likes (723)"

```

**Example run:**

![til](https://raw.githubusercontent.com/shlomo120/Spotify2YoutubeMigration/master/app/assets/images/testrun.gif)

```

🎵 STEP 1/3: Getting Spotify liked songs...
✅ Found 847 liked songs!
🎯 MAX_SONGS=10

🔍 STEP 2/3: Finding YouTube links...
Progress: 10/10 (100.0%)
✅ 8/10 links found (80.0%)!
💾 Saved: spotify_liked_songs_10songs.txt

🎬 STEP 3/3: Creating YouTube Music playlist...
✅ Connected to YouTube Music!
✅ 8 video IDs ready!
✅ Playlist created! ID: PL9qIzx58Cd...
🎉 SUCCESS!
📝 'Test Playlist (8)' - 8 songs

```

---

## 📁 Generated Files

| File | Purpose |
|------|---------|
| **`config.json`** | **Your credentials** (edit once) |
| **`headers_auth.json`** | **Auto-generated** (don't edit) |
| **`spotify_liked_songs_Nsongs.txt`** | **Debug: All YouTube URLs found** |

---

## 🔍 Finding Your Playlist

**YouTube Music App / Website:**
```

📱 Library → Playlists
🌐 https://music.youtube.com/playlist
🔍 Search Your Playlists

```

---

## 🛠️ Troubleshooting

### ❌ **"yt-dlp.exe not found"**
```

Download: https://github.com/yt-dlp/yt-dlp/releases
Put yt-dlp.exe in same folder as script

```

### ❌ **"YouTube Music auth failed"**
```

1. Authorization/Cookie expired → re-capture from DevTools
2. Use same Google account in browser \& script
3. Check Network tab → "browse" request headers
```

### ❌ **"0/N links found" (0% success)**
```

1. yt-dlp.exe must exist \& be executable
2. Check internet connection
3. Test with English songs first (set max_songs=5)
```

### ❌ **Spotify callback error**
```

Redirect URI MUST be exactly:
http://127.0.0.1:8888/callback

```

---

## 📦 Requirements

```

pip install spotipy ytmusicapi pandas

```

**Plus:** `yt-dlp.exe` (Windows) or `pip install yt-dlp`

---

## 📄 License

MIT License

---

## 🙌 Credits

- **[ytmusicapi](https://github.com/sigma67/ytmusicapi)** - YouTube Music API [web:48]
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube search
- **[spotipy](https://spotipy.readthedocs.io/)** - Spotify API

**Perfect for Spotify → YouTube Music migration!** 🎵✨
```
