

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(data)

# Get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in data if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    new_user["id"] = len(data) + 1
    data.append(new_user)
    return jsonify(new_user), 201

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in data if u["id"] == user_id), None)
    if user:
        user.update(request.json)
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global data
    data = [u for u in data if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)


