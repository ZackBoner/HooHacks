from flask import *
from flask_bootstrap import Bootstrap
import pickle
from recommendations_and_risk import RecommendAndEvaluateStocks
import sys

ticker_symbols = pickle.load(open("ticker_symbols.pkl", "rb"))
recs = RecommendAndEvaluateStocks()

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET', 'POST'])
def submission_form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        try:
            ticker_symbol = request.form.get("ticker_symbol", None)
            value = request.form.get("value", None)
            future_value = request.form.get("future_value", None)
            current_risk = request.form.get("current_risk", None)
            future_risk = request.form.get("future_risk", None)

            #Zack put in ML code here

            #output format e.g. ['GME', 'AAPL', 'MSE', ...]
            recommended_stocks = list(recs.recommend_stock(int(future_risk), str(ticker_symbol), float(value), float(future_value)).index)
            stocks = '-'.join(recommended_stocks)

            # how much the user's perceived risk deviates from the risk we predict for the stock
            risk_delta = recs.evaluate_perceived_risk(int(current_risk), str(ticker_symbol))

            def validate_form(ticker_symbol, value, future_value):
                if not ( 0 < float(value) < 10000000 ):
                    print(f"Invalid value: {float(value)}", file=sys.stderr)
                    return False
                if str(ticker_symbol) not in ticker_symbols:
                    print(f"Invalid ticker: {str(ticker_symbol)}", file=sys.stderr)
                    return False
                return True

            # conditional checks to validate form 
            if validate_form(ticker_symbol, value, future_value):
                return redirect(url_for('recommendation_page', 
                                        ticker_symbol=ticker_symbol, 
                                        value=value, 
                                        future_value=future_value, 
                                        current_risk=current_risk, 
                                        future_risk=future_risk,
                                        stocks=stocks))
            else:
                return redirect(url_for('invalid_form'))
        except:
            print("Failed submission")
            return redirect(url_for('invalid_form'))

@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')

@app.route('/recommendation/<ticker_symbol>/<value>/<future_value>/<current_risk>/<future_risk>/<stocks>', methods=['GET', 'POST'])
def recommendation_page(ticker_symbol, value, future_value, current_risk, future_risk, stocks):
    if request.method == 'GET':
        return render_template('recommendation.html', 
                                ticker_symbol=ticker_symbol, 
                                value=value, 
                                future_value=future_value, 
                                current_risk=current_risk, 
                                future_risk=future_risk,
                                stocks=stocks)

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)
if __name__ == "__main__":
    app.run(debug=True)