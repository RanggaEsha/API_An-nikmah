from flask import Flask
from controllers import login_controller,register_controller,add_product_controller,protected_controller



from flask_jwt_extended import (
    JWTManager,
    jwt_required,
)
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "bacotttttttt"
jwt = JWTManager(app)

@app.get('/protected')
@jwt_required()
def get_all_products():
    return protected_controller()

@app.post('/login')
def login_process():
    return login_controller()

@app.post('/register')
def register():
    return register_controller()
   
@app.post('/products')
def upload():
    return add_product_controller()

if __name__==('__main__'):
   app.run(debug=True,port=5001,use_reloader=True,host="0.0.0.0")