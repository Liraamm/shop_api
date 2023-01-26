from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_staff')
    list_filter =(
        ('is_staff', admin.BooleanFieldListFilter),
    )