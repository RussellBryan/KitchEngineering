from flask import Flask, render_template
from cocktail_calculator import cock_calc,  inds, cocktails, VARS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(cock_calc)

@app.route('/')
def home():
	return render_template('about.html')

@app.route('/cocktailcalculator')
def show():
	G = VARS()
	return render_template('cocktail_calculator.html', G=G)

if __name__ == '__main__':
    app.run()