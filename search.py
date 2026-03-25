from database import conn
from sentiment import analyze
from datetime import datetime

def search(keyword="", sentiment=None, min_score=None):

    cursor = conn.cursor()

    query = "SELECT * FROM reviews WHERE 1=1"
    params = []

    if keyword:
        words = keyword.lower().split()

        conditions = []
        for word in words:
            conditions.append("LOWER(text) LIKE ?")
            params.append(f"%{word}%")

        query += " AND (" + " OR ".join(conditions) + ")"

    if sentiment:
        query += " AND sentiment = ?"
        params.append(sentiment)

    if min_score is not None:
        query += " AND score >= ?"
        params.append(min_score)

    cursor.execute(query, params)
    results = cursor.fetchall()

    # 🔥 RANKING (IMPORTANT FIX)
    if keyword and results:
        words = keyword.lower().split()

        ranked = []
        for row in results:
            text = row[1].lower()
            rank = sum(text.count(word) for word in words)
            ranked.append((rank, row))

        ranked.sort(reverse=True, key=lambda x: x[0])
        results = [r[1] for r in ranked]

    # 🔥 FALLBACK
    if not results and keyword:
        score, sent, _, _ = analyze(keyword)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [(0, keyword, score, sent, timestamp)]

    return results