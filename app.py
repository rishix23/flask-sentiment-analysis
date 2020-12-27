from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:superuser@localhost/test'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://umpsmgfpmnbacd:a47651ce2664dcb9fb8e55ccc5f34e4aca6b3ce9d0bd04ccc8a7b774e2de9219@ec2-54-208-233-243.compute-1.amazonaws.com:5432/d3b5k0aspcf3bq'
    app.debug = False

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

@app.route('/test')
def test():
    return render_template("index1.html")

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


