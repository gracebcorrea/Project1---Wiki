import shutil, tempfile, os, os.path, re

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path
from django.core.files.storage import default_storage

from . import util, views


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")
    pagename = forms.CharField(label="pagename")
    tipo= forms.CharField(label="tipo")

#Index Page return all itens from enciclopedia
def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })


"""New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create
a new encyclopedia entry.
Users should be able to enter a title for the page and, in a textarea, should be able to enter the
Markdown content for the page.
Users should be able to click a button to save their new page.
when the page is saved, if an encyclopedia entry already exists with the provided title, the user should
 be presented with an error message.
Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s
page.
"""
def NewPage(request):
    if request.method == "POST":
        print(f"Entrei no post do New Page")
        title = request.POST["NewTitle"]
        content = request.POST["NewContent"]
        rastag = "# "+title

        return render(request,"encyclopedia/index.html",{
             "entries":util.save_entry(title=title, content=content),
             "entries":insert_line(file_name=f"entries/{title}.md", line_number= 1, conteudo=rastag),
             "entries": util.list_entries(),
             "encyclopedia": request.session["Pwiki"]
        })
    else:
        return render(request, "encyclopedia/NewPage.html")


"""Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry,
should render a page that displays the contents of that encyclopedia entry.
The view should get the content of the encyclopedia entry by calling the appropriate util function.
If an entry is requested that does not exist, the user should be presented with an error page
indicating that their requested page was not found.
   If the entry does exist, the user should be presented with a page that displays the content of
the entry

  Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be
converted to HTML before being displayed to the user. You may use the python-markdown2 package
to perform this conversion, installable via pip3 install markdown2.
Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the
Markdown to HTML conversion without using any external libraries, supporting headings, boldface text,
unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.
"""
def EntryPage(request, entry):
    print("Estou na Entry Page")

    title = entry
    pagename = "Wiki/"+title.capitalize()
    tipo="ListEntry"
    print(title,pagename, tipo)

    context = {
             "entry" :title.upper(),
             "pagename": pagename,
             "title": title,
             "tipo": tipo,
             "content":util.get_entry(title=title)

             }
    return render(request, "encyclopedia/EntryPage.html", context)


"""
Search: Allow the user to type a query into the search box in the sidebar to search
for an encyclopedia entry.
If the query matches the name of an encyclopedia entry, the user should be redirected
to that entry’s page.
If the query does not match the name of an encyclopedia entry, the user should instead
be taken to a search results page that displays a list of all encyclopedia entries that
have the query as a substring. For example, if the search query were Py, then Python
should appear in the search results.
Clicking on any of the entry names on the search results page should take the user to that entry’s page.
"""

def Search(request):
    if request.method == "POST":
        tipo = "Search"
        seekfile = request.POST["q"]
        seekword = "%"+request.POST["q"]+"%"
        count = 0
        _, filenames = default_storage.listdir("entries")
        arquivo = seekfile+".md"

        print(f"Estou no Post de Search", seekword, arquivo)

        if arquivo in filenames:
           count += 1
           title = seekfile
           message= "You´re Lucky! We found "+str(count)+ " file"
           pagename = "Wiki/"+title.capitalize()
           print(f"Achei arquivo : ",arquivo, message , pagename, title)
           context = {
                     "entry" :title.upper(),
                     "pagename": pagename,
                     "title": title,
                     "tipo": tipo,
                     "message":message,
                     "content":util.get_entry(title=title)
                     }
           return render(request, "encyclopedia/EntryPage.html", context)

        else:
            print("Não achei arquivo com este nome",arquivo)
            for filename in filenames:
                arquivo=filename
                title = re.sub(r"\.md$", "", arquivo) #o título é o nome do arquivo sem extensão

                print("Trying to find string :", seekword,"in:", title)

                try:
                    with  open(arquivo, "r") as file:
                        conteudo = arquivo.readlines()
                        print("entrei no arquivo:", arquivo)

                    print(len(conteudo),conteudo[:256] )

                    if find(seekword) in conteudo:
                        count =+ 1
                        print(f"achei parte em um arquivo", count, seekword )

                        context =  {
                           "name" : title ,
                           "pagename" :pagename.upper() ,
                           "title" :title ,
                           "message":"Lista as opções",
                           "encyclopedia": request.session["Pwiki"]
                           }
                        return render(request, "encyclopedia/SearchResults.html", context)

                except:
                    print( "Nothing on:" , filename)


            if count == 0:
               context = {
                      "message":"Error 404. No file or Text with this content was found.",
                      "encyclopedia": request.session["Pwiki"]
                      }
               return render(request, "encyclopedia/SearchResults.html", context)


    else:
        context = {
         "message":"Nao entrei no Post",
         "encyclopedia": request.session["Pwiki"]
        }
        return render(request, "encyclopedia/SearchResults.html", context)




#Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

def RandomPage(request):
    if request.method == "GET":
        return HttpResponse("Error. Wrong request method for Random")
    else:
        return HttpResponseRedirect(reverse("RandomPage"))

#Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
#The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
#The user should be able to click a button to save the changes made to the entry.
#Once the entry is saved, the user should be redirected back to that entry’s page.

def EditPage(request):
    return (request, "encyclopedia/EditPage.html",{"message":"Edit Page"})





#insert text on the file in any line
# incluir o texto "xyz" na terceira linha do arquivo
#insert_line('arquivo.txt', 3, 'xyz')
def insert_line(file_name, line_number, conteudo):
    with open(file_name) as orig, \
         tempfile.NamedTemporaryFile('w', delete=False) as out:
        for i, line in enumerate(orig): # percorre o arquivo linha a linha
            if i == line_number - 1:
                out.write(f'{conteudo}\n')
                out.write(f'\n')
            out.write(line)
    shutil.move(out.name, file_name)
