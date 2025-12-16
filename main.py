import yt_dlp
import sys

def download_video(url, output_path='downloads'):
    """
    Download a YouTube video
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the video (default: 'downloads')
    """
    
    # Configuration options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'merge_output_format': 'mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\n✓ Successfully downloaded: {info['title']}")
            
    except Exception as e:
        print(f"\n✗ Error downloading video: {str(e)}")
        sys.exit(1)

def progress_hook(d):
    """Display download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print(f"\n✓ Download complete, now processing...")

def download_audio_only(url, output_path='downloads'):
    """
    Download audio only from YouTube video
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the audio (default: 'downloads')
    """
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\n✓ Successfully downloaded: {info['title']}")
            
    except Exception as e:
        print(f"\n✗ Error downloading audio: {str(e)}")
        sys.exit(1)

def main():
    """Main function with user interaction"""
    
    print("=" * 50)
    print("YouTube Video Downloader")
    print("=" * 50)
    
    # Get video URL from user
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nEnter YouTube video URL: ").strip()
    
    if not url:
        print("Error: No URL provided")
        sys.exit(1)
    
    # Ask user for download type
    print("\nSelect download option:")
    print("1. Video (best quality)")
    print("2. Audio only (MP3)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        download_video(url)
    elif choice == '2':
        download_audio_only(url)
    else:
        print("Invalid choice. Defaulting to video download.")
        download_video(url)

if __name__ == "__main__":
    main()