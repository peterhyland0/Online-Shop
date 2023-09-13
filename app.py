from sys import dont_write_bytecode
from flask import Flask, render_template, redirect, request, url_for, session, g
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, ShopForm, AdminForm, DetailsForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False # These 3 lines configure the way that our sessions work
app.config["SESSION_TYPE"] = "filesystem" # Session state is stored in files
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

@app.before_request
def load_logged_in_user():
    g.admin = session.get("admin_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        date_birth = form.date_birth.data
        password = form.password.data
        password2 = form.password2.data 
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
                                                WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, date_birth, password) VALUES (?, ?, ?);""",(user_id, date_birth, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data 
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users
                                                WHERE user_id = ?;""", (user_id,)).fetchone()
        if matching_user is None:
            form.user_id.errors.append("Unknown user id!")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for("shop_index",next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/shop_admin", methods=["GET","POST"])
def shop_admin():
    form = AdminForm()
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        admin_password = form.admin_password.data 
        db = get_db()
        matching_admin = db.execute("""SELECT * FROM admin
                                        WHERE admin_id = ?;""", (admin_id,)).fetchone()
        if matching_admin is None:
            form.admin_id.errors.append("Unknown user id!")
        elif not check_password_hash(matching_admin["admin_password"], admin_password):
            form.admin_password.errors.append("Incorrect admin password")
        else:
            session.clear()
            session["admin_id"] = admin_id
            
            return render_template("shop_index.html")
    return render_template("shop_login.html", form=form)

@app.route("/details", methods=["GET","POST"])
@login_required
def details():
    form = DetailsForm()
    details = None
    
    if form.validate_on_submit():
        address = form.address.data
        card_name  = form.card_name.data
        number = form.number.data
        expiry = form.expiry.data
        cvc = form.cvc.data
        db = get_db()
        if address is None:
            form.address.errors.append("Please enter a valid address")
        else:
            db.execute("""INSERT INTO details (address, card_name, number, expiry, cvc) VALUES (?, ?, ?, ?, ?);""",(address, card_name, number, expiry, cvc))
            db.commit()
            return redirect( url_for("checkout"))
    return render_template("checkout_details.html", form=form)

@app.route("/shop_items", methods=["GET","POST"])
@admin_required
def shop_items():
    form = ShopForm()
    admin = None
    
    if form.validate_on_submit():
        
        name  = form.name.data
        price = form.price.data
        description = form.description.data
        image_name = form.image_name.data
        db = get_db()
        # db.execute("""SELECT * FROM kit_all
        #                 WHERE  name = ? AND price = ?
        #                 AND description = ?""", (name, price, description)).fetchall()
        db.execute("""INSERT INTO kit_all (name, price, description, image_name) VALUES (?, ?, ?, ?);""",(name, price, description, image_name))
        db.commit()
        
    return render_template("shop_items.html", form=form)
        

@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )

@app.route("/users")
@admin_required
def users():
    db = get_db()
    users = db.execute("""SELECT * FROM users;""").fetchall() #gets a list
    return render_template("users.html", users=users)

@app.route("/user/<int:user_id>")
def user(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM users
                        WHERE user_id = ? AND password = ?;""", (user_id,)).fetchone() #gets one  
    return render_template("user.html", user=user)

@app.route("/kit_all")
def kit_all():
    db = get_db()
    kit_all = db.execute("""SELECT * FROM kit_all;""").fetchall() #gets a list
    return render_template("kit_all.html", kit_all=kit_all)

@app.route("/kit/<int:kit_id>")
def kit(kit_id):
    db = get_db()
    kit = db.execute("""SELECT * FROM kit_all
                        WHERE kit_id = ?;""", (kit_id,)).fetchone() #gets one  
    return render_template("kit.html", kit=kit)

@app.route("/cart")
@login_required
def cart():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    db = get_db()
    for kit_id in session["cart"]:
        if kit_id == None:
            return redirect( url_for("kit_all"))
        kit = db.execute("""SELECT * FROM kit_all
                            WHERE kit_id = ?;""", (kit_id,)).fetchone()
        name = kit["name"]
        names[kit_id] = name
        g.kit = None
    return render_template("cart.html", cart=session["cart"], names=names, kit=kit) 

@app.route("/checkout")
@login_required
def checkout():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    db = get_db()
    for kit_id in session["cart"]:
        kit = db.execute("""SELECT * FROM kit_all
                            WHERE kit_id = ?;""", (kit_id,)).fetchone()
        name = kit["name"]
        names[kit_id] = name
        
    return render_template("checkout.html", cart=session["cart"], names=names, kit=kit) 

@app.route("/add_to_cart/<int:kit_id>")
@login_required
def add_to_cart(kit_id):
    # Add one bottle of kit_id to cart
    if "cart" not in session:
        session["cart"] = {}
    if kit_id not in session["cart"]:
        session["cart"][kit_id] = 0
    session["cart"][kit_id] = session["cart"][kit_id] + 1
    return redirect( url_for("cart") )

# @app.route("/checkout")
# @login_required
# def checkout(kit_id):
#     # Add one bottle of kit_id to cart
#     if "cart" not in session:
#         session["cart"] = {}
#     if kit_id not in session["cart"]:
#         session["cart"][kit_id] = 0
#     session["cart"][kit_id] = session["cart"][kit_id] + 1
#     return redirect( render_template("checkout.html") )

@app.route("/delete_from_cart/<int:kit_id>")
@login_required
def delete_from_cart(kit_id):
    # Add one bottle of kit_id to cart
    if "cart" in session:
      if kit_id in session["cart"]:
        del session["cart"][kit_id] 
    if "cart" in session == {}:
        return redirect( url_for("kit_all") )

    # session["cart"][kit_id] = session["cart"][kit_id] 
    return redirect( url_for("cart") )

@app.route("/delete_cart/<int:kit_id>")
@login_required
def delete_cart(kit_id):
    # Add one bottle of kit_id to cart
    if "cart" in session:
        session["cart"] = {}
    # if kit_id not in session["cart"]:
    #     session["cart"][kit_id] = 0
    # session["cart"][kit_id] = session["cart"][kit_id] + 1
    return redirect( url_for("cart") )