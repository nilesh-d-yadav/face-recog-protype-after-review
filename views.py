# Learning lesson's From Code with Tim

from flask import Blueprint, render_template, jsonify, redirect, url_for

viewt= Blueprint(__name__, "views")

@viewt.route("/a")
def home():
    return "This Is Me, Nilesh Yadav "

@viewt.route("/a")
def home2():
    return "This is Dharmanath Yadav"

@viewt.route("/")
def home3():
    return render_template("index.html", name="nileshhh", age=12, claass= '7A')

@viewt.route("/profile/<id>")
def profile(id):
    return render_template("index.html", name=id)

# Return Json

@viewt.route("/json")
def do_json():
    return jsonify({'name': 'nilesh', 'class': 'ten'})

# redirect to a page
# import redirect, url_for

@viewt.route("/go_to_json")
def go_to_json():
    return redirect(url_for("views.do_json")) # views.function call