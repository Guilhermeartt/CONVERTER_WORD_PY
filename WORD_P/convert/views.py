from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from bs4 import BeautifulSoup as bs
import re
from django.conf import settings
import os 
from django.template.loader import render_to_string
from itertools import zip_longest

from .models import MsgModel
from .forms import MsgFormulario


def export_messages_json(request):
    messages = MsgModel.objects.all()  # Obtém todas as mensagens
    messages_data = [
        {
            'messaging_product': message.messaging_product,
            'recipient_type': message.recipient_type,
            'to': message.to,
            'type_msg': message.type_msg,
            # Adicione outros campos conforme necessário
        }
        for message in messages
    ]
    return JsonResponse(messages_data, safe=False)

def card_connections_view(request):
    cards = MsgModel.objects.all()
    return render(request, 'card_connections.html', {'cards': cards})

def card_list(request):
    cards = MsgModel.objects.all()

    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        MsgModel.objects.filter(id__in=selected_messages).delete()

    return render(request, 'card_list.html', {'cards': cards})
    
def delete_selected_messages(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        MsgModel.objects.filter(id__in=selected_messages).delete()
    
    return redirect('card_list')



def create_message(request):
    if request.method == 'POST':
        form = MsgFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card_list')
    else:
        form = MsgFormulario()
    return render(request, 'create_message.html', {'form': form})


def formulario(request):

    initial_values = {
        'messaging_product': "{{ $json['body']['entry'][0]['changes'][0]['value']['messaging_product'] }}",
        'recipient_type': 'individual',
        'to': "{{ $json['body']['entry'][0]['changes'][0]['value']['messages'][0]['from'] }}",
        'type_msg': 'interactive',
        'interactive.type': 'button',
        'header.type': 'text',
        'header.text': 'Seja ProEpi',
        'body.text': 'Que ótimo! Vou te ajudar a fazer parte da nossa rede.\n\nO que você gostaria de fazer?',
        'footer.text': 'Não hesite em usar MENU ou ENCERRAR a qualquer momento.',                     
        'buttons.type': 'reply',
        'reply.id': 'S1',
        'reply.title': 'Associar-se'

        # Outros campos iniciais aqui...
    }
    if request.method == 'POST':
        form = MsgFormulario(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('card_list')  # Redirecionar para a página de listagem de mensagens após o salvamento bem-sucedido
    else:
        form = MsgFormulario()
    
    return render(request, 'formulario.html', {'form': form})



def index(request):
    if request.method == "GET":
        return render(request, 'wordconvert.html')
    elif request.method == "POST":
        files = request.FILES.getlist("my_file")  # Use getlist() to get a list of files
        modified_files = []
        for file in files:
            soup = bs(file, 'html.parser', from_encoding='utf-8')
            modifica(soup)  # Process the file and get the modified content
            modified_files.append(file.name)  # Append the modified file name to the list

        aula = render(request, 'modified_files.html', {'modified_files': modified_files})

        return aula


def modifica(soup): 

        for style_tag in soup.find_all('style'):
            style_tag.extract()
        for script_tag in soup.find_all('script'):
            script_tag.extract()

        pattern = re.compile(r"(.*)(CxSpFirst|CxSpMiddle|CxSpLast)$")
        tags = soup.find_all(class_=pattern)

        for tag in tags:
            class_name = tag.get('class')[0]
            class_without_suffix = re.sub(pattern, r"\1", class_name)
            tag['class'] = [class_without_suffix]

        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            src = img_tag.get('src')
            
            new_src = "/static/" + src
            img_tag['src'] = new_src

        captions = soup.find_all(class_="MsoCaption")
        for caption in captions:
            caption['class'] = caption.get('class', []) + ['figure-caption']
     
        normals = soup.find_all(class_="MsoNormal")
        for normal in normals:
            normal['class'] = normal.get('class', []) + ['fs-5', 'text-justify']
            style_atual = normal.get('style', '')
            style_atual += 'text-align: justify;'
            normal['style'] = style_atual

            linkss = normal.find_all('a')
            for linka in linkss:
                if linka:
                    # Adicionar a classe do Bootstrap ao link
                    linka['class'] = 'text-decoration-none'
                    linka['target'] = '_blank'
                    linka['title'] = 'link externo!'
                    linka['data-bs-toggle'] ='tooltip'
                    linka['data-bs-placement'] = 'top' 

        biolinks = soup.find_all(class_="PRObibliografia")
        for biolink in biolinks:
            biolink['class'] = ['PRObibliografia', 'fs-5', 'text-justify']
            biolink['style'] = ['text-align: justify;']
            if biolink.span:
                biolink.span.unwrap()
            a_tags = biolink.find_all("a")
            for a_tag in a_tags:
                a_tag.span.unwrap()
                text = a_tag.get_text()
                modified_letters = []
                for letter in text:
                    modified_letters.append(letter)
                    modified_letters.append(soup.new_tag('wbr'))
                modified_letters.pop()
                a_tag.clear()
                for element in modified_letters:
                    a_tag.append(element)
                        
        titles = soup.find_all(class_="MsoTitle")
        for title1 in titles:
            title1['class'] = title1.get('class', []) + ['display-4','pt-5', 'pb-2','ttl1', 'nvl0']

        title1s = soup.find_all(class_="PRO1Ttulonumerado")
        for title1 in title1s:
            title1['class'] = title1.get('class', []) + ['display-4','pt-5', 'pb-2', 'ttl1', 'nvl1']
            new_tag = soup.new_tag('div', attrs={'class':'row'})
            new_colun_8 = soup.new_tag('div', attrs={'class':'col-sm-1 float-end mw-100 mh-100 min-vh-10 h-10','style': 'background-color: #eee; border-radius: 10px;'})
            new_colun_4 = soup.new_tag('div', attrs={'class':'col-sm-11 '})
            title1.wrap( new_colun_4)
            new_colun_4.wrap(new_tag)
            new_colun_4.insert_before(new_colun_8)

        title11s = soup.find_all(class_="PRO11Ttulonumerado")
        for title1 in title11s:
            title1['class'] = title1.get('class', []) + ['display-5','pt-5', 'pb-2','ttl1', 'nvl2']

        title111s = soup.find_all(class_="PRO111Ttulonumerado")
        for title1 in title111s:
            title1['class'] = title1.get('class', []) + ['display-5','pt-5', 'pb-2','ttl1', 'nvl3']
            
        imgs = soup.find_all('img')
        for img in imgs:
            add_class = img.get('class', [])
            add_class.extend(['w-100','img-fluid ' ])
            img['class'] = add_class

        figures = soup.find_all(class_="PROimagem")
        for figure in figures:
            figure.name = 'figure'
            figure['class'] = figure.get('class', []) + ['figure', 'pt-3','rounded', 'mx-auto', 'd-block','w-75']

        fig = soup.find_all('figure')
        for figure in fig:    
            if figure is not None:
                next_sibling = figure.find_next_sibling("p")

                if next_sibling is not None and 'MsoCaption' in next_sibling.get('class', []):
                    figure.append(next_sibling.extract())
                    next_sibling.name = 'figcaption'

        figcaption_list = soup.find_all('figcaption')
        for figcaption in figcaption_list:
            
            span_tags = figcaption.find_all('span')
            for span_tag in span_tags:
                span_tag.unwrap()
            
            link = figcaption.find('a')
            if link:
                # Adicionar a classe do Bootstrap ao link
                link['class'] = 'badge bg-secondary text-decoration-none'
                link['target'] = '_blank'
                link['title'] = 'Abrir link em outra página'
                link['data-bs-toggle'] ='tooltip'
                link['data-bs-placement'] = 'top' 
                link.string = "fonte da imagem"


        lista_li = soup.select('p.PROBullets')
        for p in lista_li:
            stylep = p.get('style', '')
            stylep += 'border-radius: 10px;'
            p['class'] = 'list-group-item', 'list-group-item-action','list-group-item-secondary','mb-2','mt-2'
            p['style'] = stylep
            p.name = 'li'
            p.span.extract()

        lis = soup.find_all('li') 
        sequencias_li = []
        for li, proximo_li in zip_longest(lis, lis[1:]):
            if li.find_next_sibling() == proximo_li:
                if not sequencias_li or li not in sequencias_li[-1]:
                    sequencias_li.append([li])
                sequencias_li[-1].append(proximo_li)
            else:
                if len(sequencias_li[-1]) > 1:
                    ul = soup.new_tag('ul')
                    for item in sequencias_li[-1]:
                        item.wrap(ul)
                sequencias_li.pop()

        tags_ul = soup.find_all('ul')
        for ul in tags_ul:
            ul['class'] = 'fs-5','list-group' 

        cor_base_1 = "#61a88"

        ul_tags = soup.find_all('ul')
        for ul_tag in ul_tags:
            new_tag = soup.new_tag('div', attrs={'class':'row'})
            new_colun_4 = soup.new_tag('div', attrs={'class':'col-sm-2 float-end mw-100 mh-100 min-vh-10 border border-3 border-white','style': 'background-color: #f9b14b; border-radius: 10px;'})
            new_colun_8 = soup.new_tag('div', attrs={'class':'col-sm-10 border border-3 border-white' ,'style': 'background-color: #f9b14b; border-radius: 10px;'})
            ul_tag.wrap(new_colun_8)
            new_colun_8.wrap(new_tag)
            new_colun_8.insert_after(new_colun_4)

        aula_tag = soup.find(class_='AULA')
        mso_title_tag = soup.find(class_='MsoTitle')
        content_combined = ""
        if aula_tag:
            content_combined += aula_tag.get_text() 
            content_combined += " - "
        if mso_title_tag:
            content_combined += mso_title_tag.get_text()
            content_combined = content_combined[1:].capitalize()
            

        links_youtube = soup.find_all(class_='PROtextoquadro')
        for a_link in links_youtube:
            video_link = a_link.find_all('a', href=lambda href: href and 'www.youtube.com' in href)#encontar link do youtube que estiver dentro de um quadro
            for link in video_link:
                video_id = link['href'].split('v=')[1]
                embed_tag = soup.new_tag('embed')
                embed_tag['src'] = f'https://www.youtube.com/embed/{video_id}'
                embed_tag['autoplay'] = 'true'
                embed_tag['controls'] = 'false'
                link.replace_with(embed_tag)

        # Cria uma nova tag <a> com a classe "btn" e "btn-primary"


        navbar = soup.new_tag("nav", **{'class': "navbar fixed-top navbar-expand-lg navbar-light bg-light"})
        divbar = soup.new_tag("div", **{'class': "container-fluid"})
        menu_bt = soup.new_tag("a", **{'class': "btn btn-primary",'data-bs-toggle': "offcanvas", 'href': "#offcanvasExample", 'role': "button",'aria-controls':"offcanvasExample"})
        menu_bt.string = "Sumário"
        #exit_bt = soup.new_tag("button", **{'class': "btn btn-success", 'id': "completar-aula-btn", 'style': "display:none;",'aria-label':"Completar Aula"})
        #exit_bt.string = "Completar Aula"
        # Cria a div principal com a classe "message-container"
        # Cria a div principal com o ícone de check
        # Cria a tag <div> para o círculo animado com o ícone de marca de verificação
        circle_container_div = soup.new_tag("div", attrs={"class": "circle-container","id": "concluiu_aula", "style": "display: none; width: 24px; height: 24px; border: 2px solid #4caf50; border-radius: 50%; position: relative; overflow: show; opacity: 0; animation: inAnima 5s cubic-bezier(0,1,0,1) 1s forwards "})

        # Cria o primeiro SVG do ícone de marca de verificação com borda branca
        check_icon_svg_white = soup.new_tag("svg", attrs={"class": "check-icon", "xmlns": "http://www.w3.org/2000/svg", "width": "40", "height": "40", "viewBox": "0 0 24 24", "fill": "#ffffff", "stroke": "#ffffff", "stroke-width": "3", "stroke-linecap": "round", "stroke-linejoin": "round", "style": "position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 1; z-index: 1;"})
        check_icon_svg_white.append(soup.new_tag("path", attrs={"d": "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"}))
        circle_container_div.append(check_icon_svg_white)

        # Cria o segundo SVG do ícone de marca de verificação com a cor verde
        check_icon_svg_green = soup.new_tag("svg", attrs={"class": "check-icon", "xmlns": "http://www.w3.org/2000/svg", "width": "40", "height": "40", "viewBox": "0 0 24 24", "fill": "#4caf50", "stroke": "#4caf50", "stroke-width": "1", "stroke-linecap": "round", "stroke-linejoin": "round", "style": "position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 1; z-index: 1;"})
        check_icon_svg_green.append(soup.new_tag("path", attrs={"d": "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"}))
        circle_container_div.append(check_icon_svg_green)

        circle_message_div = soup.new_tag("div", attrs={"class": "congratulations-text","id": "message_congratulation", "style": "width: 210px; float: right; color: #4caf50 ;  right: -100%; opacity: 0; font-size: 14px; font-weight: bold; animation: fadeInFromLeft 1s 3s forwards;"})
        circle_message_div.append("Parabéns! Aula concluída")
        circle_container_div.append(circle_message_div)


        div_bar_progress = soup.new_tag("div", **{'class': "fixed-top", 'style': "top: 50px;"})
        progressbar = soup.new_tag("div", **{'class': "progress", 'style': "z-index:1050; height: 5px;"})
        progressbarcolor = soup.new_tag("div", **{'class': "progress-bar bg-success", 'id': "scroll-progress", 'role': "progressbar", 'style': "width: 0%", 'aria-valuenow': "0", 'aria-valuemin': "0", 'aria-valuemax': "100"})
        
        progressbar.append(progressbarcolor)
        div_bar_progress.append(progressbar)

        divbar.append(menu_bt)
        divbar.append(circle_container_div)

        navbar.append(divbar)
        

        # Cria a tag <div> com os atributos fornecidos
        offcanvas_div = soup.new_tag("div", **{"class": "offcanvas offcanvas-start", "tabindex": "-1", "id": "offcanvasExample", "aria-labelledby": "offcanvasExampleLabel"})
 
        # Cria a tag <div class="offcanvas-header">
        offcanvas_header_div = soup.new_tag("div", **{"class": "offcanvas-header"})
        # Cria a tag <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
        offcanvas_title_h5 = soup.new_tag("h5", **{"class": "offcanvas-title", "id": "offcanvasExampleLabel"})
        offcanvas_title_h5.string = "Sumário"
        # Cria a tag <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        button = soup.new_tag("button", **{"type": "button", "class": "btn-close text-reset", "data-bs-dismiss": "offcanvas", "aria-label": "Close"})

        # Adiciona as tags filhas:
        offcanvas_header_div.append(offcanvas_title_h5)
        offcanvas_header_div.append(button)

        offcanvas_body_div = soup.new_tag("div", **{"class": "offcanvas-body"})
        
        text_div = soup.new_tag("div")
        text_div.string = "Navegue pelo conteúdo utilizando este menu."
        
        dropdown_div = soup.new_tag("div", **{"class": "list-group mw-40 mt-3", "id": "#menulist"})
    
        titulo_lista = soup.find_all(class_="ttl1")
        titulos = []

        for i in range(len(titulo_lista)):
            titulo1 = titulo_lista[i]
            titulo1['id'] = 't' + str(i)
            titulos.append(titulo1.get_text())

            a_tag1 = soup.new_tag("a", href="#t" + str(i), **{"class": "list-group-item list-group-item-action"})

            if "nvl0" in titulo1["class"]:
                a_tag1["class"].append("nvl0 ps-2")
            elif "nvl1" in titulo1["class"]:
                a_tag1["class"].append("nvl1 ps-3")
            elif "nvl2" in titulo1["class"]:
                a_tag1["class"].append("nvl2 ps-4")
            elif "nvl3" in titulo1["class"]:
                a_tag1["class"].append("nvl3 ps-5")

            a_tag1.string = titulo1.get_text()
            dropdown_div.append(a_tag1)

        # Adiciona as tags filhas:
        offcanvas_body_div.append(text_div)
        offcanvas_body_div.append(dropdown_div)

        # Adiciona as tags filhas ao offcanvas_div:
        offcanvas_div.append(offcanvas_header_div)
        offcanvas_div.append(offcanvas_body_div)
  
        target_elements = soup.find_all(class_="MsoTitle")
     
        if target_elements:
            prefix_class = target_elements[0].find_previous(class_=lambda class_: class_ and class_.startswith("WordSection"))
            
            next_word_section = target_elements[0].find_next(class_=lambda class_: class_ and class_.startswith("WordSection"))

  
        target_elements = soup.find_all(class_="MsoNormal")
        for element in target_elements:
            if element.get_text(strip=True) == "" or element.get_text(strip=True) == "&nbsp;":
                element.extract()

        section_class = navbar, div_bar_progress ,offcanvas_div ,prefix_class, next_word_section

        soup = section_class  
        soup =  " ".join(str(x) for x in soup) 

              
        # Renderiza o template em uma string
        html_content = render_to_string('conteudo.html', {'conteudo': soup})
        nome_arquivo = content_combined + ".html"
        caminho_arquivo = os.path.join(settings.MEDIA_ROOT, nome_arquivo)
        with open(caminho_arquivo, 'w') as file:
            file.write(html_content)
 
    
        return soup
    

