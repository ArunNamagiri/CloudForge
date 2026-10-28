import multiprocessing
import time

def burn_cpu(seconds):
    end = time.time() + seconds
    while time.time() < end:
        sum(i * i for i in range(1000))

if __name__ == "__main__":
    workers = min(2, multiprocessing.cpu_count())
    print(f"Starting {workers} CPU workers for 120 seconds...")

    with multiprocessing.Pool(workers) as pool:
        pool.map(burn_cpu, [120] * workers)

    print("CPU-load test completed.")
