import os

DATA_BACKEND = os.environ.get("DATA_BACKEND", "mock").lower()

if DATA_BACKEND == "mock":
    from .mock_impl import list_assignments
else:
    # future：sqlite/db 实现
    from .mock_impl import list_assignments  # Return back to mock