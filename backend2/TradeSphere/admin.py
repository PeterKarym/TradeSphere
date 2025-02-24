from django.contrib import admin
from .models import EmailVerification

# Register your models here.

# Register EmailVerification model
@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'verification_code', 'created_at')
