from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

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
