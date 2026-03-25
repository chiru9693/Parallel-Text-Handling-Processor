import pandas as pd
from database import fetch_all

def export_csv():
    data = fetch_all()
    df = pd.DataFrame(data, columns=["ID","Text","Score","Sentiment","Time"])
    df.to_csv("output.csv", index=False)
    return "output.csv"