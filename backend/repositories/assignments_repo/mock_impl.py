import json
import os
from typing import List, Tuple, Optional

def _mock_path() -> str:
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(root, "mock", "assignments.json")

def list_assignments(status: Optional[str], page: int, page_size: int) -> Tuple[List[dict], int]:
    with open(_mock_path(), "r", encoding="utf-8") as f:
        all_items = json.load(f)

    if status:
        all_items = [a for a in all_items if a.get("status") == status]

    total = len(all_items)
    start = max(page - 1, 0) * page_size
    end = start + page_size
    items = all_items[start:end]
    return items, total