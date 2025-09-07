from ninja import NinjaAPI, Schema
from typing import List, Optional, Union
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
import uuid
from datetime import datetime
from .models import Users, Event, Registration, Attendance, Feedback, UserToken


api = NinjaAPI(title="Campus Event Manager API")

# ========================================================
# HELPER FUNCTIONS
# ========================================================

def get_user_from_token(token: str):
    try:
        return UserToken.objects.get(token=token).user
    except UserToken.DoesNotExist:
        return None


# ========================================================
# SCHEMAS
# ========================================================

class UserIn(Schema):
    name: str
    email: str
    password: str
    role: str  # "admin" or "student"

class UserOut(Schema):
    id: int
    name: str
    email: str
    role: str

class EventIn(Schema):
    title: str
    description: Optional[str] = None
    type: str
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    capacity: Optional[int] = None

class EventOut(Schema):
    id: int
    title: str
    type: str
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str]
    created_by: str

class RegistrationIn(Schema):
    event_id: int

class AttendanceIn(Schema):
    registration_id: int
    present: bool

class FeedbackIn(Schema):
    registration_id: int
    rating: int
    comment: Optional[str] = None


# ========================================================
# AUTHENTICATION
# ========================================================

@api.post("/users/", response=UserOut)
def create_user(request, payload: UserIn):
    """Register a new user (admin or student)."""
    user = Users.objects.create(**payload.dict())
    return user


@api.post("/login/")
def login(request, email: str, password: str):
    """Login with email/password → returns token."""
    try:
        user = Users.objects.get(email=email, password=password)
    except Users.DoesNotExist:
        return {"error": "Invalid credentials"}

    token, created = UserToken.objects.get_or_create(user=user)
    if not created:  # refresh token each login
        token.token = str(uuid.uuid4())
        token.save()
    return {"token": token.token, "user_id": user.id, "role": user.role}


@api.post("/logout/")
def logout(request, token: str):
    """Logout → deletes token."""
    try:
        user_token = UserToken.objects.get(token=token)
        user_token.delete()
        return {"success": True}
    except UserToken.DoesNotExist:
        return {"error": "Invalid token"}


# ========================================================
# EVENTS
# ========================================================

@api.post("/events/", response=Union[EventOut, dict])
def create_event(request, payload: EventIn, token: str):
    """Admin creates event."""
    user = get_user_from_token(token)
    if not user or user.role != "admin":
        return {"error": "Unauthorized"}

    event = Event.objects.create(**payload.dict(), created_by=user)
    return {
        "id": event.id,
        "title": event.title,
        "type": event.type,
        "start_datetime": str(event.start_datetime),
        "end_datetime": str(event.end_datetime),
        "location": event.location,
        "created_by": user.name,
    }


@api.get("/events/", response=List[EventOut])
def list_events(request, token: Optional[str] = None):
    """List all events (students + admins)."""
    events = Event.objects.select_related("created_by").all()
    return [
        {
            "id": e.id,
            "title": e.title,
            "type": e.type,
            "start_datetime": str(e.start_datetime),
            "end_datetime": str(e.end_datetime),
            "location": e.location,
            "created_by": e.created_by.name,
        }
        for e in events
    ]


# ========================================================
# REGISTRATIONS
# ========================================================

@api.post("/registrations/")
def register_event(request, payload: RegistrationIn, token: str):
    """Student registers for an event."""
    user = get_user_from_token(token)
    if not user or user.role != "student":
        return {"error": "Unauthorized"}

    event = get_object_or_404(Event, id=payload.event_id)
    reg, created = Registration.objects.get_or_create(event=event, student=user)
    return {"registration_id": reg.id, "status": reg.status}


@api.get("/my-registrations/")
def my_registrations(request, token: str):
    user = get_user_from_token(token)
    if not user or user.role != "student":
        return {"error": "Unauthorized"}

    regs = Registration.objects.filter(student=user).select_related("event").annotate(attended=Count("attendance", filter=Q(attendance__present=True)))

    return [
        {
            "registration_id": r.id,   # ✅ add this
            "event": r.event.title,
            "status": r.status,
            "registered_at": str(r.registered_at),
            "attendance": r.attended > 0,
        }
        for r in regs
    ]


# ========================================================
# ATTENDANCE
# ========================================================

@api.post("/attendance/")
def mark_attendance(request, payload: AttendanceIn, token: str):
    """Admin marks student attendance."""
    user = get_user_from_token(token)
    if not user or user.role != "admin":
        return {"error": "Unauthorized"}

    reg = get_object_or_404(Registration, id=payload.registration_id)
    att, _ = Attendance.objects.get_or_create(registration=reg)
    att.present = payload.present
    att.save()
    return {"attendance_id": att.id, "present": att.present}


# ========================================================
# FEEDBACK
# ========================================================

@api.post("/feedback/")
def submit_feedback(request, payload: FeedbackIn, token: str):
    """Student submits feedback for event."""
    user = get_user_from_token(token)
    if not user or user.role != "student":
        return {"error": "Unauthorized"}

    reg = get_object_or_404(Registration, id=payload.registration_id, student=user)
    fb, _ = Feedback.objects.update_or_create(
        registration=reg,
        defaults={"rating": payload.rating, "comment": payload.comment}
    )
    return {"feedback_id": fb.id, "rating": fb.rating}


# ========================================================
# REPORTS
# ========================================================

@api.get("/reports/event-popularity/")
def event_popularity(request, token: str):
    """Admin: Event popularity report (by registrations)."""
    user = get_user_from_token(token)
    if not user or user.role != "admin":
        return {"error": "Unauthorized"}

    events = Event.objects.annotate(reg_count=Count("registrations")).order_by("-reg_count")
    return [{"event": e.title, "registrations": e.reg_count} for e in events]


@api.get("/reports/student-participation/")
def student_participation(request, token: str):
    """Admin: Student participation report (attendance count)."""
    user = get_user_from_token(token)
    if not user or user.role != "admin":
        return {"error": "Unauthorized"}

    students = Users.objects.filter(role="student").annotate(
        attended=Count("registrations__attendance", filter=Q(registrations__attendance__present=True))
    )
    return [{"student": s.name, "attended": s.attended} for s in students]
