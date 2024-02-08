from wtforms import Form, BooleanField, StringField, PasswordField, validators,EmailField, IntegerField

class RegistrationForm(Form):
    first_name = StringField('first_name', [validators.Length(min=3, max=25)])
    last_name = StringField('last_name', [validators.Length(min=3, max=35)])
    email = EmailField("email",[validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField("email",[validators.Length(min=6, max=35)])

class get_cart_form(Form):
    max_date = IntegerField("max_date", [validators.NumberRange(min=1,max=100,message="salah anjing, harus angka cok")])
    min_date = IntegerField("min_date", [validators.NumberRange(min=1,max=100,message="salah anjing, harus angka cok")])

class add_cart_form(Form):
    product_id = IntegerField("product_id", [validators.Length(min=1,max=200,message="product_id must be number")]) 
    quantity = IntegerField("quantity", [validators.Length(min=1,max=200,message="quality must be number")]) 