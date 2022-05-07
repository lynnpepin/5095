import numpy as np
from main import main

Ns  = [2, 4, 8, 16, 32, 64, 128]
K   = 32
T   = 20
FPS = 30

print(f"Broadcast throughput ratio for variable N nodes communicating over {K} channels at {FPS} fps:")
print()
print("| N | throughput |")
print("| - | ---------- |")

for N in Ns:
    throughput = main(N=N, K=K, fps=FPS, total_time=T, simplify_render=2, ratelimit=False)
    print(f"| {N} | {throughput*100:.1f}% |")
