from django.urls import path, include
from django.conf.urls import url
from insight_journal.resources import EntryResource
from . import views

entry_resource = EntryResource()

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('entry/<int:pk>/', views.entry, name='entry'),
    path('entry/new', views.new, name='new'),
    path('entry/<int:pk>/edit/', views.edit, name='edit'),
    path('entry/<int:pk>/remove/', views.remove, name='remove'),
    url('accounts/signup/$', views.signup, name='signup'),
]
