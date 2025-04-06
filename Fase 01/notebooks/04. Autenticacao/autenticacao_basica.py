from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "user1": "password1",
    "user2": "password2"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    

@app.route("/hello", methods=["GET"])
@auth.login_required
def hello():
    return jsonify({"message": "hello, world!"})


if __name__ == "__main__":
    app.run(debug=True)
