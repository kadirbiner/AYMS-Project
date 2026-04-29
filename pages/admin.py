from django.contrib import admin
from .models import Profile, EmergencyContact
from .models import EmergencyAlert

class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1

# ProfileAdmin'i yalnızca bir kez kaydediyoruz
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number", "email", "user")
    list_display_links = ("first_name", "phone_number")
    list_filter = ("first_name", "email")
    search_fields = ("first_name",)
    inlines = [EmergencyContactInline]  # EmergencyContact'ı Profile ile birlikte göster

# EmergencyContactAdmin
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "relationship", "phone_number")
    list_display_links = ("name", "phone_number")
    list_filter = ("name",)
    search_fields = ("name",)



class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ( 'user','latitude', 'longitude', )
    
    

admin.site.register(EmergencyAlert, EmergencyAlertAdmin)