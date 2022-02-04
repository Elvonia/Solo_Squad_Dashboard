import os

from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

#-------------> Remove before release <--------------#
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
#----------------------------------------------------#

app.config["DISCORD_CLIENT_ID"] = os.environ.get("DISCORD_CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get("DISCORD_CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback"

app.secret_key = app.config["DISCORD_CLIENT_SECRET"]

discord = DiscordOAuth2Session(app)

# Any reason to call @requires_authorization when discord.fetch_user() triggers login if no user data is present?
@app.route("/")
def index():
    return render_template("index.html", user=discord.fetch_user())


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("index"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)