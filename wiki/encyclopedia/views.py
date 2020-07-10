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
    content = util.get_entry(title=title)
    html = markdown.markdown(content)

    context = {
        "entry" :title.upper(),
        "pagename": pagename,
        "title": title,
        "content":html,

        #"content":util.get_entry(title=title)
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
                "content":util.get_entry(title=title)
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

                    #    Searchentry=title.upper()
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
                    "TitulosAchados": TitulosAchados             #list(sorted(TitulosAchados))
                     }
                return render(request, "encyclopedia/Search.html", context)




    else:
        context ={
            "message":"Nao entrei no Post",
            "encyclopedia": request.session["Pwiki"]
            }
        return render(request, "encyclopedia/Search.html", context)

"""
Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
The user should be able to click a button to save the changes made to the entry.
Once the entry is saved, the user should be redirected back to that entry’s page.
"""
def EditPage(request):
    if request.method == "POST":
        title= request.POST["title"]
        content = util.get_entry(title=title)

        NewTitle = title
        #NewContent = request.POST["NewContent"]


        print("Estou no Post do Edit Page" , title,content )
    #    print("Vou gravar novo conteúdo" , NewTitle, NewContent)

        #filename= default_storage.open(f"entries/{title}.md")

        #with open(filename, 'w+',) as Myfile:
        #    MyFile.seek(0,0)
        #    MyFile.write(NewContent+"\n")


        context = {
                "title": title,
                "content":content,
                "Newtitle":NewTitle,
            #    "NewContent":NewContent
                }
        return render(request, "encyclopedia/EditPage.html",context)

    else:
        context ={
                "title": None,
                "content":None,
                "Newtitle":None,
                "NewContent":None
                }
        return render(request, "encyclopedia/EditPage.html",context)


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
