from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	fields = ['user']
	list_display = ['__str__', 'getNickname', 'getId', 'getVect']
	
	def getId(self,obj):
		return obj.user.id
	getId.admin_order_field = 'user__id'

	def getNickname(self,obj):
		return obj.user.username
	getNickname.admin_order_field = 'user__username'
	getNickname.short_description = 'Nickname'

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
