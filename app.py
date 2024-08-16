from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import twitter

app = Flask(__name__)

ENV = 'dev'

# TODO:
# UPDATE API URIS

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tweets(db.Model):
    __tablename__ = 'Tweets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)

    def __init__(self, name):
        self.name = name

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        user = request.form["name"]
        return render_template("index.html", submission=user)
    else:
        return render_template("index.html")

@app.route('/twitterScrap')
def twitterScrap():
    twitter.create_webdriver_instance()
    return f"Should work!"

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        if name == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Tweets).filter(Tweets.name == name).count() == 0:
            data = Tweets(name)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted this Tweet before.')

#AJAX METHOD

# @app.route('/')
# def index():
# 	return render_template('form.html')


# @app.route('/process', methods=['POST'])
# def process():

# 	email = request.form['email']
# 	name = request.form['name']

# 	if name and email:
# 		newName = name[::-1]

# 		return jsonify({'name' : newName})

# 	return jsonify({'error' : 'Missing data!'})


#SAMPLE METHODS

# #return variable into html
# @app.route("/<name>")
# def home(name):
#      return render_template("index.html", content=["tim", "joe", "bill"])



# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

# @app.route('/admin/')
# def admin():
#     return redirect(url_for("user", name="Admin!"))

# @app.route('/submit', methods =['POST'])
# def submit():
#     if request.method == 'POST':
#         customer = request.form['customer']
#         print(customer)
#         return render_template('sucess.html')

if __name__ == '__main__':
    app.run()


