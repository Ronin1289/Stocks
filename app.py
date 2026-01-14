
import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from prometheus_2_1 import (
    scan_divergences,
    NIFTY100,
    LARGE_CAP_STOCKS,
    MID_CAP_STOCKS,
    SMALL_CAP_STOCKS,
)
import config

app = Flask(__name__)

# Secret key: prefer config, then environment, fallback to insecure default
app.secret_key = config.FLASK_SECRET_KEY or os.environ.get("FLASK_SECRET_KEY", "change-me")

# Credentials: prefer config.py values, then environment variables
CONFIG_USERNAME = getattr(config, "USERNAME", None) or os.environ.get("PROMETHEUS_USERNAME")
CONFIG_PASSWORD = getattr(config, "PASSWORD", None) or os.environ.get("PROMETHEUS_PASSWORD")

STOCK_GROUPS = {
    "nifty100": NIFTY100,
    "large": LARGE_CAP_STOCKS,
    "mid": MID_CAP_STOCKS,
    "small": SMALL_CAP_STOCKS,
}


def login_required_page(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
@login_required_page
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not CONFIG_PASSWORD:
            flash("Server has no password configured.", "danger")
            return render_template("login.html")

        # If a username is configured, require both username+password to match.
        if CONFIG_USERNAME:
            if username == CONFIG_USERNAME and password == CONFIG_PASSWORD:
                session["authenticated"] = True
                session["username"] = username
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Invalid username or password", "danger")
                return render_template("login.html")
        else:
            # password-only mode
            if password == CONFIG_PASSWORD:
                session["authenticated"] = True
                session.pop("username", None)
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Invalid password", "danger")
                return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))


@app.route("/api/scan", methods=["POST"])
def api_scan():
    if not session.get("authenticated"):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json() or {}
    group = data.get("group", "large")
    period = data.get("period", "1y")
    interval = data.get("interval", "1d")
    order = int(data.get("order", 5))

    stocks = STOCK_GROUPS.get(group, LARGE_CAP_STOCKS)

    try:
        df = scan_divergences(stocks, period=period, interval=interval, order=order)
        records = df.to_dict(orient="records")
        counts = df["Signal"].value_counts().to_dict()
        return jsonify({"results": records, "counts": counts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
