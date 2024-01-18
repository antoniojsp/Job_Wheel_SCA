from flask import Flask, render_template
from Job import Jobs

app = Flask(__name__)
data = Jobs("Copy of JS Job Wheel", "./credentials.json")


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)