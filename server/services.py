import os
import subprocess
import yt_dlp
import threading
from logger import MCPLogger

class YoutubeDownloader():

    def __init__(self):
        self.download_status: dict[str, str] = {}
        self.status_lock = threading.Lock()
        self.downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    def _check_ffmpeg(self) -> bool:
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return True
        except FileNotFoundError:
            return False

    def download_video_task(self, url: str, download_id: str):
        try:
            self.set_download_status(download_id, 'in_progress')
            if not self._check_ffmpeg():
                self.set_download_status(download_id, 'error: ffmpeg not installed')
                return
            if not os.path.exists(self.downloads_folder):
                os.makedirs(self.downloads_folder)
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'outtmpl': os.path.join(self.downloads_folder, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',
                'logger': MCPLogger(),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.set_download_status(download_id, 'completed')
        except Exception as e:
            self.set_download_status(download_id, f'error: {str(e)}')

    def get_download_status(self, download_id: str) -> str:
        with self.status_lock:
            return self.download_status.get(download_id, 'not found')
    
    def set_download_status(self, download_id: str, status: str):
        with self.status_lock:
            self.download_status[download_id] = status







