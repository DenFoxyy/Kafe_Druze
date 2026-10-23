import re

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bestilling", methods=["GET", "POST"])
def bestilling():
    if request.method == "POST":
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()
        phone_pattern = r"[0-9+() .-]*[0-9][0-9+() .-]*"
        email_pattern = r"[^@\s]+@[^@\s]+\.[^@\s]+"

        if not re.fullmatch(phone_pattern, phone) or not re.fullmatch(email_pattern, email):
            return render_template(
                "bestilling.html",
                validation_error="Enter a valid phone number and email address.",
            ), 400

        booking = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "phone": phone,
            "email": email,
            "guests": request.form["guests"],
            "date": request.form["date"],
            "time": request.form["time"],
            "comment": request.form.get("comment", ""),
        }

        return render_template(
            "bekreftelse.html",
            booking=booking,
        )

    return render_template("bestilling.html")


if __name__ == "__main__":
    app.run(debug=True)