import uuid
import logging
import threading
from mcp.server.fastmcp import FastMCP
from services import YoutubeDownloader

mcp = FastMCP("youtube_downloader")
downloader = YoutubeDownloader()

@mcp.tool()
async def download_youtube_video(url: str) -> str:
    """Download a YouTube video to the user's Downloads folder asynchronously.

    Args:
        url: The YouTube video URL.
    Returns:
        A download_id to check status.
    """
    download_id = str(uuid.uuid4())

    downloader.set_download_status(download_id, 'in_progress')
    threading.Thread(
        target=downloader.download_video_task, 
        args=(url, download_id), 
        daemon=True).start()

    return f"Download started. Use download_id '{download_id}' to check status."

@mcp.tool()
async def check_download_status(download_id: str) -> str:
    """Check the status of a YouTube video download by download_id."""
    status = downloader.get_download_status(download_id)

    if status is None:
        return "Download ID not found."
    return f"Status for {download_id}: {status}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Running YouTube Downloader MCP server")
    mcp.run(transport='stdio') 