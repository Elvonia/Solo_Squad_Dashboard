import os

from flask import Flask, redirect, url_for, render_template, request
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


@app.route("/")
def index():
    b = request.args.get("auth")
    if b == "true":
        return render_template("index.html", user=discord.fetch_user(), guilds=discord.fetch_guilds())
    else:
        return render_template("index.html", user=None, guilds=None)


@app.route("/login/")
def login():
    return discord.create_session(scope={'identify', 'guilds'})


@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for("index"))


@app.route("/callback/")
def callback():
    code = request.args.get("code")
    if code != None:
        discord.callback()
        return redirect(url_for("index") + "?auth=true")
    else:
        return redirect(url_for("index"))


@app.route("/test/")
def test():
    return render_template("test.html")


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)