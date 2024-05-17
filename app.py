from flask import Flask, render_template, request, redirect, url_for, jsonify,send_from_directory
import pandas as pd

app = Flask(__name__)

# Define the path to the CSV file
CSV_FILE = "data.csv"

# Define column names for the CSV file
columns = ["logo", "title", "description", "link"]


@app.route("/static/videos/source.mp4", methods=["GET", "POST"])
def serve_video():
    return send_from_directory(app.static_folder, "source.mp4")


# Define the route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "sam" and password == "admin":
            return redirect(url_for("main"))
        else:
            return render_template("index.html", message="Invalid username or password")
    return render_template("index.html", message="")


@app.route("/")
def index():
    return render_template("index.html")


# Define the route to render the main page (main.html)
@app.route("/main")
def main():
    return render_template("main.html")


# Define the route to fetch tools data from the CSV file
@app.route("/get_tools", methods=["GET"])
def get_tools():
    try:
        df = pd.read_csv(CSV_FILE, names=columns, delimiter="\t")
        data = df.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


# Define the route to handle form submission for adding a tool
@app.route("/add_tool", methods=["POST"])
def add_tool():
    try:
        # Get JSON data from request
        data = request.get_json()
        logo = data.get("logo")
        title = data.get("title")
        description = data.get("description")
        link = data.get("link")

        # Append data to CSV file
        with open(CSV_FILE, "a") as f:
            f.write(f"{logo}\t{title}\t{description}\t{link}\n")

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)
