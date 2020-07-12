import shutil, tempfile, os, os.path, re, markdown
from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path, NoReverseMatch
from django.core.files.storage import default_storage

from . import util, views


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")
    pagename = forms.CharField(label="pagename")
    NewContent = forms.CharField(label="NewContent")
    entry = forms.CharField(label="entry")


#Index Page return all itens from enciclopedia
def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })


"""
   NewPage - falta:
   Markdown content for the page.
   when the page is saved, if an encyclopedia entry already exists with the provided title, the user should
   be presented with an error message.
"""
def NewPage(request):
    if request.method == "POST":
        print(f"Entrei no post do New Page")

        title = request.POST["NewTitle"]
        content = request.POST["NewContent"]
        rastag = "# "+title
        pagename = "Wiki/"+title.capitalize()

        html = markdown.markdown(content)

        context={
             "page": "EntryPage",
             "pagename":pagename,
             "entry":title.upper(),
             "title":title,
             "content":content,
             "entries":util.save_entry(title=title, content=content),
             "entries":insert_line(file_name=f"entries/{title}.md", line_number= 1, conteudo=rastag),
             "encyclopedia": request.session["Pwiki"]
        }

        return render(request,"encyclopedia/EntryPage.html",context)
    else:
        return render(request, "encyclopedia/NewPage.html")


"""
   Entry Page: Falta:
   Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be
   converted to HTML before being displayed to the user. You may use the python-markdown2 package
   to perform this conversion, installable via pip3 install markdown2.

"""
def EntryPage(request, entry):
    print("Estou na Entry Page")
    page = "EntryPage"
    title = str(entry)
    pagename = "Wiki/"+title.capitalize()
    content = util.get_entry(title=title)
    html = markdown.markdown(content)

    context = {
        "entry" :title,
        "pagename": pagename,
        "title": title,
        "content":html,
        "page": page,
        "encyclopedia": request.session["Pwiki"]
        }
    return render(request, "encyclopedia/EntryPage.html", context)


def Search(request):
    if request.method == "POST":
        seekfile = request.POST["q"]
        #seekword = "%"+request.POST["q"]+"%"
        seekword = request.POST["q"]
        count = 0
        _, filenames = default_storage.listdir("entries")
        arquivo = seekfile+".md"

        if arquivo in filenames:
           count += 1
           title = seekfile
           message= "You´re Lucky! We found "+str(count)+ " file"
           pagename = "Wiki/"+title.capitalize()
           Searchentry = title.upper()
           print(f"Achei arquivo : ",arquivo, message , pagename, title)
           context = {
                "Searchentry" :Searchentry,
                "pagename": pagename,
                "title": title,
                "message":message,
                "content":util.get_entry(title=title),
                "encyclopedia": request.session["Pwiki"]
                }
           return render(request, "encyclopedia/EntryPage.html", context)

        else:
            TitulosAchados = []
            print(f"lista de arquivos a procurar",filenames)

            for filename in filenames:
                print(f"Trying to find string :", seekword,"in:", filename)
                meuarquivo= "entries/"+filename

                with open(meuarquivo) as myfile:
                    if seekword in myfile.read():
                        count = count + 1
                        titulo = re.sub(r"\.md$", "", filename) #o título é o nome do arquivo sem extensão
                        print(f'Achei :', seekword, "em", meuarquivo )
                        print(f"vou salvar para imprimir: ",titulo , str(count))
                        TitulosAchados.append(titulo)

            if count == 0:
                context ={
                    "count" : count,
                    "seekword":seekword,
                    "message":"Error 404. No file or Text with this content was found."
                    }
                return render(request, "encyclopedia/Search.html", context)
            else:
                context ={
                    "seekword":seekword,
                    "count":count,
                    "titulo": titulo,
                    "TitulosAchados": TitulosAchados,
                    "encyclopedia": request.session["Pwiki"]
                     }
                return render(request, "encyclopedia/Search.html", context)
    else:
        context ={
            "message":"Nao entrei no Post",
            "encyclopedia": request.session["Pwiki"]
            }
        return render(request, "encyclopedia/Search.html", context)


"""
Edit Page:  Falta:
The textarea should be pre-populated with the existing Markdown content of the page.
(i.e., the existing content should be the initial value of the textarea).
The user should be able to click a button to save the changes made to the entry.
Once the entry is saved, the user should be redirected back to that entry’s page.
"""

def EditPage(request):
    print("Estou na  Edit Page:")

    if request.method == "POST":
        entry = str(request.POST["entry"])
        title = str( request.POST["title"])
        print("Reading:" , "Título:",title, "Entry:", entry)

        content =util.get_entry(title)

        NewContent= ""       # request.POST["NewContent"]
        print("Will Save:", NewContent)


        if len( NewContent) >0:
            pagename = "Wiki/"+title
            filename =  f"entries/{title}.md"


            with open (filename, "w") as myfile:
                myfile.seek(0,0)
                myfile.write(NewContent)
                myfile.save()

            context={
                     "page": "EntryPage",
                     "pagename":pagename,
                     "entry":entry,
                     "title":title,
                     "content":util.get_entry(title),
                     "encyclopedia": request.session["Pwiki"]
                }
            return render(request, "encyclopedia/EntryPage.html", context)

        context = {
                "title": title,
                "entry": entry,
                "content" : util.get_entry(title),
                "encyclopedia": request.session["Pwiki"]

        }

        return render(request, "encyclopedia/EditPage.html",context)


    #    else:
    #        return render(request, "encyclopedia/EditPage.html",{"message":" The content is empty, please try again"})
    else:
        context = {
                "message":"Empty Form didn´t get into POST",

            }

        return render(request, "encyclopedia/EditPage.html" ,context)









#Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

def RandomPage(request):
    if request.method == "GET":
        return HttpResponse("Error. Wrong request method for Random")
    else:
        return HttpResponseRedirect(reverse("RandomPage"))


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






#utils for add latter

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True

    return False


def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results
