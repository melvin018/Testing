import requests
import matplotlib.pyplot as plt
from transformers import T5ForConditionalGeneration, T5Tokenizer
import time
import torch
import speech_recognition as sr
import os 
from langchain_community.llms import HuggingFaceHub
from transformers import pipeline

# Load Google Flan-T5 Model and Tokenizer for Q&A

os.environ["HUGGINGFACEHUB_API_TOKEN"]="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"
llm_huggingface=HuggingFaceHub(repo_id="google/flan-t5-large",model_kwargs={"temperature":0,"max_length":128})
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

# 1. Get Stock Price using Alpha Vantage API
def get_stock_price(symbol):
    api_key = "65FIIVKB83908VDO"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    print(f" the api response : {data}")
    try:
        latest_time = list(data['Time Series (5min)'].keys())[0]
        latest_price = data['Time Series (5min)'][latest_time]['1. open']
        return latest_price
    except KeyError:
        return f"Error fetching data for {symbol}. Please check the stock symbol."

# 2. Get Financial News Sentiment
def get_news_sentiment(stock_symbol):
    # Example news headlines for demonstration
    news_headlines = [
        f"{stock_symbol} stock surges after earnings beat expectations",
        f"{stock_symbol} faces challenges due to rising competition"
    ]
    
    for headline in news_headlines:
        sentiment = sentiment_pipeline(headline)[0]
        print(f"Headline: {headline}")
        print(f"Sentiment: {sentiment['label']}, Confidence: {sentiment['score']:.2f}\n")

# 3. Compare Stocks
def compare_stocks(stock_symbols):
    data = {}
    
    for symbol in stock_symbols:
        stock_price = get_stock_price(symbol)
        data[symbol] = stock_price
        print(f"{symbol}: ${stock_price}")

    # Display comparison visually
    plt.figure(figsize=(8, 4))
    plt.bar(data.keys(), [float(data[symbol]) for symbol in data.keys()])
    plt.xlabel('Stock Symbol')
    plt.ylabel('Stock Price (USD)')
    plt.title('Stock Price Comparison')
    plt.show()

# 4. Set and Check Price Alerts
alerts = {}

def set_price_alert(stock_symbol, target_price):
    alerts[stock_symbol] = target_price
    print(f"Price alert set for {stock_symbol} at ${target_price}")

def check_price_alerts():
    while True:
        for stock_symbol, target_price in alerts.items():
            current_price = get_stock_price(stock_symbol)
            if float(current_price) >= target_price:
                print(f"Alert! {stock_symbol} has reached ${current_price}, which is above your target of ${target_price}")
                del alerts[stock_symbol]  # Remove alert after triggering
        time.sleep(60)  # Check every 60 seconds

# 5. Historical Data Analysis (Moving Averages)
def get_moving_average(stock_symbol, period='50'):
    api_key = "65FIIVKB83908VDO"
    url = f"https://www.alphavantage.co/query?function=SMA&symbol={stock_symbol}&interval=daily&time_period={period}&series_type=close&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    try:
        sma = list(data['Technical Analysis: SMA'].values())[0]['SMA']
        print(f"{period}-day Moving Average for {stock_symbol}: ${sma}")
        return sma
    except KeyError:
        return "Error fetching moving average."

# 6. Currency Conversion
def convert_currency(amount, from_currency, to_currency):
    api_key = "65FIIVKB83908VDO"
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    try:
        exchange_rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
        converted_amount = float(amount) * float(exchange_rate)
        print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
        return converted_amount
    except KeyError:
        return "Error fetching exchange rate."

# 7. Investment Advice
def investment_advice(risk_level):
    if risk_level.lower() == "conservative":
        return "We recommend a conservative portfolio with bonds and blue-chip stocks."
    elif risk_level.lower() == "moderate":
        return "A moderate portfolio might include a mix of large-cap stocks and bonds."
    elif risk_level.lower() == "aggressive":
        return "For aggressive investors, we suggest looking at growth stocks and emerging markets."
    else:
        return "Please specify a risk level: conservative, moderate, or aggressive."

# 8. Predictive Stock Price Forecasting (Simple Moving Average)
def predict_stock_price(stock_symbol, days_ahead):
    current_price = float(get_stock_price(stock_symbol))
    sma_50 = float(get_moving_average(stock_symbol, '50'))
    sma_200 = float(get_moving_average(stock_symbol, '200'))
    
    trend = "upward" if sma_50 > sma_200 else "downward"
    prediction = current_price * (1 + (0.02 if trend == "upward" else -0.02)) ** days_ahead
    print(f"Based on a {trend} trend, {stock_symbol} could be ${prediction:.2f} in {days_ahead} days.")
    return prediction

# 9. Speech-to-Text Functionality
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"User Query: {query}")
        return query
    except sr.UnknownValueError:
        return "Sorry, I could not understand your speech."
    except sr.RequestError:
        return "Sorry, the speech service is unavailable."

# 10. Q&A Function using Google Flan-T5
def financial_qa(question):
    input_text = f"question: {question}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    return answer

# Example Use Case: Integrating Speech Input
def process_speech_query():
    query = speech_to_text()
    if "compare" in query:
        compare_stocks(["AAPL", "TSLA", "MSFT"])
    elif "Tesla" in query:
        get_stock_price("TSLA")
    else:
        financial_qa(query)
