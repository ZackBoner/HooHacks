from flask import *
from flask_bootstrap import Bootstrap

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
            current_risk = request.form.get("current_risk", None)
            future_risk = request.form.get("future_risk", None)
            return redirect(url_for('recommendation_page', ticker_symbol=ticker_symbol, value=value, current_risk=current_risk, future_risk=future_risk))
        except:
            print("Failed submission")
            return redirect(url_for('home_page'))

@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')

@app.route('/recommendation/<ticker_symbol>/<value>/<current_risk>/<future_risk>', methods=['GET', 'POST'])
def recommendation_page(ticker_symbol, value, current_risk, future_risk):
    if request.method == 'GET':
        return render_template('recommendation.html', ticker_symbol=ticker_symbol, value=value, current_risk=current_risk, future_risk=future_risk)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)