import json
import subprocess
from pathlib import Path


class VideoService:
    """Service for video processing."""

    def get_video_info(self, video_path: Path) -> dict:
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        metadata = json.loads(result.stdout)

        video_stream = next(
            stream
            for stream in metadata["streams"]
            if stream["codec_type"] == "video"
        )

        fps_parts = video_stream["r_frame_rate"].split("/")
        fps = float(fps_parts[0]) / float(fps_parts[1])

        return {
            "filename": video_path.name,
            "size_bytes": video_path.stat().st_size,
            "duration_seconds": round(
                float(metadata["format"]["duration"]),
                2,
            ),
            "fps": round(fps, 2),
            "width": video_stream["width"],
            "height": video_stream["height"],
            "codec": video_stream["codec_name"],
        }