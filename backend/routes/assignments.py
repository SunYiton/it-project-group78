# routes/assignments.py
from flask import Blueprint, request, jsonify
from repositories.assignments_repo import list_assignments

bp = Blueprint("assignments", __name__)

@bp.get("/assignments")
def get_assignments():
    status = request.args.get("status")  # current | history | None
    page = int(request.args.get("page", "1"))
    page_size = int(request.args.get("pageSize", "20"))

    items, total = list_assignments(status=status, page=page, page_size=page_size)

    return jsonify({
        "items": items,
        "page": page,
        "pageSize": page_size,
        "total": total
    }), 200