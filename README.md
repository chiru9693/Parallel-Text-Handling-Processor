# 🚀 Parallel Text Handling Processor

## 📌 Project Overview

The **Parallel Text Handling Processor** is a data processing and sentiment analysis application built using Streamlit.
It allows users to upload large text-based datasets (TXT, CSV, Excel), process them efficiently using **parallel computing**, and perform **sentiment analysis** with real-time visualization.

The system is designed to handle **large datasets (50,000+ records)** while maintaining performance and stability.

---

## ✨ Features Implemented

### 📂 File Upload

* Supports:

  * TXT files
  * CSV files
  * Excel files
* Multiple file upload supported
* Handles large files using chunk processing
* Extracts text from all columns

---

### ⚙️ Processing

* Sequential (normal) processing
* Parallel processing using `ThreadPoolExecutor`
* Batch processing for large datasets (chunk size = 5000)
* Performance metrics displayed:

  * Normal execution time
  * Parallel execution time
  * CPU cores used

---

### 📊 Dashboard

* Total records processed
* Sentiment distribution:

  * Positive
  * Negative
  * Neutral
* Visualizations:

  * Bar chart
  * Pie chart
* Word-level analysis:

  * Total positive words
  * Total negative words
  * Total neutral words

---

### ✍️ Manual Text Analysis

* User can input custom text
* Displays:

  * Sentiment score
  * Final sentiment
  * Positive/Negative/Neutral word counts
* Visualized using:

  * Bar chart
  * Pie chart

---

### 🔍 Search Functionality

* Search by keyword
* Filter by:

  * Sentiment
  * Minimum score
* Smart fallback:

  * If no database result found → analyzes keyword and returns result

---

### 📁 Export

* Export processed data to CSV
* Download directly from UI

---

### 🧹 UI Improvements

* Reset/Clear database button
* File count display
* Total extracted records display
* Progress bar + loading spinner

---

## ⚡ Parallel Processing Logic

The system processes text in two modes:

### 1. Sequential Processing

* Each record is processed one by one
* Slower for large datasets

### 2. Parallel Processing

* Uses `ThreadPoolExecutor`
* Multiple threads process records simultaneously
* Utilizes multiple CPU cores

### 🧠 Key Insight

* For small datasets → parallel may be slower (due to thread overhead)
* For large datasets → parallel is significantly faster

---

## 😊 Sentiment Analysis Logic

The system uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)**.

### How it works:

* Text is cleaned and tokenized
* VADER computes a **compound score**
* Words are checked against the VADER lexicon

### Enhancements implemented:

* ✔ Repeated words handling
  Example: `good good bad → Positive`
* ✔ Negation handling
  Example: `not good → Negative`
* ✔ Intensifier handling
  Example: `very good → Strong Positive`
* ✔ Word-level counting:

  * Positive words
  * Negative words
  * Neutral words

---

## 📊 Dataset Details

* Supports any textual dataset
* Tested with:

  * Random text datasets
  * CSV/Excel structured data
  * Large datasets (50K+ records)
* Extracts all textual values from uploaded files

---

## ⚡ Performance Comparison

| Mode       | Behavior                     |
| ---------- | ---------------------------- |
| Sequential | Slower, processes one-by-one |
| Parallel   | Faster for large datasets    |

### Example:

* 50K records:

  * Sequential → Higher time
  * Parallel → Reduced time

---

## ⚠️ Edge Cases Handled

* Empty file upload
* Invalid file format
* Large file handling
* Memory overflow prevention
* No data extracted scenario
* Empty user input
* No search results → fallback logic
* Repeated words in text
* Neutral word detection

---

## 🧪 Dataset Handling

* Supports up to **50,000 records safely**
* Uses:

  * Chunk processing (CSV)
  * Batch processing (5000 records)
* Prevents crashes and improves performance

---

## ▶️ Steps to Run the Project

### 1. Install dependencies

```bash
pip install streamlit pandas altair vaderSentiment
```

### 2. Activate virtual environment (optional)

```bash
.\.venv\Scripts\activate
```

### 3. Run the application

```bash
streamlit run app.py
```

### 4. Open in browser

```
http://localhost:8501
```

---

## 🔍 Performance & Optimization

* Batch processing reduces memory usage
* Chunk processing avoids loading full dataset
* Parallel execution improves speed
* Database operations optimized (bulk insert)

---

## 🚀 Future Improvements

* Machine Learning / Deep Learning models
* Support for 1M+ datasets
* Cloud deployment (AWS / Azure)
* Real-time streaming data analysis
* Advanced NLP (context-aware sentiment)

---

## 🎯 Conclusion

This project demonstrates:

* Efficient large dataset handling
* Parallel computing
* Real-time sentiment analysis
* Interactive data visualization

It is designed to be **scalable, efficient, and user-friendly**, making it suitable for real-world data analysis applications.

---
