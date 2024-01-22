from flask import Flask, render_template
from Job import Jobs

app = Flask(__name__)
data = Jobs("Copy of JS Job Wheel", "./credentials.json")


@app.route("/")
def index():
    titles = data.get_sheet_names()
    names = data.get_members_names()
    print(data.get_assigned_jobs())
    return render_template('index.html', title=titles[0], titles=titles, names=names)


if __name__ == "__main__":
    app.run(debug=True)
