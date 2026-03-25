from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import re

analyzer = SentimentIntensityAnalyzer()

def analyze(text):

    clean = re.sub(r"[^\w\s]", "", text.lower())
    words = clean.split()

    scores = analyzer.polarity_scores(clean)
    compound = scores["compound"]

    word_counts = Counter(words)

    pos_count = 0
    neg_count = 0

    # 🔥 COUNT POSITIVE / NEGATIVE WORDS
    for word, count in word_counts.items():
        if word in analyzer.lexicon:
            score = analyzer.lexicon[word]

            if score > 0:
                pos_count += count
            elif score < 0:
                neg_count += count

    # 🔥 FIX: NOT HANDLING (STRONG NEGATIVE)
    if "not" in words:
        compound -= 0.6   # stronger effect

    # 🔥 FIX: VERY HANDLING (BOOST POSITIVE)
    if "very" in words:
        compound += 0.4

    compound = max(min(compound, 1), -1)

    score = round(compound * 10)

    if compound > 0:
        sentiment = "Positive"
    elif compound < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return score, sentiment, pos_count, neg_count