import time
import sys

# 打印文件总数
total_files = 120_000_000
sampled_files = 1_200_000
print(f"text database file count: {total_files:,}")

# 模拟进度条
def progress_bar(duration=5):
    total_steps = 50  # 进度条步数
    for i in range(total_steps + 1):
        bar = '█' * i + '-' * (total_steps - i)
        sys.stdout.write(f"\rSampling... [{bar}] {i * 2}%")
        sys.stdout.flush()
        time.sleep(duration / total_steps)
    print()  # 换行

# 调用进度条函数
progress_bar()

# 打印抽样文件大小
print(f"Sampled file count: {sampled_files:,}")


