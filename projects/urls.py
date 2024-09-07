from django.urls import path
from .views import ProjectList
from .views import index
from .views import save_project
from .views import add_items
from .views import admin
from .views import project_delete

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('admin/', admin, name='admin'),
    path('',index, name='index'),
    path('add_items/', add_items, name='add_items'),
    path('delete/<int:project_id>/', project_delete, name='delete'),
]

