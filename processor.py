from concurrent.futures import ProcessPoolExecutor
from sentiment import analyze
from database import insert
import time
import os

# ================= PROCESS FUNCTION =================
def process(text):
    score, sentiment, _, _ = analyze(text)
    return (text, score, sentiment)


# ================= TEXT STORAGE IMPROVER =================
def optimize_texts(texts):
    start = time.time()

    # 🔥 REMOVE DUPLICATES (SET → O(1))
    unique_texts = list(set(texts))

    end = time.time()

    return unique_texts, round(end - start, 4)


# ================= MAIN =================
def process_texts(texts):

    # 🔥 APPLY OPTIMIZATION
    optimized_texts, optimize_time = optimize_texts(texts)

    # ================= NORMAL =================
    start_normal = time.time()

    normal_results = []
    for t in optimized_texts:
        normal_results.append(process(t))

    normal_time = round(time.time() - start_normal, 2)

    # ================= PARALLEL =================
    start_parallel = time.time()

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        parallel_results = list(executor.map(process, optimized_texts))

    parallel_time = round(time.time() - start_parallel, 2)

    # ================= INSERT =================
    for text, score, sentiment in parallel_results:
        insert(text, score, sentiment)

    return {
        "normal_time": normal_time,
        "parallel_time": parallel_time,
        "cores_used": os.cpu_count(),
        "original_count": len(texts),
        "optimized_count": len(optimized_texts),
        "optimize_time": optimize_time
    }
