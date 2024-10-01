import yt_dlp
from yt_dlp.utils import DownloadError
from urllib.parse import urlparse, parse_qs, urlencode

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'extract_flat': True,
    'skip_download': True,
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

def get_video_info(url):
    # Remove playlist parameter from URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params.pop('list', None)
    clean_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

    with ydl:
        try:
            result = ydl.extract_info(clean_url, download=False)
        except DownloadError:
            return None

    if 'entries' in result:
        # If it's still a playlist, take the first video
        video = result['entries'][0]
    else:
        # Just a video
        video = result
    return video

def get_audio_and_video_urls(video_info):
    video_formats = []
    audio_formats = []
    for f in video_info['formats']:
        if f['ext'] != 'mhtml':
            format_info = {
                'ext': f.get('ext', 'Unknown'),
                'filesize': f.get('filesize', 0),
                'resolution': f.get('resolution', 'Unknown'),
                'url': f.get('url')
            }
            if f.get('vcodec') != 'none' and f['ext'] == 'mp4':
                video_formats.append(format_info)
            elif f.get('acodec') != 'none':
                audio_formats.append(format_info)

    # Sort videos by size (from largest to smallest)
    video_formats.sort(key=lambda x: x['filesize'] or 0, reverse=True)
    
    # Get audio URL in m4a format (if available)
    audio_format = next((f for f in audio_formats if f['ext'] == 'm4a'), None)
    audio_url = audio_format['url'] if audio_format else None
    audio_size = f"{audio_format['filesize'] / (1024 * 1024):.2f} MB" if audio_format and audio_format['filesize'] else 'Unknown'

    # Get URL of the largest mp4 video file
    largest_video = video_formats[0] if video_formats else None
    video_url = largest_video['url'] if largest_video else None
    video_size = f"{largest_video['filesize'] / (1024 * 1024):.2f} MB" if largest_video and largest_video['filesize'] else 'Unknown'
    video_resolution = largest_video['resolution'] if largest_video else None

    return audio_url, video_url, 'mp4', video_size, audio_size, video_resolution

if __name__ == '__main__':
    video_info = get_video_info("https://youtu.be/e-kSGNzu0hM")
    audio_url, video_url, video_ext, video_size, audio_size, video_resolution = get_audio_and_video_urls(video_info)
    print(f"\nAudio URL (m4a): {audio_url}")
    print(f"Video URL ({video_ext}, {video_size}): {video_url}")
    print(f"Video resolution: {video_resolution}")

