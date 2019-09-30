from app import app, db, flask_bcrypt
from flask import jsonify, request
from app.models import Users
from flask_jwt_extended import create_access_token
from datetime import datetime


@app.route('/users/register', methods=['POST'])
def register():
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = flask_bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user = Users.query.filter_by(email=email).first()
    if not user:
        data_user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            created=created
        )
        db.session.add(data_user)
        db.session.commit()

    user = Users.query.filter_by(email=email).first()
    result = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password,
        'created': user.created
    }

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    result = ''
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = Users.query.filter_by(email=email).first()
    if user:
        if user.check_password(password):
            access_token = create_access_token(
                identity={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"error": "This user doesn't exist."})

    return result
