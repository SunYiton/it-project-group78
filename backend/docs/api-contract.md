# API Contract

## Login

**Auth token object**
{
  "token": "<JWT>",
  "role": "coordinator"
} 

### POST /login
Creates a session and returns a JWT.

URL Params: None
Headers: Content-Type: application/json

Request Body
{
  "email": "coord@example.com",
  "password": "pass"
}

Success Response:
Code: 200
Content:
{
  "token": "<JWT>",
  "role": "coordinator"
}

Error Response:
Code: 401
Content: 
{ "error": { "code": 401, "message": "Invalid credentials" } }

## Assignments

Assignment object(schema)
{
  "id": "A-1001",
  "title": "Essay 1",
  "dueDate": "2025-09-01T00:00:00Z",
  "status": "current",
  "discrepancyCount": 2
}


### GET /assignments
Returns a paginated list of assignments.

Query
status (optional): current | history
page (int, default 1)
pageSize (int, default 20)

Headers
Content-Type: application/json
Authorization: Bearer <JWT>

Success Response:
Code: 200
Content:
{
  "items": [ { "id": "A-1001", "title": "Essay 1", "dueDate": "2025-09-01T00:00:00Z", "status": "current", "discrepancyCount": 2 } ],
  "page": 1,
  "pageSize": 20,
  "total": 42
}

Error Response:
Code: 401
Content: 
{ "error": { "code": 401, "message": "Unauthorized" } }

## Moderations (Week 8 – initial)

Moderation object
{
  "id": "M-1001",
  "assignmentId": "A-1001",
  "studentId": "S-1",
  "markerId": "MK-1",
  "rubric": [
    { "criterion": "Clarity", "markerScore": 7, "coordinatorScore": 8, "delta": 1 }
  ],
  "overall": { "markerTotal": 70, "coordinatorTotal": 75, "delta": 5 },
  "status": "open",
  "createdAt": "2025-09-01T10:00:00Z",
  "updatedAt": "2025-09-02T09:00:00Z"
}

### GET /moderations/:id
Returns the specified moderation detail.

URL Params
id(string)

Headers
Content-Type: application/json
Authorization: Bearer <JWT>

Success Response:
Code: 200
Content: 
{ "...": "moderation_object" }

Error Response:
Code: 404
Content: 
{ "error": { "code": 404, "message": "Moderation not found" } }
{ "error": { "code": 401, "message": "Unauthorized" } }

### POST /moderations/:id/resolve
Resolve a moderation with coordinator’s decision.(role:coordinator)

URL Params: id(string)

Headers
Content-Type: application/json
Authorization: Bearer <JWT>

Success Response:
Code: 200
Content: 
{
  "coordinatorNotes": "Adjust based on rubric discussion.",
  "adjustedScores": [
    { "criterion": "Clarity", "coordinatorScore": 8 }
  ]
}

Code: 201
Content:
{ "id": "M-1001", "status": "resolved", "updatedAt": "2025-10-12T09:30:00Z" }

Error Response:
Code: 400/401/403/404
{ "error": { "code": 400, "message": "Invalid payload" } }

## Feedback (Week 8 – initial)

Feedback object
{
  "id": "F-1",
  "markerId": "MK-1",
  "assignmentId": "A-1001",
  "moderationId": "M-1001",
  "message": "Please align with rubric criterion #2",
  "createdAt": "2025-09-03T11:00:00Z"
}

### POST /feedback
Creates a feedback entry from coordinator to marker. (role: coordinator)

Headers
Content-Type: application/json
Authorization: Bearer <JWT>

Success Response:
Code: 200
Content: 
{
  "id": "F-1",
  "markerId": "MK-1",
  "assignmentId": "A-1001",
  "moderationId": "M-1001",
  "message": "Please align with rubric criterion #2",
  "createdAt": "2025-09-03T11:00:00Z"
}


Error Response:
Code: 400
Content: 
{ "error": { "code": 400, "message": "Invalid payload" } }
Code: 401/403
Content: 
{ "error": { "code": 401, "message": "Unauthorized" } }

### GET /feedback
Returns a paginated list of feedback entries.

Query (optional)
    markerId (string)
    assignmentId (string)
    page (int, default 1)
    pageSize (int, default 20)

Headers
    Authorization: Bearer <JWT>

Success Response:
Code: 200
Content:
{
  "items": [ { "...": "feedback_object" } ],
  "page": 1,
  "pageSize": 20,
  "total": 1
}

Error Format (Unified)
{ "error": { "code": 401, "message": "Unauthorized" } }

## Change Policy
    Field names frozen from Week 7 for Login and Assignments.

    Only additive changes allowed (new fields); no renaming/removal without FE/DB agreement.

## Change Log
    2025-09-15 — /assignments data access refactored to Repository layer (default backend: mock; contract unchanged). Future switch via DATA_BACKEND=sqlite|db.