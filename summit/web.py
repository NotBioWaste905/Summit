from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from discussion import Discussion
from langchain_community.chat_models import ChatOpenAI

app = Flask(__name__)

# Directory to store discussion files
DISCUSSIONS_DIR = Path("discussions")
DISCUSSIONS_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    # Get all discussion files
    discussions = []
    for file in DISCUSSIONS_DIR.glob("*.md"):
        with open(file, "r") as f:
            title = f.readline().strip("# \n")
            discussions.append({"title": title, "filename": file.name})
    return render_template("index.html", discussions=discussions)


@app.route("/discussion/<filename>")
def view_discussion(filename):
    filepath = DISCUSSIONS_DIR / filename
    if not filepath.exists():
        return "Discussion not found", 404

    with open(filepath, "r") as f:
        content = f.read()
    return render_template("discussion.html", content=content)


@app.route("/new", methods=["GET", "POST"])
def new_discussion():
    if request.method == "POST":
        topic = request.form["topic"]
        participants = {
            "Alice": {"model": ChatOpenAI(model="gpt-4o-mini"), "finished": False},
            "Bob": {"model": ChatOpenAI(model="gpt-4o-mini"), "finished": False},
            "Charlie": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
            "Dave": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
            "Eve": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
        }

        disc = Discussion(participants=participants, topic=topic)
        disc.run()

        return redirect(url_for("index"))

    return render_template("new_discussion.html")


if __name__ == "__main__":
    app.run(debug=True, port=5555)
