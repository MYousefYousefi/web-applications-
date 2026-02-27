from flask import Flask, render_template

app = Flask(__name__)

profile = {
    "name": "Yousef",
    "about": "I am a python developer "
}

skills = [
    "Python",
    "flask",
    "HTML & CSS",
    "Git & GitHub",
    "SQL"
]

projects = [
    {
        "title" : "portfolio website",
        "description" : "A personal portfolio website built with Flask"
    },
    {
    "title" : "Note-taking app",
    "description" : "A simple note-taking app built with Flask"
    }
]

@app.route('/')
def home():
    return render_template("base.html", profile=profile)

@app.route("/skills")
def show_skills():
    return render_template("skill.html", skills=skills)

@app.route("/projects")
def show_projects():
    return render_template("project.html", projects=projects)

if __name__ == '__main__':
    app.run(debug=True)