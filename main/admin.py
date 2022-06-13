from django.contrib import admin
from .models import TODO, User
# Register your models here.
@admin.register(TODO)
class TODOAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ( 'title' ,'added_date','due_on',)
    search_fields = ('id','title',)
    ordering = ('-added_date',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at',)