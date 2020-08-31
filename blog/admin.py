from django.contrib import admin
from .models import Post

# Register your models here.


# registers Post class and the wrapped ModelAdmin class to admin site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status', 'created', 'updated', 'body')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body', 'created')
    prepopulated_fields = {'slug': ('title',)}  # ??
    raw_id_fields = ('author',)  # displayes id of the author instead of name
    date_hierarchy = 'created'  # created a a date navigator hierarchy on the top
    # creates list order, overrides Meta class of Post
    ordering = ('status', 'publish')
