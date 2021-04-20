from . import views
from django.urls import path

urlpatterns = [
    path('', views.main, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('addJob', views.addJob, name="addJob"),    
    path('view/<int:id>', views.get_job, name="get_job"),    
    path('edit/<int:id>', views.edit, name="edit"),
    path('update', views.update, name="update"),
    path('remove/<int:id>', views.remove, name="remove"),
    path('addMyJob/<int:id>', views.addMyJob, name="addMyJob"),
    path('removeMyJob/<int:id>', views.removeMyJob, name="removeMyJob")
] 