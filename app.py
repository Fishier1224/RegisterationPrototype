from flask import Flask, session, request, render_template, redirect, url_for
import chromadb_setup as db
import logging

app = Flask(__name__)

app.secret_key = "AthenaMo"

logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect user details from the form and store in session
        session['user_details'] = {
            "phone": request.form["phone"],
            "user_id": request.form["user_id"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "occupation": request.form["occupation"]
        }
        return redirect(url_for("interests"))
    return render_template("index.html")


@app.route("/interests", methods=["GET", "POST"])
def interests():
    if request.method == "POST":
        interests = request.form.getlist("interests")
        user_details = session.get('user_details', {})
        
        # Debugging: Log the session details
        logging.debug(f"Session user details: {user_details}")
        
        # Add the user to the database, including their selected interests
        db.add_user(user_details.get('phone'), user_details.get('user_id'), user_details.get('age'),
                    user_details.get('gender'), user_details.get('occupation'), interests)
        
        return "Registration Complete!"
    
    return render_template("interests.html")




@app.route("/user/<user_id>")
def view_user(user_id):
    user = db.get_user(user_id)
    if user:
        return f"""
        <h1>User Details</h1>
        <p><strong>User ID:</strong> {user_id}</p>
        <p><strong>Phone:</strong> {user['phone']}</p>
        <p><strong>Age:</strong> {user['age']}</p>
        <p><strong>Gender:</strong> {user['gender']}</p>
        <p><strong>Occupation:</strong> {user['occupation']}</p>
        <p><strong>Interests:</strong> {', '.join(user['interests'])}</p>
        """
    else:
        return f"<p>No user found with user_id: {user_id}</p>"



if __name__ == "__main__":
    app.run(debug=True)
