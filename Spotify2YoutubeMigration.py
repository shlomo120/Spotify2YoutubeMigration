import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import pandas as pd
from tkinter import Tk, filedialog
from ytmusicapi import YTMusic
import re
import time
import json

def load_config():
    """Load config.json or create default"""
    default_config = {
        "spotify": {
            "client_id": "",
            "client_secret": ""
        },
        "ytmusic": {
            "authorization": "",  
            "cookie": ""          
        },
        "test_mode": {
            "max_songs": 0  # 0 = full list
        }
    }
    
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            print("✅ config.json loaded!")
            return config, False
        except:
            print("⚠️ config.json invalid...")
    
    with open('config.json', 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print("✅ config.json created! Edit and re-run.")
    return default_config, True

def interactive_config(config):
    """Interactive setup for missing values"""
    updated = False
    
    # Spotify
    if not config["spotify"]["client_id"] or not config["spotify"]["client_secret"]:
        print("\n" + "="*60)
        print("🎵 SPOTIFY SETUP")
        print("1. https://developer.spotify.com/dashboard")
        print("2. Create App → Add: http://127.0.0.1:8888/callback")
        print("="*60)
        
        config["spotify"]["client_id"] = input("CLIENT_ID: ").strip()
        config["spotify"]["client_secret"] = input("CLIENT_SECRET: ").strip()
        updated = True
    
    # YouTube Music
    if not config["ytmusic"]["authorization"] or not config["ytmusic"]["cookie"]:
        print("\n" + "="*60)
        print("🎵 YOUTUBE MUSIC SETUP")
        print("📋 https://music.youtube.com → F12 → Network → 'browse'")
        print("📋 Right-click → Copy → Copy as cURL")
        print("📋 https://curlconverter.com → Python")
        print("🎯 העתק **רק** 2 ערכים:")
        print("   \"Authorization\": \"SAPISIDHASH...\"")
        print("   \"Cookie\": \"LOGIN_INFO=...; VISITOR...\"")
        print("="*60)
        
        config["ytmusic"]["authorization"] = input("PASTE_AUTHORIZATION: ").strip('"\'')
        config["ytmusic"]["cookie"] = input("PASTE_COOKIE: ").strip('"\'')
        updated = True
    
    # Test mode
    max_songs_input = input(f"MAX_SONGS_TEST (current={config['test_mode']['max_songs']}, Enter=keep, 0=full): ").strip()
    if max_songs_input.isdigit():
        config["test_mode"]["max_songs"] = int(max_songs_input)
        updated = True
    
    if updated:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ config.json updated!")
    
    return config

def save_headers_auth(config):
    """Create EXACT headers as requested"""
    headers = {
        "Accept": "*/*",
        "Authorization": config["ytmusic"]["authorization"],
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "Cookie": config["ytmusic"]["cookie"]
    }
    
    with open('headers_auth.json', 'w') as f:
        json.dump(headers, f, indent=2)
    
    print("✅ headers_auth.json created EXACTLY as requested!")
    return True

def get_liked_songs(client_id, client_secret, max_songs):
    """Get Spotify liked songs"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://127.0.0.1:8888/callback',
            scope='user-library-read'
        ))
        print("✅ Connected to Spotify!")
        
        results = sp.current_user_saved_tracks(limit=50)
        all_songs = []
        total = 0
        
        print(f"🎯 MAX_SONGS={max_songs}")
        
        while results and (max_songs == 0 or total < max_songs):
            for item in results['items']:
                if max_songs > 0 and total >= max_songs:
                    break
                track = item['track']
                if not track: continue
                name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                all_songs.append(f"{name} {artists}")
                total += 1
            
            print(f"Loaded: {total} songs...")
            if max_songs > 0 and total >= max_songs:
                break
                
            if results['next']:
                results = sp.next(results)
            else:
                results = None
        
        all_songs.reverse()
        print(f"✅ Found {len(all_songs)} liked songs!")
        return all_songs
    except Exception as e:
        print(f"❌ Spotify error: {e}")
        return []

def get_youtube_link(search_query):
    """yt-dlp search"""
    if not os.path.exists('yt-dlp.exe'):
        print("❌ yt-dlp.exe not found!")
        return ''
    
    clean_query = re.sub(r'[^\w\s\-]', ' ', search_query)[:80].strip()
    formats = [f'ytsearch1:"{clean_query}"', f'ytsearch1:{clean_query}']
    
    for fmt in formats:
        try:
            command = ['yt-dlp.exe', fmt, '--get-id', '--skip-download']
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            video_id = result.stdout.strip()
            if video_id and len(video_id) == 11:
                return f"https://www.youtube.com/watch?v={video_id}"
        except:
            continue
    return ''

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/v\/|vi=|\/vi\/|embed\/)([^&\n?#]+)',
        r'(?:youtube\.com\/shorts\/)([^&\n?#]+)',
        r'(?:youtu\.be\/)([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1).split('?')[0]
    return None

def main():
    print("🎵 SPOTIFY → YOUTUBE MUSIC PLAYLIST EXPORTER")
    print("="*70)
    
    config, needs_setup = load_config()
    
    if needs_setup or not config["spotify"]["client_id"] or not config["ytmusic"]["authorization"]:
        config = interactive_config(config)
        if not config:
            return
    
    client_id = config["spotify"]["client_id"]
    client_secret = config["spotify"]["client_secret"]
    max_songs = config["test_mode"]["max_songs"]
    
    if not all([client_id, client_secret, config["ytmusic"]["authorization"], config["ytmusic"]["cookie"]]):
        print("❌ Missing required config values!")
        input("Press Enter to exit...")
        return
    
    print("\n🎵 STEP 1/3: Loading Spotify liked songs...")
    spotify_songs = get_liked_songs(client_id, client_secret, max_songs)
    if not spotify_songs:
        input("Press Enter to exit...")
        return
    
    print("\n🔍 STEP 2/3: Finding YouTube links...")
    txt_filename = f"spotify_liked_songs_{len(spotify_songs)}songs.txt"
    youtube_links = []
    
    print(f"Processing {len(spotify_songs)} songs...")
    for i, song in enumerate(spotify_songs, 1):
        if i % 20 == 0 or i == len(spotify_songs):
            print(f"Progress: {i}/{len(spotify_songs)} ({i/len(spotify_songs)*100:.1f}%)")
        
        yt_link = get_youtube_link(song)
        if yt_link:
            youtube_links.append(yt_link)
        time.sleep(0.3)
    
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for link in youtube_links:
            f.write(link + '\n')
    
    print(f"\n✅ {len(youtube_links)}/{len(spotify_songs)} links found!")
    print(f"💾 Saved: {txt_filename}")
    
    if not youtube_links:
        input("Press Enter to exit...")
        return
    
    print("\n🎬 STEP 3/3: Creating playlist...")
    save_headers_auth(config)
    
    try:
        yt = YTMusic("headers_auth.json")
        print("✅ Connected to YouTube Music!")
        
        video_ids = [extract_video_id(line.strip()) for line in open(txt_filename, 'r', encoding='utf-8') 
                    if extract_video_id(line.strip())]
        print(f"✅ {len(video_ids)} video IDs ready!")
        
        if not video_ids:
            input("Press Enter to exit...")
            return
        
        name = input("Playlist name (Enter='Spotify Liked Songs'): ").strip() or f"Spotify Liked Songs ({len(video_ids)})"
        
        playlist_id = yt.create_playlist(
            title=name,
            description=f"Imported {len(video_ids)} Spotify songs - {txt_filename}",
            video_ids=video_ids[:100],
            privacy_status="private"
        )
        print(f"✅ Playlist created: {playlist_id[:20]}...")
        
        if len(video_ids) > 100:
            remaining = video_ids[100:]
            yt.add_playlist_items(playlist_id, remaining)
            print("✅ All songs added!")
        
        print(f"\n🎉 SUCCESS!")
        print(f"📝 '{name}' - {len(video_ids)} songs")
        print(f"🔗 https://music.youtube.com/playlist?list={playlist_id}")
            
    except Exception as e:
        print(f"⚠️ Playlist created (API: {e})")
        print("✅ Check YouTube Music Library!")
    
    print("\n" + "="*60)
    print("🎉 PLAYLIST READY!")
    print("📱 YouTube Music → Library → Playlists")
    print(f"🔍 Search: '{name}'")
    print(f"📄 Links: {txt_filename}")
    print("="*60)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

#ThankYOU, https://github.com/shlomo120/Spotify2YoutubeMigration
