from django.urls import path

from . import views

urlpatterns = [
    # views.index -> index é uma função em views.py
    # name="index" -> index é um nome arbitrário para a rota (url)
    path("", views.index, name="index"),
    # entry recebida é envaida para a função entry_page em views
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page")
]

# wiki/<str:title> cria um padrão de URL.
# Qualquer coisa depois de wiki/ será capturada como uma string e passada para a view com o nome de title.
# views.entry_page é o nome da função de view para lidar com essa rota.