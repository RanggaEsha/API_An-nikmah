from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
    EmailField,
    IntegerField,
    DateField,
)
from datetime import datetime


# AUTH
class LoginForm(Form):
    """
    Form for user login.

    Fields:
        email (EmailField): User's email.
        password (PasswordField): User's password.

    Validation:
        - Email validation.
        - Password length between 6 and 35 characters.
    """

    email = EmailField("email", [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField(
        "password",
        [
            validators.Length(
                min=6, max=35, message="Password must be atleast 6 characters"
            )
        ],
    )


class RegistrationForm(Form):
    """
    Form for user registration.

    Fields:
        first_name (StringField): User's first name.
        email (EmailField): User's email.
        password (PasswordField): User's password.
        confirm_password (PasswordField): Confirmation of user's password.

    Validation:
        - First name length between 3 and 25 characters.
        - Email validation.
        - Password length at least 6 characters.
        - Confirm password must match the password.
    """

    first_name = StringField("first_name", [validators.Length(min=3, max=25)])
    email = EmailField("email", [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField(
        "password",
        [
            validators.Length(
                min=6, max=35, message="Password is too short, atleast 6 characters"
            )
        ],
    )
    confirm_password = PasswordField(
        validators=[validators.EqualTo("password", "Confirm password is mismatch")]
    )


# CART
class get_cart_form(Form):
    """
    Form for retrieving user carts.

    Fields:
        max_date (DateField, optional): Maximum date for filtering carts.
        min_date (DateField, optional): Minimum date for filtering carts.

    Validation:
        - Date format validation (YYYY-MM-DD).
    """

    max_date = DateField(validators=[validators.Optional()])
    min_date = DateField(validators=[validators.Optional()])


def validate_date_format(date_str):
    """
    Validate date format as YYYY-MM-DD.

    Args:
        date_str (str): Date string to validate.

    Returns:
        datetime object: Validated date if the format is correct.
        bool: False if the format is incorrect.

    Raises:
        ValueError: If the date format is incorrect.
    """
    try:
        # Check if date format is YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False


class add_cart_form(Form):
    """
    Form for adding a new cart.

    Fields:
        product_id (IntegerField): ID of the product to add to the cart.
        quantity (IntegerField): Quantity of the product to add to the cart.

    Validation:
        - Numeric validation for product_id and quantity.
    """

    product_id = IntegerField(
        "product_id",
        [validators.NumberRange(min=1, max=200, message="product_id must be number")],
    )
    quantity = IntegerField(
        "quantity",
        [validators.NumberRange(min=1, max=200, message="quality must be number")],
    )


# CATHEGORY
class add_category_form(Form):
    """
    Form for adding a new category.

    Fields:
        name (StringField): Name of the category.

    Validation:
        - Name length between 3 and 25 characters.
    """

    name = StringField("name", [validators.Length(min=3, max=25)])


# PRODUCT
class add_product_form(Form):
    """
    Form for adding a new product.

    Fields:
        name (StringField): Name of the product.
        description (StringField): Description of the product.
        price (IntegerField): Price of the product.
        quantity (IntegerField): Quantity of the product.
        category_id (IntegerField): ID of the category to which the product belongs.

    Validation:
        - Numeric validation for price, quantity, and category_id.
    """

    name = StringField("name", [validators.Length(min=3, max=35)])
    description = StringField("description", [validators.Length(min=3, max=200)])
    price = IntegerField(
        "price",
        [validators.NumberRange(min=1, max=1000000, message="price must be number")],
    )
    quantity = IntegerField(
        "quantity",
        [validators.NumberRange(min=1, max=200, message="quantity must be number")],
    )
    category_id = IntegerField(
        "category_id",
        [validators.NumberRange(min=1, max=200, message="category_id must be number")],
    )


# TRANSACTION
class get_transaction_form(Form):
    """
    Form for retrieving user transactions.

    Fields:
        max_date (DateField, optional): Maximum date for filtering transactions.
        min_date (DateField, optional): Minimum date for filtering transactions.

    Validation:
        - Date format validation (YYYY-MM-DD).
    """

    max_date = DateField(validators=[validators.Optional()])
    min_date = DateField(validators=[validators.Optional()])


class add_transaction_form(Form):
    """
    Form for adding a new transaction.

    Fields:
        address (StringField): Address for the transaction.
        fullname (StringField): Full name for the transaction.
        phone_number (StringField): Phone number for the transaction.
        product_id (IntegerField): ID of the product for the transaction.
        quantity (IntegerField): Quantity of the product for the transaction.

    Validation:
        - Numeric validation for product_id and quantity.
        - Phone number validation (minimum length of 10 characters).
    """

    address = StringField("address", [validators.Length(min=3, max=35)])
    fullname = StringField("fullname", [validators.Length(min=3, max=200)])
    phone_number = StringField(
        "phone_number", [validators.Length(min=10, message="phone number is invalid")]
    )
    product_id = IntegerField(
        "product_id",
        [validators.NumberRange(min=1, max=200, message="product is must be number")],
    )
    quantity = IntegerField(
        "quantity",
        [validators.NumberRange(min=1, max=200, message="category_id must be number")],
    )


class add_transaction_from_cart_form(Form):
    """
    Form for adding a new transaction from cart.

    Fields:
        address (StringField): Address for the transaction.
        fullname (StringField): Full name for the transaction.
        phone_number (StringField): Phone number for the transaction.
        carts_ids (IntegerField): IDs of the carts for the transaction.

    Validation:
        - Numeric validation for carts_ids.
        - Phone number validation (minimum length of 10 characters).
    """

    address = StringField("address", [validators.Length(min=3, max=35)])
    fullname = StringField("fullname", [validators.Length(min=3, max=200)])
    phone_number = StringField(
        "phone_number", [validators.Length(min=10, message="phone number is invalid")]
    )
    carts_ids = IntegerField(
        "cart_ids",
        [validators.NumberRange(min=1, max=200, message="product is must be number")],
    )
