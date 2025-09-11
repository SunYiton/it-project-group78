from flask import Flask, jsonify, request
from flask_cors import CORS
import os, datetime, jwt, json

app = Flask(__name__)
CORS(app)

# ====== JWT config ======
JWT_SECRET  = os.environ.get("JWT_SECRET", "dev-secret")
JWT_HOURS   = int(os.environ.get("JWT_HOURS", "8"))
ALGORITHM   = "HS256"

# ====== health check ======
@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

# ====== login (mock) ======
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    users = {
        "coord@example.com":  {"role": "coordinator", "password": "pass"},
        "marker@example.com": {"role": "marker",      "password": "pass"},
    }

    u = users.get(email)
    if not u or u["password"] != password:
        return jsonify(error={"code": 401, "message": "Invalid credentials"}), 401

    payload = {
        "sub":  email,
        "role": u["role"],
        "exp":  datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_HOURS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return jsonify(token=token, role=u["role"])

# ====== secure endpoint (JWT required) ======
@app.route("/secure/ping", methods=["GET"])
def secure_ping():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(detail="Missing or invalid Authorization header"), 401

    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify(detail="Token expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(detail="Invalid token"), 401

    return jsonify(
        status="ok",
        user={"sub": payload.get("sub"), "role": payload.get("role")}
    ), 200

# ====== assignments (mock + pagination) ======
@app.route("/assignments", methods=["GET"])
def get_assignments():
    status    = request.args.get("status")
    page      = int(request.args.get("page", "1"))
    page_size = int(request.args.get("pageSize", "20"))

    with open(os.path.join(os.path.dirname(__file__), "mock/assignments.json"), "r") as f:
        all_assignments = json.load(f)

    if status:
        all_assignments = [a for a in all_assignments if a.get("status") == status]

    total = len(all_assignments)
    start = (page - 1) * page_size
    end   = start + page_size
    items = all_assignments[start:end]

    return jsonify({
        "items": items,
        "page": page,
        "pageSize": page_size,
        "total": total
    }), 200

# ====== debug: list all routes ======
@app.route("/__routes", methods=["GET"])
def list_routes():
    return jsonify(sorted([str(r) for r in app.url_map.iter_rules()]))

# ====== entrypoint ======
if __name__ == "__main__":
    print(">>> LOADED app.py from:", __file__)
    print(">>> ROUTES at startup:", sorted([str(r) for r in app.url_map.iter_rules()]))
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
        use_reloader=False
    )
