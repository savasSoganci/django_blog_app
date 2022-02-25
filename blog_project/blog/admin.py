from django.contrib import admin
from django.forms import ModelForm, Textarea
from .models import Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ('title', 'slug', 'author', 'publish',
    'status','created_on','updated_on','image','url','email')
   search_fields = ('title', 'body')
   prepopulated_fields = {'slug': ('title',)} #The attribute prepopulated_fields tells the admin application to automatically fill the field slug - in this case with the text entered into the name field.
   #raw_id_fields = ('author',)
   date_hierarchy = 'publish'
   ordering=('status','publish')
   autocomplete_fields = ['author'] #database'i parça parça getirmeyi sağlıyor.

