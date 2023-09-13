from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, FileField
from wtforms.validators import InputRequired, EqualTo

class LoginForm(FlaskForm):
    user_id = StringField("User id: ", validators=[InputRequired()])
    password = PasswordField("Password : ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    user_id = StringField("User id: ", validators=[InputRequired()])
    date_birth = DateField("Date of Birth: ", validators=[InputRequired()])
    password = PasswordField("Password : ", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:",
        validators= [InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class AdminForm(FlaskForm):
    admin_id = StringField("admin id: ", validators=[InputRequired()])
    admin_password = PasswordField("Password : ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ShopForm(FlaskForm):
    name = StringField("Add Item:", validators=[InputRequired()])
    price = IntegerField("Add Price:", validators=[InputRequired()])
    description = StringField("Add Description of Item:", validators=[InputRequired()])
    image_name = FileField("Add an image: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class DetailsForm(FlaskForm):
    address = StringField("Address:", validators=[InputRequired()])
    card_name = StringField("Card holders name:", validators=[InputRequired()])
    number = IntegerField("Your card number:", validators=[InputRequired()])
    expiry = DateField("Expiry date", validators=[InputRequired()])
    cvc = IntegerField("CVC", validators=[InputRequired()])
    submit = SubmitField("Submit")