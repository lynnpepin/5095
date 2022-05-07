import numpy as np
from main import main

N=60
K=10
T=20
FPSes = [2,3,6,12,30,60,120]


print(f"Broadcast throughput ratio for {N} nodes communicating over {K} channels over {T} seconds, ")
print("for different values of FPS.")
print()
print("| FPS | dt | throughput |")
print("| --- | -- | ---------- |")

for fps in FPSes:
    throughput = main(N=N, K=K, fps=fps, total_time=T, simplify_render=2, ratelimit=False)
    print(f"| {fps} | {1/fps:.3f} | {throughput*100:.1f}% |")
