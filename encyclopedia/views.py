from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Função que receberá o title da url,
# busca o arquivo corresponde com util.get_entry()
# e renderiza uma nova página com o conteúdo.
def entry_page(request, title):
    # Procura um arquivo md com o título recebido e armazena o conteúdo do arquivo em content_md
    content_md = util.get_entry(title)
    if content_md is None:
        # Se a entrada não existir, mostre uma página de erro (vamos criá-la)
        return render(request, "encyclopedia/error.html", {
            "message": f"A página '{title}' não foi encontrada."
        })
    else:
        # Converte o texto de Markdown para HTML
        content_html = markdown2.markdown(content_md)
        # Se a entrada existir, mostre a página com o conteúdo
        # Renderiza entry.html, enviando o título e o content já convertido
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })
    
# Função de busca
def search(request):
    # Pega o termo da busca da URL (?q=...)
    query = request.GET.get('q', '')

    # Pega a lista de todas as entradas
    all_entries = util.list_entries()

    # 1. Checa por um correspondência exata (ignora maiúsculas/minúsculas)
    for entry in all_entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", args=[entry]))
        
    # 2. Se não houver correspondência exata, busca por substrings
    results = [entry for entry in all_entries if query.lower() in entry.lower()]

    # Renderiza a página de resultados, passando os resultados encontrados
    return render(request, "encyclopedia/search_results.html", {
        "results": results,
        "query": query
    })

def create_page(request):
    # Se o formulário foi enviado (POST)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Verifica se a entrada com este título já existe
        if util.get_entry(title) is not None:
            # Se existir, renderiza a página de erro
            return render(request, "encyclopedia/create_page.html", {
                "error": "An entry with this title already exists. Please choose a different title."
            })
        
        # Se não existir, salva a nova entrada e redireciona
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
    # Esse é o comando que mostra a página de criação, se a requisição for GET  
    return render(request, "encyclopedia/create_page.html")

# Função que exibe o formulário e salva as alterações
def edit_page(request, title):
    # Pega o conteúdo original da entrada
    original_content = util.get_entry(title)

    # Se a requisição for POST (formulário enviado)
    if request.method == "POST":
        # Pega o novo conteúdo do formulário
        new_content = request.POST.get ("content")

        # Salva o conteúdo atualizado
        util.save_entry(title, new_content)

        # Redireciona de volra para a página de entrada
        return HttpResponseRedirect(reverse("entry, args=[title]"))
    
    # Se a requisição for GET, e não POST (ou seja, apenas visitando a página de edição)
    else:
        # Renderiza a página de edição, passando o título e o contéudo original
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": original_content
        })
    
def random_page(request):
    # Redireciona o usuário para uma página aleatória de entrada
    all_entries = util.list_entries()

    # Escolhe um título aleatoriamente da lista
    random_title = random.choice(all_entries)

    # Redireciona para a página escolhida
    return HttpResponseRedirect(reverse("entry", args=[random_title]))