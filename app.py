from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils import (
    get_stock_price,
    get_news_sentiment,
    compare_stocks,
    process_speech_query,
    set_price_alert,
    check_price_alerts,
    get_moving_average,
    convert_currency,
    investment_advice,
    predict_stock_price,
    financial_qa,
)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data.get('question')

    if not query:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        # Check different query types and handle accordingly
        if "compare" in query:
            symbols = data.get('symbols', '').split(',')
            if not symbols:
                return jsonify({"error": "No stock symbols provided"}), 400
            generated_answer = compare_stocks([symbol.strip() for symbol in symbols])
            actual_answer = None
            context = "Comparison of stock prices for the provided symbols."
        
        elif "set alert" in query:
            stock_symbol = data.get('stock_symbol')
            target_price = data.get('target_price')
            if not stock_symbol or not target_price:
                return jsonify({"error": "Stock symbol and target price required for setting an alert"}), 400
            generated_answer = set_price_alert(stock_symbol, target_price)
            actual_answer = None
            context = f"Price alert set for {stock_symbol} at {target_price}."
        
        elif "check alerts" in query:
            generated_answer = check_price_alerts()
            actual_answer = None
            context = "Checking all active price alerts."
        
        elif "moving average" in query:
            stock_symbol = data.get('stock_symbol')
            period = data.get('period')
            if not stock_symbol or not period:
                return jsonify({"error": "Stock symbol and period required for moving average"}), 400
            generated_answer = get_moving_average(stock_symbol, period)
            actual_answer = None
            context = f"Moving average for {stock_symbol} over {period} period."
        
        elif "convert currency" in query:
            amount = data.get('amount')
            from_currency = data.get('from_currency')
            to_currency = data.get('to_currency')
            if not amount or not from_currency or not to_currency:
                return jsonify({"error": "Amount, from_currency, and to_currency required for conversion"}), 400
            generated_answer = convert_currency(amount, from_currency, to_currency)
            actual_answer = None
            context = f"Converted {amount} {from_currency} to {to_currency}."
        
        elif "investment advice" in query:
            risk_level = data.get('risk_level')
            if not risk_level:
                return jsonify({"error": "Risk level required for investment advice"}), 400
            generated_answer = investment_advice(risk_level)
            actual_answer = None
            context = f"Investment advice for risk level {risk_level}."
        
        elif "predict" in query:
            stock_symbol = data.get('stock_symbol')
            days_ahead = data.get('days_ahead')
            if not stock_symbol or not days_ahead:
                return jsonify({"error": "Stock symbol and days ahead required for prediction"}), 400
            generated_answer = predict_stock_price(stock_symbol, days_ahead)
            actual_answer = None
            context = f"Stock price prediction for {stock_symbol} for {days_ahead} days ahead."
        
        elif "speech" in query:
            generated_answer = process_speech_query()
            actual_answer = None
            context = "Processed speech query."
        
        else:
            # Default to financial QA system if no specific query type is matched
            try: 
                generated_answer = financial_qa(query)
                symbol = data.get('symbol')  # This may still be None
                print(symbol)
                actual_answer = get_stock_price(symbol)
                context = "Financial question answered using the financial QA system."
            except: 
                actual_answer = "No stock symbol provided."
            

        # Return the response as expected by the front-end
        return jsonify({
            "generatedAnswer": generated_answer,
            "actualAnswer": actual_answer,
            "context": context
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
