#Login

Auth token object
{
token: string (JWT HS256)
role: string (coordinator|marker)
}

POST /login
Creates a session and returns a JWT.

URL Params
None

Data Params
{
email: string
password: string
}

Headers
Content-Type: application/json

Success Response:
Code: 200
Content:
{
token: "<JWT>",
role: "coordinator"
}

Error Response:
Code: 401
Content: { error: "Invalid credentials" }

Notes

Test accounts (Week 7 mock): coord@example.com
 / pass, marker@example.com
 / pass

JWT expiry: configured by server (e.g., 8 hours)

#Assignments

Assignment object
{
id: string
title: string
dueDate: datetime (ISO 8601)
status: string (current|history)
discrepancyCount: integer
}

GET /assignments
Returns a paginated list of assignments (Week 7 mock).

URL Params
Optional:
status=[current|history]
page=[integer, default=1]
pageSize=[integer, default=20]

Data Params
None

Headers
Content-Type: application/json
Authorization: Bearer <JWT Token> // optional in Week 7 mock; required later

Success Response:
Code: 200
Content:
{
items: [
{ <assignment_object> },
{ <assignment_object> }
],
page: 1,
pageSize: 20,
total: 3
}

Error Response:
Code: 401
Content: { error: "Unauthorized" }

Notes

Field names are frozen from Week 7. Only additive changes allowed later.

#Moderations (Week 8 – to be defined)

Moderation object
{
id: string
assignmentId: string
studentId: string
markerId: string
rubric: [
{
criterion: string
markerScore: number
coordinatorScore: number
delta: number
}
]
overall: {
markerTotal: number
coordinatorTotal: number
delta: number
}
status: string (open|resolved)
createdAt: datetime (ISO 8601)
updatedAt: datetime (ISO 8601)
}

GET /moderations/:id
Returns the specified moderation detail.

URL Params
Required: id=[string]

Data Params
None

Headers
Content-Type: application/json
Authorization: Bearer <JWT Token>

Success Response:
Code: 200
Content: { <moderation_object> }

Error Response:
Code: 404
Content: { error: "Moderation not found" }
OR
Code: 401
Content: { error: "Unauthorized" }

POST /moderations/:id/resolve
(Week 8) Resolve a moderation with coordinator’s decision.

URL Params
Required: id=[string]

Data Params
{
coordinatorNotes: string
adjustedScores: [
{ criterion: string, coordinatorScore: number }
]
}

Headers
Content-Type: application/json
Authorization: Bearer <JWT Token> // role=coordinator

Success Response:
Code: 200
Content: { id: "M-1001", status: "resolved", updatedAt: "2025-10-12T09:30:00Z" }

Error Response:
Code: 400/401/403/404 with error message

#Feedback (Week 8 – to be defined)

Feedback object
{
id: string
markerId: string
assignmentId: string
moderationId: string
message: string
createdAt: datetime (ISO 8601)
}

POST /feedback
Creates a feedback entry from coordinator to marker.

URL Params
None

Data Params
{
markerId: string
assignmentId: string
moderationId: string
message: string
}

Headers
Content-Type: application/json
Authorization: Bearer <JWT Token> // role=coordinator

Success Response:
Code: 200
Content: { <feedback_object> }

Error Response:
Code: 400
Content: { error: "Invalid payload" }
OR
Code: 401/403
Content: { error: "Unauthorized" }

GET /feedback
Returns a paginated list of feedback entries.

URL Params
Optional:
markerId=[string]
assignmentId=[string]
page=[integer, default=1]
pageSize=[integer, default=20]

Data Params
None

Headers
Content-Type: application/json
Authorization: Bearer <JWT Token>

Success Response:
Code: 200
Content:
{
items: [
{ <feedback_object> }
],
page: 1,
pageSize: 20,
total: 1
}

#Error Format (consistent JSON)
Simple:
{ error: "Unauthorized" }

Detailed:
{ error: { code: 401, message: "Unauthorized" } }

#Change Policy

Field names are frozen from Week 7 for Login and Assignments.

Only additive changes allowed (new fields).

No renaming or removal without agreement from FE/DB.