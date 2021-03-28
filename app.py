from flask import *
from flask_bootstrap import Bootstrap
from flask import session
import pickle
from recommendations_and_risk import RecommendAndEvaluateStocks
import sys

ticker_symbols = pickle.load(open("ticker_symbols.pkl", "rb"))
recs = RecommendAndEvaluateStocks()

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = b'\xea\x81X\xda@ ja\xcd\xbb\xf2\x1f\x9d\xda\x8d\x89"\xba\xb14\xda\x8eJ\xe1\xf4\x13U\xb8$\x10\xdf\xbf'

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
            value_each = int(float(future_value)//len(recommended_stocks))

            # how risky is the stock?
            risk = recs.evaluate_risk(str(ticker_symbol))

            if risk >= 4:
                risk_tag = 1
                secondary_stocks = list(recs.recommend_stock(1, str(ticker_symbol), float(value), float(future_value)).index)
            elif risk <= 2:
                risk_tag = 2
                secondary_stocks = list(recs.recommend_stock(4, str(ticker_symbol), float(value), float(future_value)).index)
            else:
                risk_tag = 0
                secondary_stocks = list(recs.recommend_stock(1, str(ticker_symbol), float(value), float(future_value)/4).index)\
                + list(recs.recommend_stock(2, str(ticker_symbol), float(value), float(future_value)/4).index)\
                + list(recs.recommend_stock(4, str(ticker_symbol), float(value), float(future_value)/4).index)\
                + list(recs.recommend_stock(5, str(ticker_symbol), float(value), float(future_value)/4).index)

            if int(future_risk) >= 4:
                future_risk_tag = 1
            elif int(future_risk) <= 2:
                future_risk_tag = 2
            else:
                future_risk_tag = 0

            risk_delta = abs(int(current_risk)-risk)
            if risk_delta >= 2:
                bad_risk_assessment_tag = 1
            else:
                bad_risk_assessment_tag = 0

            def validate_form(ticker_symbol, value, future_value):
                if not ( 0 < float(value) < 10000000 ):
                    print(f"Invalid value: {float(value)}", file=sys.stderr)
                    return False
                if str(ticker_symbol) not in ticker_symbols:
                    print(f"Invalid ticker: {str(ticker_symbol)}", file=sys.stderr)
                    return False
                return True

            session['stocks'] = recommended_stocks
            session['secondary'] = secondary_stocks

            # conditional checks to validate form 
            if validate_form(ticker_symbol, value, future_value):
                return redirect(url_for('recommendation_page', 
                                        ticker_symbol=ticker_symbol,
                                        value_each=value_each,
                                        risk_tag=risk_tag,
                                        future_risk_tag=future_risk_tag,
                                        bad_risk_assessment_tag=bad_risk_assessment_tag))
            else:
                return redirect(url_for('invalid_form'))
        except ValueError as e:
            print(f"{e}")
            return redirect(url_for('invalid_form'))

@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')

@app.route('/recommendation/<ticker_symbol>/<value_each>/<risk_tag>/<future_risk_tag>/<bad_risk_assessment_tag>', methods=['GET', 'POST'])
def recommendation_page(ticker_symbol, value_each, risk_tag, future_risk_tag, bad_risk_assessment_tag):
    stocks = session.get('stocks', None)
    secondary = session.get('secondary', None)
    if request.method == 'GET':
        return render_template('recommendation.html', 
                                ticker_symbol=ticker_symbol,
                                stocks=stocks,
                                value_each=value_each,
                                secondary_stocks=secondary,
                                risk_tag=risk_tag,
                                future_risk_tag=future_risk_tag,
                                bad_risk_assessment_tag=bad_risk_assessment_tag)

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)
if __name__ == "__main__":
    app.run()