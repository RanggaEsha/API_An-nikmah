from wtforms import Form, StringField, PasswordField, validators,EmailField, IntegerField, DateField
from datetime import datetime

# AUTH 
class LoginForm(Form):
    email = EmailField("email",[validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField("password",[validators.Length(min=6, max=35,message="Password must be atleast 6 characters")])

class RegistrationForm(Form):
    first_name = StringField('first_name', [validators.Length(min=3, max=25)])
    email = EmailField("email",[validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField("password",[validators.Length(min=6, max=35,message="Password is too short, atleast 6 characters")])
    confirm_password = PasswordField(validators=[validators.EqualTo('password', 'Password mismatch')])


# CART
class get_cart_form(Form):
    max_date = DateField(validators=[validators.Optional()])
    min_date = DateField(validators=[validators.Optional()])

def validate_date_format(date_str):
    try:
        # Check if date format is YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False

class add_cart_form(Form):
    product_id = IntegerField("product_id", [validators.NumberRange(min=1,max=200,message="product_id must be number")]) 
    quantity = IntegerField("quantity", [validators.NumberRange(min=1,max=200,message="quality must be number")]) 

# CATHEGORY
class add_category_form(Form):
    name = StringField('name', [validators.Length(min=3, max=25)])


# PRODUCT
class add_product_form(Form):
    name = StringField('name', [validators.Length(min=3, max=35)])
    description = StringField('description', [validators.Length(min=3, max=200)])
    price = IntegerField("price", [validators.NumberRange(min=1,max=1000000,message="price must be number")]) 
    quantity = IntegerField("quantity", [validators.NumberRange(min=1,max=200,message="quantity must be number")]) 
    category_id = IntegerField("category_id", [validators.NumberRange(min=1,max=200,message="category_id must be number")])

# TRANSACTION
class add_transaction_form(Form):
    address = StringField('address', [validators.Length(min=3, max=35)])
    fullname = StringField('fullname', [validators.Length(min=3, max=200)])
    phone_number = StringField("phone_number", [validators.Length(min=10,message="phone number is invalid")]) 
    product_id = IntegerField("product_id", [validators.NumberRange(min=1,max=200,message="product is must be number")]) 
    quantity = IntegerField("quantity", [validators.NumberRange(min=1,max=200,message="category_id must be number")])

class add_transaction_from_cart_form(Form):
    address = StringField('address', [validators.Length(min=3, max=35)])
    fullname = StringField('fullname', [validators.Length(min=3, max=200)])
    phone_number = StringField("phone_number", [validators.Length(min=10,message="phone number is invalid")]) 
    carts_ids = IntegerField("carts_ids", [validators.NumberRange(min=1,max=200,message="product is must be number")])