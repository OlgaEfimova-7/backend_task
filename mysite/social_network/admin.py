from django.contrib import admin
from social_network.models import User, FriendList
# Register your models here.

class FriendListInline(admin.TabularInline):
    model = FriendList
    fk_name = "profile"

class UserAdmin(admin.ModelAdmin):
    inlines=(FriendListInline,)

admin.site.register(User, UserAdmin)