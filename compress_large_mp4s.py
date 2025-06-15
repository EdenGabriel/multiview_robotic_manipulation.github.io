import os
import subprocess

# 设置要遍历的视频目录和压缩阈值
video_dir = "static/videos/real-world/success"
max_size_mb = 97
crf = 28  # 推荐起始压缩系数

# 遍历文件夹查找大文件
def get_large_mp4_files(directory, size_limit_mb):
    large_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".mp4"):
                full_path = os.path.join(root, f)
                size_mb = os.path.getsize(full_path) / (1024 * 1024)
                if size_mb > size_limit_mb:
                    large_files.append((full_path, size_mb))
    return large_files

# 执行压缩命令
def compress_file(input_path, crf_val):
    output_path = input_path.replace(".mp4", "_compressed.mp4")
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vcodec", "libx264",
        "-crf", str(crf_val),
        "-preset", "slow",
        "-y", output_path
    ]
    print(f"\nCompressing {input_path} → {output_path}")
    subprocess.run(cmd)

# 主执行逻辑
if __name__ == "__main__":
    files = get_large_mp4_files(video_dir, max_size_mb)
    if not files:
        print("No .mp4 files larger than", max_size_mb, "MB.")
    else:
        for fpath, size in files:
            print(f"{fpath} ({size:.2f}MB)")
            compress_file(fpath, crf)
