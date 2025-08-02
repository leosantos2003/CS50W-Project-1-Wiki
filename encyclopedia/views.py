from django.shortcuts import render
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
    content_md = util.get_entry(title)
    if content_md is None:
        # Se a entrada não existir, mostre uma página de erro (vamos criá-la)
        return render(request, "encyclopedia/error.html", {
            "message": f"A página '{title}' não foi encontrada."
        })
    else:
        content_html = markdown2.markdown(content_md)
        # Se a entrada existir, mostre a página com o conteúdo
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })