import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 AI Trading Dashboard (44/200 SMA Strategy)")

symbols = st.text_input("Enter stock symbols (comma separated)", value="RELIANCE.NS,TCS.NS,INFY.NS").split(",")

def calculate_signals(df):
    df["SMA44"] = df["Close"].rolling(window=44).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()
    df["Signal"] = df["SMA44"] > df["SMA200"]
    return df

for symbol in symbols:
    symbol = symbol.strip().upper()
    if not symbol:
        continue
    df = yf.download(symbol, period="1y", interval="1d")
    if df.empty:
        st.warning(f"No data for {symbol}")
        continue
    df = calculate_signals(df)
    st.subheader(f"📊 {symbol}")
    st.line_chart(df[["Close", "SMA44", "SMA200"]])
    signal = df["Signal"].iloc[-1]
    if signal:
        st.success("✅ Buy Signal")
    else:
        st.error("❌ No Buy Signal")
