from flask import *
from flask_bootstrap import Bootstrap
import pickle

ticker_symbols = pickle.load(open("ticker_symbols.pkl", "rb"))

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
            # conditional checks to validate form 
            if float(value) > 0 and float(future_value) > 0 and float(future_value) < 1000000000 and str(ticker_symbol) in ticker_symbols:
                return redirect(url_for('recommendation_page', ticker_symbol=ticker_symbol, value=value, future_value=future_value, current_risk=current_risk, future_risk=future_risk))
            else:
                return redirect(url_for('invalid_form'))
        except:
            print("Failed submission")
            return redirect(url_for('invalid_form'))

@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')

@app.route('/recommendation/<ticker_symbol>/<value>/<future_value>/<current_risk>/<future_risk>', methods=['GET', 'POST'])
def recommendation_page(ticker_symbol, value, future_value, current_risk, future_risk):
    if request.method == 'GET':
        return render_template('recommendation.html', ticker_symbol=ticker_symbol, value=value, future_value=future_value, current_risk=current_risk, future_risk=future_risk)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)