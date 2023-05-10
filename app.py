from flask import *
from database import init_db, db_session
from models import *
from sqlalchemy import func

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = 'ui9UhnxKk8'

# TODO: Fill in methods and routes

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        zipcode = int(request.form["zipcode"])
        experience = request.form["experience"]
        language = request.form["language"]
        bio = request.form["bio"]

        if db_session.query(User).where(User.name == name).first() is None:
            user = User(name = name, password = password, age = age, gender = gender, zipcode = zipcode, experience = experience, language = language, bio = bio)
            db_session.add(user)
            db_session.commit()
            session['currentUser'] = user.id
            return redirect(url_for('home'))
        else:
            flash("That name has been taken!")
    else:
        return render_template("signup.html")
    return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = db_session.query(User).where(User.name == name).first()
        if user is None:
            flash("There is no account under that name.")
            return render_template('login.html')
        elif user.password != password:
            flash("Incorrect Password!")
            return render_template('login.html')
        else:
            session['currentUser'] = user.id
            return redirect(url_for('home'))
            
    return render_template("login.html")

@app.route("/home", methods = ["GET"])
def home():
    if "currentUser" in session:
        requests = {}
        upcoming_sessions = []
        user = db_session.query(User).where(User.id == session["currentUser"]).first()
        user_sessions = db_session.query(UserSession).where(UserSession.user_id == session["currentUser"])
        print(user_sessions)
        for u in user_sessions:
            other_user_session = db_session.query(UserSession).where((UserSession.session_id == u.session_id) & (UserSession.user_id != user.id)).first()
            if other_user_session is not None:
                this_session = db_session.query(Session).where(Session.id == other_user_session.session_id).first()
                other_user = db_session.query(User).where(User.id == other_user_session.user_id).first()
                print(other_user.name)
                if (other_user is not None)&(other_user_session.requester_id!=user.id)&(this_session.accepted!="True"):
                    requests.update({this_session:other_user})
            upcoming_sessions = db_session.query(Session).where((Session.id == u.session_id)&(Session.accepted == "True"))
        return render_template("home.html", user = user, requests = requests, upcoming = upcoming_sessions)
    else:
        return redirect(url_for('login'))

@app.route("/find-a-duo", methods = ["GET", "POST"])
def findaduo():
    if "currentUser" in session:
        user = db_session.query(User).where(User.id == session["currentUser"]).first()
        if request.method == "POST":
            min_age = request.form["min-age"]
            max_age = request.form["max-age"]
            gender = request.form["gender"]
            experience = request.form["experience"]
            language = request.form["language"]
            viable_users = db_session.query(User).where((User.age >= min_age)&(User.age <= max_age)&(func.lower(User.gender) == func.lower(gender)) & (func.lower(User.language) == func.lower(language))&(func.lower(User.experience) == func.lower(experience))&(User.id != user.id))
            return render_template("findaduo.html", viable_users = viable_users, currentUser = user)
        else:
            return render_template("findaduo.html", users = [], currentUser = user)
    else:
        return redirect(url_for('login'))

@app.route("/profile/<userid>", methods = ["GET", "POST"])
def profile(userid):
    if "currentUser" in session:
        currentUser = db_session.query(User).where(User.id == session["currentUser"]).first()
        user = db_session.query(User).where(User.id == userid).first()
        if user != None:
            #Form post for creating a new session
            if request.method == "POST":
                month = request.form["month"]
                day = request.form["day"]
                location = request.form["location"]
                time = request.form["time"]
                new_session = Session(time = time, month = month, day = day, location = location, accepted = "False")
                db_session.add(new_session)
                db_session.flush()
                user_session = UserSession(user_id = currentUser.id, session_id = new_session.id, requester_id = currentUser.id)
                db_session.add(user_session)
                other_user_session = UserSession(user_id = user.id, session_id = new_session.id, requester_id = currentUser.id)
                db_session.add(other_user_session)
                db_session.commit()
            return render_template("profile.html", user = user, currentUser = currentUser)
        else:
            return redirect(url_for('home'))
        # else:
        #     return redirect(url_for('home'))
    else: return redirect(url_for('login'))


@app.route("/logout")
def logout():
    if "currentUser" in session:
        session.pop("currentUser")
    return redirect(url_for("login"))

#Commands triggered by the accept and deny buttons for each session request

@app.route("/accept/<sessionid>")
def accept(sessionid):
    sessionToAccept = db_session.query(Session).where(Session.id == sessionid).first()
    if sessionToAccept is not None:
        sessionToAccept.accepted = "True"
        db_session.commit()
    return redirect(url_for('home'))

@app.route("/deny/<sessionid>")
def deny(sessionid):
    sessionToDeny = db_session.query(Session).where(Session.id == sessionid).first()
    if sessionToDeny is not None:
        db_session.delete(sessionToDeny)
        db_session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)