from django.contrib import admin
from .models import Users, Event, Registration, Attendance, Feedback


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role")
    list_filter = ("role",)
    search_fields = ("name", "email")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "start_datetime", "end_datetime", "created_by")
    list_filter = ("type", "created_by")
    search_fields = ("title", "description", "location")
    ordering = ("-start_datetime",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "student", "status", "registered_at")
    list_filter = ("status", "event")
    search_fields = ("student__name", "student__email", "event__title")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "registration", "present", "checked_in_at")
    list_filter = ("present",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "registration", "rating", "submitted_at")
    list_filter = ("rating",)
