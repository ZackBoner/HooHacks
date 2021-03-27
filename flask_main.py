from flask import *

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def submission_form():
    return render_template('form.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)