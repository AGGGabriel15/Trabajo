from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('nuevo/', views.new_estudiante, name="nuevo"),
    path('editar/<int:id>', views.editar, name="editar"),
    path('eliminar/<int:id>', views.eliminar, name="eliminar"),

]
