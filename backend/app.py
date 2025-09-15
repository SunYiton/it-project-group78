# app.py
from flask import Flask, jsonify, request, g
from flask_cors import CORS
import os, datetime, jwt

# config
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
JWT_HOURS = int(os.environ.get("JWT_HOURS", "8"))

def create_app():
    app = Flask(__name__)
    CORS(app)

    # helpers
    def json_error(code: int, message: str):
        resp = jsonify(error={"code": code, "message": message})
        resp.status_code = code
        return resp

    # auth decorators (JWT)
    def require_auth(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            prefix = "Bearer "
            if not auth.startswith(prefix):
                return json_error(401, "Missing or invalid Authorization header")
            token = auth[len(prefix):].strip()
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return json_error(401, "Token expired")
            except jwt.InvalidTokenError:
                return json_error(401, "Invalid token")

            g.user = {
                "email": payload.get("sub"),
                "role": payload.get("role"),
            }
            return fn(*args, **kwargs)
        return wrapper

    def require_role(role: str):
        def decorator(fn):
            from functools import wraps
            @wraps(fn)
            def wrapper(*args, **kwargs):
                auth = request.headers.get("Authorization", "")
                if not auth.startswith("Bearer "):
                    return json_error(401, "Missing or invalid Authorization header")
                token = auth[len("Bearer "):].strip()
                try:
                    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                except jwt.ExpiredSignatureError:
                    return json_error(401, "Token expired")
                except jwt.InvalidTokenError:
                    return json_error(401, "Invalid token")

                user_role = payload.get("role")
                if user_role != role:
                    return json_error(403, f"Forbidden: requires role '{role}'")
                g.user = {"email": payload.get("sub"), "role": user_role}
                return fn(*args, **kwargs)
            return wrapper
        return decorator

    # health
    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    # login (mock)
    @app.post("/login")
    def login():
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        # mock users
        users = {
            "coord@example.com": {"role": "coordinator", "password": "pass"},
            "marker@example.com": {"role": "marker", "password": "pass"},
        }

        u = users.get(email)
        if not u or u["password"] != password:
            return json_error(401, "Invalid credentials")

        payload = {
            "sub": email,
            "role": u["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_HOURS),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return jsonify(token=token, role=u["role"])

    # protected demo route
    @app.get("/secure/ping")
    @require_auth
    def secure_ping():
        # g.user set by require_auth
        return jsonify(message="pong", user=g.get("user")), 200

    # Example of role-protected route (only coordinator)
    @app.get("/secure/admin-only")
    @require_role("coordinator")
    def admin_only():
        return jsonify(message="hello, coordinator"), 200

    # register blueprints
    from routes.assignments import bp as assignments_bp
    app.register_blueprint(assignments_bp)

    # error handlers (json)
    @app.errorhandler(404)
    def not_found(_e):
        return json_error(404, "Not found")

    @app.errorhandler(500)
    def server_error(e):
        # optional: log e
        return json_error(500, "Internal server error")

    return app


if __name__ == "__main__":
    # local dev run
    app = create_app()
    # set host="0.0.0.0" if needed
    app.run(debug=True)