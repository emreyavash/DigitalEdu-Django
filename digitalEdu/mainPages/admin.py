from django.contrib import admin
from .models import Category, Course,Instructor,ContactMessage
from django.utils.safestring import mark_safe
# Register your models here.
class CoursesAdmin(admin.ModelAdmin):
    list_display=("courseName","is_active","is_home","selected_category",)
    list_editable=("is_active","is_home",)
    search_fields=("title",)
    readonly_fileds=("slug",)
    list_filter=("is_active","is_home","categoryId")

    def selected_category(self, obj):
        html = "<ul>"

        for category in obj.categoryId.all():
            html +="<li>"+category.name+"</li>"

        html+="</ul>"
        return mark_safe(html)

admin.site.register(Course,CoursesAdmin)
admin.site.register(Instructor)
admin.site.register(ContactMessage)
admin.site.register(Category)
