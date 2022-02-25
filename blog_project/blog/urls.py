from django.urls import path
from . import views
from blog.views import (registration_view, logout_view, login_view, my_repository, add_post, post_slug_update, delete_post,
 update_post)
urlpatterns = [
    path('',views.home, name='blog-home'),
    path('posts/',views.blog_title_getirme,name="index"),
    path('posts/post/<int:id>/',views.blog_object,name='post-content'),
    path('about/',views.about, name='blog-about'),
    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('myrepository/',my_repository,name='repository'),
    path('addpost/',add_post,name='add-post'),
    path('addpost-slug/',post_slug_update,name='add-post-slug'),
    path('posts/delete-post/<int:id>/',delete_post,name='delete-post'),
    path('posts/update-post/<int:id>/',update_post,name='update-post'),
]

