import re

from flask import Flask, render_template, request, flash, redirect, url_for
from db_config import save_booking, get_all_bookings, init_database

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production' 


try:
    init_database()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")


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

        
        try:
            booking_id = save_booking(booking)
            booking['id'] = booking_id
            flash("Bestilling lagret!", "success")
        except Exception as e:
            print(f"Error saving booking: {e}")
            flash("Det oppstod en feil ved lagring av bestillingen.", "error")
            return render_template("bestilling.html", validation_error="Database error occurred"), 500

        return render_template(
            "bekreftelse.html",
            booking=booking,
        )

    return render_template("bestilling.html")


@app.route("/admin/bookings")
def admin_bookings():
    """Admin page to view all bookings."""
    try:
        bookings = get_all_bookings()
        return render_template("admin_bookings.html", bookings=bookings)
    except Exception as e:
        print(f"Error retrieving bookings: {e}")
        flash("Kunne ikke hente bestillinger.", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)