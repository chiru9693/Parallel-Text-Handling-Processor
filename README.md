# 🚀 Parallel Text Handling Processor

## 📌 Project Overview

The **Parallel Text Handling Processor** is a high-performance data processing and sentiment analysis application built using **Streamlit**.

It enables users to upload large text datasets (TXT, CSV, Excel), process them efficiently using **parallel computing**, perform **sentiment analysis**, and generate **downloadable/email reports** with real-time visualization.

The system is optimized to handle **large datasets (50,000+ records)** with stability and performance.

---

## ✨ Features Implemented

### 📂 File Upload
- Supports:
  - TXT files
  - CSV files
  - Excel files
- Multiple file upload supported
- Chunk-based reading for large files
- Extracts text from all columns

---

### ⚙️ Processing Engine

- Sequential (Normal) Processing
- Parallel Processing using `ProcessPoolExecutor`
- Batch Processing (Chunk size = 5000)
- Performance Metrics:
  - Normal execution time
  - Parallel execution time
  - CPU cores used

---

### ⚡ Data Optimization (NEW)

- Duplicate record removal
- Reduces redundant data
- Improves processing efficiency
- Metrics displayed:
  - Original records count
  - Optimized records count
  - Optimization time

---

### 📊 Dashboard

- Total records processed
- Sentiment distribution:
  - Positive
  - Negative
  - Neutral
- Visualizations:
  - Bar Chart
  - Pie Chart
- Word-level analytics:
  - Total positive words
  - Total negative words
  - Total neutral words

---

### ✍️ Manual Text Analysis

- Analyze custom user input
- Displays:
  - Sentiment score
  - Final sentiment
  - Positive / Negative / Neutral word counts
- Visualizations:
  - Bar chart
  - Pie chart

---

### 🔍 Smart Search

- Keyword-based search
- Filters:
  - Sentiment
  - Minimum score
- Intelligent fallback:
  - If no result → real-time sentiment analysis of keyword

---

### 📁 Export

- Export processed data to CSV
- Download directly from UI

---

### 📧 Email Report (NEW)

- Send CSV reports via email
- Uses SMTP (Gmail App Password authentication)
- Supports:
  - Database data report
  - Search results report

---

### 🧹 UI Enhancements

- Reset/Clear database button
- File count display
- Total extracted records display
- Progress bar
- Loading spinner

---

## ⚡ Parallel Processing Logic

### 1. Sequential Processing
- Processes records one-by-one
- Slower for large datasets

### 2. Parallel Processing
- Uses `ProcessPoolExecutor`
- Utilizes multiple CPU cores
- Processes records concurrently

### 🧠 Key Insight

- Small datasets → Parallel slower (overhead cost)
- Large datasets → Parallel significantly faster

---

## 😊 Sentiment Analysis Logic

Uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)**.

### Workflow:
- Text cleaning & tokenization
- Compound score calculation
- Lexicon-based word evaluation

### Enhancements:

- ✔ Repeated words handling  
  Example: `good good bad → Positive`

- ✔ Negation handling  
  Example: `not good → Negative`

- ✔ Intensifier handling  
  Example: `very good → Strong Positive`

- ✔ Word-level classification:
  - Positive words
  - Negative words
  - Neutral words

---

## 📊 Dataset Support

- Supports structured & unstructured text data
- Tested with:
  - CSV datasets
  - Excel datasets
  - Large datasets (50K+ records)
- Extracts all textual values dynamically

---

## ⚡ Performance Comparison

| Mode       | Behavior                     |
|-----------|-----------------------------|
| Sequential | Slower, single-threaded     |
| Parallel   | Faster for large datasets   |

### Example:
- 50K records:
  - Sequential → Higher time
  - Parallel → Reduced time

---

## ⚠️ Edge Cases Handled

- Empty file upload
- Invalid file formats
- Large dataset handling
- Memory overflow prevention
- No extracted data scenario
- Empty user input
- No search results (fallback logic)
- Duplicate data removal
- Neutral word detection

---

## 🧪 Dataset Handling

- Supports up to **50,000 records safely**
- Uses:
  - Chunk processing (CSV)
  - Batch processing (5000 records)
- Prevents crashes and improves performance

---

## ▶️ Steps to Run the Project

### 1. Install dependencies

```bash
pip install streamlit pandas altair vaderSentiment
