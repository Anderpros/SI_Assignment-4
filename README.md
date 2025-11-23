# Student Record API with JWT Authentication

**System Integration – Assignment 4**
By **Leonard Marveli B. – IS 2022**

This project is an upgraded version of Assignment 3. It introduces **secure authentication, authorization, and persistent data storage** using JSON files. Users can register, login, and perform CRUD operations on student records based on ownership rules enforced by JWT.

The API is built using **Flask**, **JSON-based storage**, **JWT tokens**, and **hashed passwords** to ensure data security and controlled access.

---

# Features Overview

### Authentication & Authorization

* User Registration (`/register`)
* User Login (`/login`)
* Password hashing using Werkzeug
* JWT Authentication for all protected endpoints
* Admin can edit/delete ALL records
* Normal users can edit/delete **only their own records**

### Persistent Data Storage

Data is stored permanently in:

* `users.json` → Registered users (username + hashed password)
* `students.json` → Student records with owner tracking
  Data **remains saved even after restarting** the server.

### Student CRUD Operations (Protected)

After logging in with JWT:

* Add new students
* Get all students
* Update a student
* Delete a student

Ownership rules:

* A user can only modify/delete records they created
* Admin can modify/delete **all** records

---

# API Endpoints (Method /Endpoint → Description)

## Authentication
- **POST** `/register`  
  → Register a new user (username + password). Saved with hashed password.

- **POST** `/login`  
  → Login and receive a JWT token.

## Student Record Endpoints (JWT Required)

- **GET** `/students`  
  → Retrieve all student records.

- **GET** `/students/<id>`  
  → Retrieve a specific student record by ID.

- **POST** `/students`  
  → Add a new student record (logged-in user becomes `owner`).

- **PUT** `/students/<id>`  
  → Update a student record (only the owner OR admin can update).

- **DELETE** `/students/<id>`  
  → Delete a student record (only the owner OR admin can delete).

---

# File Structure

```
project/
│
├── app.py
├── users.json
└── students.json
```

---

# Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Anderpros/SI_Assignment-4.git
cd SI_Assignment-4
```

### 2. Install dependencies

```bash
pip install flask flask-jwt-extended werkzeug
```

### 3. Run the Flask application

```bash
python app.py
```

The server runs at:

```
http://127.0.0.1:5000
```

---

# How to Use the API (Step-By-Step)

This section explains how to register users, log in, and perform CRUD operations with JWT.

> **IMPORTANT:**
> Use **Git Bash**, NOT PowerShell.
> PowerShell breaks curl commands.

---

# 1️. Register a New User

Endpoint: `POST /register`
This saves the user into `users.json` permanently with **hashed password**.

### Example:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"username":"leonard","password":"1234"}' \
http://127.0.0.1:5000/register
```

Response:

```json
{
  "message": "User registered successfully"
}
```

---

# 2️. Login and Get JWT Token

Endpoint: `POST /login`
Returns a **JWT token** you must use for all protected endpoints.

### Example:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"username":"leonard","password":"1234"}' \
http://127.0.0.1:5000/login
```

Response:

```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Copy the `"token"`.

---

# 3️. Using the Token

To access any protected endpoint:

```bash
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

# 4️. Add a Student (Protected)

Owner will automatically become the logged-in user.

### Example:

```bash
curl -X POST \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-H "Content-Type: application/json" \
-d '{"name":"Leonard Student","major":"IS","gpa":3.8}' \
http://127.0.0.1:5000/students
```

Response:

```json
{
  "message": "Student added successfully",
  "id": "3"
}
```

`students.json` becomes:

```json
"3": {
  "name": "Leonard Student",
  "major": "IS",
  "gpa": 3.8,
  "owner": "leonard"
}
```

---

# 5️. Get Students

Get All Students
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
http://127.0.0.1:5000/students
```

Returns all records.
##
Get a Specific Student
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
http://127.0.0.1:5000/students/3
```

Return the record of the student with ID = 3.

---

# 6️. Update a Student (Protected, Ownership Required)

### Normal users:

Can only update records where `"owner"` = their username.

### Admin:

Can update **any** record.

### Example (PUT):

```bash
curl -X PUT \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-H "Content-Type: application/json" \
-d '{"major":"Data Science"}' \
http://127.0.0.1:5000/students/3
```

If user is not the owner:

```json
{
  "error": "You are not authorized to modify this record"
}
```

---

# 7️. Delete a Student (Protected, Ownership Required)

### Example (DELETE):

```bash
curl -X DELETE \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
http://127.0.0.1:5000/students/3
```

If user is not the owner:

```json
{
  "error": "You are not authorized to delete this record"
}
```

---

# Ownership Rules Summary

| User        | Add | Edit                       | Delete                     |
| ----------- | --- | -------------------------- | -------------------------- |
| **admin**   | Yes | ALL students               | ALL students               |
| **leonard** | Yes | Only leonard-owned records | Only leonard-owned records |
| **Justin**  | Yes | Only Justin-owned records  | Only Justin-owned records  |

---

# Persistent Storage: How It Works

### `users.json`

Stores registered users like:

```json
{
  "users": [
    {
      "username": "leonard",
      "password": "hashedpassword123..."
    }
  ]
}
```

### `students.json`

Stores all students with ownership:

```json
{
  "students": {
    "3": {
      "name": "Leonard",
      "major": "Information Systems",
      "gpa": 3.8,
      "owner": "leonard"
    }
  }
}
```

Both files **stay saved even after restarting** the server.

---

# Limitations

* Not a production database (JSON files only).
* JWT tokens do not expire.
* No password reset feature.
