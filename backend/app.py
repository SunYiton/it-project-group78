from flask import Flask, jsonify, request
from flask_cors import CORS
import os, datetime, jwt, json

app = Flask(__name__)
CORS(app)

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
JWT_HOURS = int(os.environ.get("JWT_HOURS", "8"))

# health check
@app.get("/health")
def health():
    return jsonify(status="ok"), 200

# login (mock)
@app.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    users = {
        "coord@example.com": {"role": "coordinator", "password": "pass"},
        "marker@example.com": {"role": "marker", "password": "pass"},
    }

    u = users.get(email)
    if not u or u["password"] != password:
        return jsonify(error={"code": 401, "message": "Invalid credentials"}), 401

    payload = {
        "sub": email,
        "role": u["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_HOURS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return jsonify(token=token, role=u["role"])

# assignments (mock + pagination)
@app.get("/assignments")
def get_assignments():
    status = request.args.get("status")  # current | history
    page = int(request.args.get("page", "1"))
    page_size = int(request.args.get("pageSize", "20"))

    with open(os.path.join(os.path.dirname(__file__), "mock/assignments.json"), "r") as f:
        all_assignments = json.load(f)

    if status:
        all_assignments = [a for a in all_assignments if a.get("status") == status]

    total = len(all_assignments)
    start = (page - 1) * page_size
    end = start + page_size
    items = all_assignments[start:end]

    return jsonify({
        "items": items,
        "page": page,
        "pageSize": page_size,
        "total": total
    }), 200


# start server when running "python app.py"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)