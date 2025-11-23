from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret123"
jwt = JWTManager(app)

# Helper functions
def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# User Registration & Login
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users_data = load_data("users.json")
    users = users_data.get("users", [])

    if any(u["username"] == username for u in users):
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    users.append({"username": username, "password": hashed_pw})
    users_data["users"] = users
    save_data("users.json", users_data)

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users_data = load_data("users.json")
    users = users_data.get("users", [])

    for user in users:
        if user["username"] == username and check_password_hash(user["password"], password):
            token = create_access_token(identity=username)
            return jsonify({"message": "Login successful", "token": token}), 200

    return jsonify({"error": "Invalid username or password"}), 401


# Student CRUD Endpoints (Protected)
@app.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    students_data = load_data("students.json")
    return jsonify(students_data["students"]), 200


@app.route("/students/<id>", methods=["GET"])
@jwt_required()
def get_student(id):
    students_data = load_data("students.json")
    students = students_data.get("students", {})

    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(students[id]), 200


@app.route("/students", methods=["POST"])
@jwt_required()
def add_student():
    username = get_jwt_identity()
    data = request.get_json()

    students_data = load_data("students.json")
    students = students_data.get("students", {})

    new_id = str(len(students) + 1)
    students[new_id] = {
        "name": data.get("name"),
        "major": data.get("major"),
        "gpa": data.get("gpa"),
        "owner": username
    }

    students_data["students"] = students
    save_data("students.json", students_data)
    return jsonify({"message": "Student added successfully", "id": new_id}), 201


@app.route("/students/<id>", methods=["PUT"])
@jwt_required()
def update_student(id):
    username = get_jwt_identity()
    students_data = load_data("students.json")
    students = students_data.get("students", {})

    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    # Allow the owner OR admin
    if students[id]["owner"] != username and username != "admin":
        return jsonify({"error": "You are not authorized to modify this record"}), 403

    data = request.get_json()
    students[id].update(data)
    save_data("students.json", students_data)

    return jsonify({"message": "Student updated successfully"}), 200


@app.route("/students/<id>", methods=["DELETE"])
@jwt_required()
def delete_student(id):
    username = get_jwt_identity()
    students_data = load_data("students.json")
    students = students_data.get("students", {})

    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    # Allow the owner OR admin
    if students[id]["owner"] != username and username != "admin":
        return jsonify({"error": "You are not authorized to delete this record"}), 403

    del students[id]
    save_data("students.json", students_data)

    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
