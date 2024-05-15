import subprocess
from pathlib import Path

cwd = Path(__file__).parent
exts = ["json", "csv", "xlsx"]


def sync(src, dest):
    subprocess.run(
        [
            "rclone",
            "sync",
            "--exclude=.*",
            "--progress",
            "--s3-no-check-bucket",
            "--s3-chunk-size=256M",
            src,
            dest,
        ]
    )


def copy(src, dest):
    subprocess.run(
        [
            "rclone",
            "copyto",
            "--s3-no-check-bucket",
            "--s3-chunk-size=256M",
            src,
            dest,
        ]
    )


if __name__ == "__main__":
    for ext in exts:
        copy(cwd / f"outputs/population.{ext}", f"r2://fieldmaps-data/population.{ext}")
    sync(cwd / "outputs/population", "r2://fieldmaps-data/population")
