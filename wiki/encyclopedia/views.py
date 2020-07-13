import shutil, tempfile, os, os.path, re, markdown,random, markdown2

from markdown2 import Markdown
from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path, NoReverseMatch
from django.core.files.storage import default_storage


from . import util, views


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

"""
def NewPage(request):
    if request.method == "POST":
        print(f"Entrei no post do New Page")

        title = request.POST["NewTitle"]
        _, filenames = default_storage.listdir("entries")
        arquivo = title+".md"
        print(title, filenames)
        if arquivo in filenames:
            context={
                    "message" : "This Title already exists, please choose other Title"
                    }
            return render(request, "encyclopedia/NewPage.html", context)

        else:
            content = request.POST["NewContent"]
            rastag = "# "+title
            pagename = "Wiki/"+title.capitalize()


            context={
                "page": "EntryPage",
                "pagename":pagename,
                "entry":title.capitalize(),
                "title":title,
                "content":markdown2.markdown(content),
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
    #html = markdown2.markdown(content)

    context = {
        "entry" :title,
        "pagename": pagename,
        "title": title,
        "content":markdown2.markdown(content),
        "page": page,
        "encyclopedia": request.session["Pwiki"]
        }
    return render(request, "encyclopedia/EntryPage.html", context)


def EditPage(request, title):
    Etitle =  title
    print("EditPage :", Etitle)
    if request.method == "POST":
        Textsize=0

        print("Reading:" , "Título:",Etitle)

        content =util.get_entry(Etitle)
        print("Old Content", content)

        NewTextArea= request.POST["NewTextArea"]
        #NewTextArea= request.POST.get("NewTextArea")
        Textsize= len(NewTextArea)

        print("Will Save:",Textsize )


        if Textsize:
            pagename = "Wiki/"+Etitle.capitalize()
            filename =  f"entries/{Etitle}.md"
            print(pagename, filename)

            with open (filename, "w") as myfile:
                myfile.seek(0,0)
                myfile.write(NewTextArea)


            context = {
                "title": Etitle,
                "entry": Etitle,
                "content" :markdown2.markdown( util.get_entry(Etitle)),
                "encyclopedia": request.session["Pwiki"]
            }
            return render(request, "encyclopedia/EntryPage.html",context)
        else:
            context = {
                "entry": Etitle,
                "title": Etitle,
                "content" : markdown2.markdown( util.get_entry(Etitle)),
                "message":" The New content is empty, please try again",
                "encyclopedia": request.session["Pwiki"]
            }
            return render(request, "encyclopedia/EditPage.html",context)
    else:
        context = {
                "title":title,
                "content" : util.get_entry(title)
            }
        return render(request, "encyclopedia/EditPage.html" ,context)




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


def RandomPage(request):
    if request.method == "GET":
        Max=0
        randonposition=0
        filenames= []

        filenames = util.list_entries()
        #number or list itens
        Max= int(len(filenames))
        #List uses 0 as first file, so i have to count -1 for the range
        randonposition=(random.randint(0,(Max-1)))
        drawnfile = str(filenames[randonposition])
        print("titulo sorteado", drawnfile)

        drawncontent = util.get_entry(drawnfile)

        context = {
                "Entry":drawnfile.capitalize(),
                "pagename":drawnfile.capitalize(),
                "randonposition":randonposition,
                "title":drawnfile,
                "content":drawncontent
         }

        return render(request, "encyclopedia/EntryPage.html" ,context)
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
