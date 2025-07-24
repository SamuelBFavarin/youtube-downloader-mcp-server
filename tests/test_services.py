import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the server directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from services import YoutubeDownloader

class TestYoutubeDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = YoutubeDownloader()

    @patch('services.subprocess.run')
    def test_check_ffmpeg_installed(self, mock_run):
        mock_run.return_value = MagicMock()
        self.assertTrue(self.downloader._check_ffmpeg())
        mock_run.assert_called_once_with(['ffmpeg', '-version'], capture_output=True)

    @patch('services.subprocess.run', side_effect=FileNotFoundError)
    def test_check_ffmpeg_not_installed(self, mock_run):
        self.assertFalse(self.downloader._check_ffmpeg())

    def test_set_and_get_download_status(self):
        self.downloader.set_download_status('abc', 'in_progress')
        status = self.downloader.get_download_status('abc')
        self.assertEqual(status, 'in_progress')

    @patch('services.yt_dlp.YoutubeDL')
    @patch.object(YoutubeDownloader, '_check_ffmpeg', return_value=True)
    def test_download_video_task_success(self, mock_ffmpeg, mock_ytdlp):
        mock_ytdlp.return_value.__enter__.return_value.download.return_value = None
        self.downloader.download_video_task('http://test.url', 'xyz')
        status = self.downloader.get_download_status('xyz')
        self.assertEqual(status, 'completed')

    @patch('services.yt_dlp.YoutubeDL', side_effect=Exception('fail'))
    @patch.object(YoutubeDownloader, '_check_ffmpeg', return_value=True)
    def test_download_video_task_error(self, mock_ffmpeg, mock_ytdlp):
        self.downloader.download_video_task('http://test.url', 'err')
        status = self.downloader.get_download_status('err')
        self.assertTrue(status.startswith('error:'))

    @patch.object(YoutubeDownloader, '_check_ffmpeg', return_value=False)
    def test_download_video_task_no_ffmpeg(self, mock_ffmpeg):
        self.downloader.download_video_task('http://test.url', 'noffmpeg')
        status = self.downloader.get_download_status('noffmpeg')
        self.assertEqual(status, 'error: ffmpeg not installed')

if __name__ == '__main__':
    unittest.main() 