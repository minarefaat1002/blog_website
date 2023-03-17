from django.urls import path
from . import views

urlpatterns = [
    path('',views.blogs,name='blogs'),
    path('blog/<str:pk>/',views.blog,name="blog"),
    path('like/',views.like,name="like"),
    path('create-blog/', views.createBlog, name="create-blog"),
    path('update-blog/<str:pk>/', views.updateBlog, name="update-blog"),
    path('delete-blog/<str:pk>',views.deleteBlog,name='delete-blog'),
    path('fav/<str:id>/',views.favorite_add,name="favorite-add"),
    path('favorites/',views.favorites,name="favorites"),
    path('category/<str:category>/',views.category,name="category"),
]