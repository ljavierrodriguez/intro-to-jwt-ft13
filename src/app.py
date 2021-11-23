from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Intent
import datetime

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["JWT_SECRET_KEY"] = "455a0595071af6e2385c0ec556cb329c"  # Change this!
db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

banned = []
logins = []

@app.route('/')
def main():
    return render_template('index.html');


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username: return jsonify({ "msg": "Username is required!"}), 422
    if not password: return jsonify({ "msg": "Password is required!"}), 422

    user = User.query.filter_by(username=username).first()

    if not user: return jsonify({ "msg": "Username/password are incorrect!"}), 401
    if not check_password_hash(user.password, password): return jsonify({ "msg": "Username/password are incorrect!"}), 401

    expire = datetime.timedelta(minutes=5)

    access_token = create_access_token(identity=user.username, expires_delta=expire)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 200


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username: return jsonify({ "msg": "Username is required!"}), 422
    if not password: return jsonify({ "msg": "Password is required!"}), 422

    user = User.query.filter_by(username=username).first()
    if user: return jsonify({ "msg": "Username already exists!"}), 422

    user = User()
    user.username = username
    user.password = generate_password_hash(password)

    user.save()

    if user: 
        expire = datetime.timedelta(minutes=5)
        access_token = create_access_token(identity=user.username, expires_delta=expire)
        data = {
            "success": "Register succesfully!",
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 201
        #return jsonify({ "success": "Register succesfully!", "user": user.serialize()}), 201
    return jsonify({ "fail": "Register fail! Please try again"}), 422



@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    
    return jsonify(user.serialize()), 200




if __name__ == '__main__':
    app.run()