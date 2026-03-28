import pandas as pd
from database import fetch_all

def export_csv():
    data = fetch_all()

    df = pd.DataFrame(
        data,
        columns=["ID", "Text", "Score", "Sentiment", "Created_At"]
    )

    # 🔥 FIX: Convert to datetime format
    df["Created_At"] = pd.to_datetime(df["Created_At"])

    # 🔥 OPTIONAL: Format nicely for Excel
    df["Created_At"] = df["Created_At"].dt.strftime("%Y-%m-%d %H:%M:%S")

    file = "output.csv"
    df.to_csv(file, index=False, encoding="utf-8-sig")

    return file
