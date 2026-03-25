from concurrent.futures import ThreadPoolExecutor
from sentiment import analyze
from database import insert
import time
import os

def process_texts(texts):

    def process(text):
        score, sentiment, _, _ = analyze(text)
        return (text, score, sentiment)

    start_normal = time.time()

    normal_results = []
    for t in texts:
        normal_results.append(process(t))

    normal_time = round(time.time() - start_normal, 2)

    start_parallel = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        parallel_results = list(executor.map(process, texts))

    parallel_time = round(time.time() - start_parallel, 2)

    # 🔥 INSERT AFTER PROCESSING (NOT INSIDE LOOP)
    for text, score, sentiment in parallel_results:
        insert(text, score, sentiment)

    return {
        "normal_time": normal_time,
        "parallel_time": parallel_time,
        "cores_used": os.cpu_count()
    }