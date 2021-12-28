from flask import Flask, redirect, url_for, request, render_template, session, flash
import time, datetime, requests, mysql.connector
from datetime import timedelta
from mydb import dbHandle as myhandle
#creating an instance of the app
app = Flask(__name__)
app.secret_key = "hell"
# user will be logged for the give no of days hours or min
app.permanent_session_lifetime = timedelta(minutes=5)


#the home page of the app
@app.route("/")
def home():
    return render_template("index.html", user = (True if session.get('user') else False))

#the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user'):
        return redirect(url_for("user"))
        return render_template("user.html")
    else:    
        if request.method == "POST":
            myhandle.create_table()
            user = request.form["nm"]
            pas = request.form["password"]
            if (myhandle.select_info(user, pas)):
               session.permanent = True
               session["user"] = user
               return redirect(url_for("user"))
               return render_template("user.html")
            else:
               return render_template("login.html")
        else:
            return render_template("login.html", user = (True if session.get('user') else False))



#registering the user
@app.route("/register", methods=["GET", "POST"])
def register():
   if session.get('user'):
        return redirect(url_for("user"))
        return render_template("user.html")
   else:    
      if request.method == "POST":
         user = request.form["nm"]
         pas = request.form["password"]
         print(user + pas)
         myhandle.insert_user(user, pas)
         if (myhandle.select_info(user, pas)):
            session.permanent = True
            session["user"] = user
            return redirect(url_for("user"))
            return render_template("user.html")
         else:
            return render_template("register.html")
      else:
         return render_template("register.html", user = (True if session.get('user') else False))

@app.route("/user")
def user():
   if session.get('user'):
      us = True
      return render_template("user.html", user = (True if session.get('user') else False))
   else:
      return redirect(url_for("login"))
      return render_template("login.html")

@app.route("/dashboard")
def dboard():
   if session.get('user'):
      return render_template("dashboard.html", user = (True if session.get('user') else False))
   else:
      return redirect(url_for("login"))
      return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))




def get_price():
    url='https://ftx.com/api/markets/BTC/USD'
    interval=2
    try:
        response=requests.get(url)
        if response.status_code==200:
            data=response.json()
            price=data['result']['last']
    except KeyError:
        time.sleep(interval)
    except:
        time.sleep(interval)
    return price


@app.route("/stock")
def stock():
    price = get_price()
    print(price)
    #flash(price)
    return render_template("stock.html", price = price)

#running the app
if __name__ == "__main__":
    app.run(debug=True)