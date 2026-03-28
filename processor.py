from concurrent.futures import ProcessPoolExecutor
from sentiment import analyze
from database import insert
import time
import os

# 🔥 IMPORTANT: function must be outside
def process(text):
    score, sentiment, _, _ = analyze(text)
    return (text, score, sentiment)


def process_texts(texts):

    # ================= NORMAL =================
    start_normal = time.time()

    normal_results = []
    for t in texts:
        normal_results.append(process(t))

    normal_time = round(time.time() - start_normal, 2)

    # ================= PARALLEL =================
    start_parallel = time.time()

    # 🔥 REAL PARALLEL (MULTIPROCESSING)
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        parallel_results = list(executor.map(process, texts))

    parallel_time = round(time.time() - start_parallel, 2)

    # ================= INSERT =================
    for text, score, sentiment in parallel_results:
        insert(text, score, sentiment)

    return {
        "normal_time": normal_time,
        "parallel_time": parallel_time,
        "cores_used": os.cpu_count()
    }
