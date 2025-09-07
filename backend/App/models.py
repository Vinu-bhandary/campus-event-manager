from django.db import models
from django.utils import timezone
import uuid


# ---------------------------
# USER MODEL
# ---------------------------
class Users(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # store hashed in real apps
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.role})"


# ---------------------------
# EVENT MODEL
# ---------------------------
class Event(models.Model):
    EVENT_TYPES = [
        ("workshop", "Workshop"),
        ("fest", "Fest"),
        ("seminar", "Seminar"),
        ("talk", "Tech Talk"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=EVENT_TYPES, default="other")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return f"{self.title} ({self.type})"


# ---------------------------
# REGISTRATION MODEL
# ---------------------------
class Registration(models.Model):
    STATUS_CHOICES = [
        ("registered", "Registered"),
        ("cancelled", "Cancelled"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="registered")

    class Meta:
        unique_together = ("event", "student")

    def __str__(self):
        return f"{self.student.name} → {self.event.title}"


# ---------------------------
# ATTENDANCE MODEL
# ---------------------------
class Attendance(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="attendance")
    present = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.registration.student.name} - {self.registration.event.title}: {'Present' if self.present else 'Absent'}"


# ---------------------------
# FEEDBACK MODEL
# ---------------------------
class Feedback(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="feedback")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback: {self.registration.student.name} → {self.registration.event.title}"


class UserToken(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="token")
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.email}"
