
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Optional
from flask_wtf.file import FileRequired, FileField, FileAllowed, FileRequired

# specify allowed image file formats
IMAGE_FORMAT = {"png", "jpg", "webp"}

# creates the login information
class LoginForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired('Enter username')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    username =StringField("Username", validators=[InputRequired()])
    phone =IntegerField("Phone Number (Optional)", validators=[Optional(), NumberRange(min=0, max=9999999999,
    message="Please enter a valid phone number e.g. 0412345678")])
    address =StringField("Address (Optional)", validators=[Optional()])
    # linking two fields - password should be equal to data entered in confirm
    password =PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords do not match")])
    
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# creates an event
class EventForm(FlaskForm):
    name = StringField("Name", validators = [InputRequired()])
    description = TextAreaField("Description", validators = [InputRequired()])
    image = FileField("Image", validators=[
        FileRequired(message="Must provide an image"),
        FileAllowed(IMAGE_FORMAT, message="Supported formats: PNG, JPG and WEBP")
    ])
    date = DateField("Date")
    time = TimeField("Time")
    category = SelectField(label='Category', choices=[("Classical", "Classical"), ("Rock", "Rock"),
        ("EDM", "EDM"), ("Hip Hop", "Hip Hop"), ("Pop", "Pop"), ("Jazz", "Jazz"),
        ("Blues", "Blues")])
    artist = StringField("Artist", validators = [InputRequired()])
    venue = StringField("Venue", validators = [InputRequired()])
    ticket_max = IntegerField("Tickets Available", validators = [InputRequired(), NumberRange(min=1)])
    status = SelectField(label='Status', choices=[("Open", "Open"), ("Unpublished", "Unpublished"),
        ("Sold Out", "Sold Out"), ("Cancelled", "Cancelled")])
    submit = SubmitField("Create now")

# category selection
class CategoryFilterForm(FlaskForm):
    category = SelectField(label='Category', choices=[("All","All"),("Classical", "Classical"), ("Rock", "Rock"),
        ("EDM", "EDM"), ("Hip Hop", "Hip Hop"), ("Pop", "Pop"), ("Jazz", "Jazz"),
        ("Blues", "Blues")])

    submit = SubmitField("Search Category")

# creates an event
class EditEventForm(FlaskForm):
    name = StringField("Name", validators = [InputRequired()])
    description = TextAreaField("Description", validators = [InputRequired()])
    date = DateField("Date")
    time = TimeField("Time")
    category = SelectField(label='Category', choices=[("Classical", "Classical"), ("Rock", "Rock"),
        ("EDM", "EDM"), ("Hip Hop", "Hip Hop"), ("Pop", "Pop"), ("Jazz", "Jazz"),
        ("Blues", "Blues")])
    artist = StringField("Artist", validators = [InputRequired()])
    venue = StringField("Venue", validators = [InputRequired()])
    ticket_max = IntegerField("Tickets Available", validators = [InputRequired(), NumberRange(min=1)])
    status = SelectField(label='Status', choices=[("Open", "Open"), ("Unpublished", "Unpublished"),
        ("Sold Out", "Sold Out"), ("Cancelled", "Cancelled")])

    submit = SubmitField("Save Changes")

# creates a comment for an event
class CommentForm(FlaskForm):
    comment = TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField("Submit")

# form for creating a booking
class BookingForm(FlaskForm):
    ticket_qty = IntegerField("Ticket Quantity", validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField("Submit")
