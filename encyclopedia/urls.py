from django.urls import path

from . import views

urlpatterns = [
    # views.index -> index é uma função em views.py
    # name="index" -> index é um nome arbitrário para a rota (url)
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry")
]

# wiki/<str:title> cria um padrão de URL.
# Qualquer coisa depois de wiki/ será capturada como uma string e passada para a view com o nome de title.
# views.entry_page é o nome da função de view que vamos criar no próximo passo para lidar com essa rota.