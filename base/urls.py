from django.urls import path
from . import views
from .views import Tasks, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Use LogoutView directly
    path('register/', RegisterPage.as_view(), name='register'),
    path('', Tasks.as_view(), name='tasks'),  # Tasks is a class so we use .as_view() to convert to a view
    path('task/<str:pk>/', TaskDetail.as_view(), name='task_detail'),  # TaskDetail is a class so we use .as_view()
    path('taskCreation/', TaskCreate.as_view(), name='task_create'),
    path('taskUpdate/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('taskDelete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
]
  #the name is passed to the template to be used in the href attribute of the anchor tag