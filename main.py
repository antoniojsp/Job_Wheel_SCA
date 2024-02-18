from flask import Flask, render_template, request
from Job import Jobs

app = Flask(__name__)
data = Jobs("JS Job Wheel", "./credentials.json")


@app.route("/")
def index():
    titles = data.get_sheet_names()
    titles[0] += " (Current term)"
    names = ["------------"] + data.get_members_names()
    return render_template('index.html', title=titles[0], titles=titles, names=names)


@app.route("/member")
def select_member():
    pass


if __name__ == "__main__":
    app.run(debug=True)
