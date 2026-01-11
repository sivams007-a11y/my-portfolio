from flask import Flask, render_template, request, redirect, session, send_from_directory
import json, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

PROFILE_FILE = "profile.json"
IMAGE_FOLDER = "static/images"
FILE_FOLDER = "static/files"

# ---------- Helpers ----------
def load_profile():
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profile(data):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- Routes ----------
@app.route("/")
def home():
    profile = load_profile()
    return render_template("home.html", profile=profile)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    profile = load_profile()

    if request.method == "POST":
        profile["name"] = request.form["name"]
        profile["bio"] = request.form["bio"]
        profile["vision"] = request.form["vision"]
        profile["skills"] = request.form["skills"]
        profile["experience"] = request.form["experience"]

        image = request.files.get("profile_image")
        if image and image.filename:
            image.save(os.path.join(IMAGE_FOLDER, "profile.jpg"))

        resume = request.files.get("resume")
        if resume and resume.filename:
            resume.save(os.path.join(FILE_FOLDER, "Siva_Kumar_Resume.pdf"))

        save_profile(profile)
        return redirect("/")

    return render_template("admin.html", profile=profile)

@app.route("/resume")
def resume():
    return send_from_directory(FILE_FOLDER, "Siva_Kumar_Resume.pdf", as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
