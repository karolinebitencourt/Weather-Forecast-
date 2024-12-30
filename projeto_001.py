import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import requests
from datetime import datetime
import json
import pytz
import pycountry_convert as pc

from deep_translator import GoogleTranslator

tradutor = GoogleTranslator('en', 'pt')

# Para facilitar as cores
co0 = "#444466"  # preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul
co3 = "#C8A2C8"  # lilas

fundo_dia = "#6cc4cc"
fundo_tarde = "#bfb86d"
fundo_noite = "#484f60"

fundo = co3

janela = Tk()
janela.title('CLIMA ONDE VOCÊ QUISER')
janela.geometry('320x350')
janela.configure(bg=fundo)
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

# criando frames
frame_top = Frame(janela, width=350, height=50, bg=co3, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=350, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use('clam')


def converter_para_celsius(temp):
    celsius=temp - 273
    print(celsius)
    return int(celsius)


global imagem

def informacao():
    chave = 'da3ef0503d5e3a8c236babc6dd43a63d'
    cidade = e_local.get()
    api_link = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(cidade, chave)
    r = requests.get(api_link)

    dados = r.json()

    pais_codigo = dados['sys']['country']

    zona_fuso = pytz.country_timezones[pais_codigo]

    pais = pytz.country_names[pais_codigo]

    zona = pytz.timezone(zona_fuso[0])

    zona_horas = datetime.now(zona)
    # horas
    zona_horas = zona_horas.strftime("Data: %d/%m/%Y || Horas: %H:%M:%S %p")

    tempo = dados['main']['temp']
    pressao = dados['main']['pressure']
    humidade = dados['main']['humidity']
    vento = dados['wind']['speed']
    descricao = tradutor.translate(dados['weather'][0]['description'])
    temperatura_atual= str(converter_para_celsius(dados['main']['temp']))
    temperatura_min= str(converter_para_celsius(dados['main']['temp_min']))
    temperatura_max= str(converter_para_celsius(dados['main']['temp_max']))
    sensacao_termica=converter_para_celsius(dados['main']['feels_like'])


    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continente_codigo)
        return pais_continente_nome

    continente = pais_para_continente(pais)

    # retornando informações nas labels
    l_cidade['text'] = cidade.title() + " - " + tradutor.translate(pais) + " / " +tradutor.translate(continente)
    l_data['text'] = zona_horas
    l_humidade['text'] = humidade
    l_pressao['text'] = 'Pressão: ' + str(pressao) + ' Pa'
    l_velocidade['text'] = 'Vento: ' + str(vento) + ' km/h'
    l_descricao['text'] = 'Céu: ' + descricao.title()
    l_h_simbol['text'] = '%'
    l_h_nome['text'] = 'Humidade'
    l_temperatura_atual['text']=temperatura_atual
    l_temperatura['text']='Temp. Mín: '+ temperatura_min + '°C' + '   Temp. Máx: '+ temperatura_max + '°C'
    l_t_atual_nome['text']= 'Temp. Atual'
    l_t_atual_simbol['text']= '°C'
    l_temperatura_sensacao_atual['text']=sensacao_termica
    l_t_sensacao_nome['text']= 'Sensação Térmica'
    l_t_sensacao_simbol['text']= '°C'


    # Lógica para trocar o fundo

    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")

    global imagem

    zona_periodo = int(zona_periodo)

    if 0 <= zona_periodo <= 5:
        imagem = Image.open('/Users/karolinebitencourt/image/lua.png')
        l_hora['text']='Noite'
        fundo = fundo_noite

    elif 5 < zona_periodo <= 11:
        imagem = Image.open('/Users/karolinebitencourt/image/sol_dia.png')
        l_hora['text']='Manhã'
        fundo = fundo_dia

    elif 11 < zona_periodo <= 17:
        imagem = Image.open('/Users/karolinebitencourt/image/sol_tarde.png')
        l_hora['text']='Tarde'
        fundo = fundo_tarde

    elif 17 < zona_periodo <= 24:
        imagem = Image.open('/Users/karolinebitencourt/image/lua.png')
        l_hora['text']='Noite'
        fundo = fundo_noite

    else:
        pass

    imagem = imagem.resize((60, 60))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_corpo, image=imagem, bg=fundo)
    l_icon.place(x=240, y=45)

    janela.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)


    l_cidade['bg'] = fundo
    l_hora['bg'] = fundo
    l_data['bg'] = fundo
    l_humidade['bg'] = fundo
    l_pressao['bg'] = fundo
    l_velocidade['bg'] = fundo
    l_descricao['bg'] = fundo
    l_h_simbol['bg'] = fundo
    l_h_nome['bg'] = fundo
    l_temperatura_atual['bg']=fundo
    l_temperatura['bg']=fundo
    l_t_atual_simbol['bg']=fundo
    l_t_atual_nome['bg']=fundo
    l_temperatura_sensacao_atual['bg'] = fundo
    l_t_sensacao_simbol['bg'] = fundo
    l_t_sensacao_nome['bg'] = fundo


e_local = Entry(frame_top, width=20, justify='left', font=('', 16), highlightthickness=1, relief='solid')
e_local.place(x=5, y=13)
b_ver = Button(frame_top, command=informacao, text='Ver Clima', bg=co1, fg=co0, font=('Ivy 14 bold'), relief='raised',
               overrelief=RIDGE)
b_ver.place(x=215, y=12)

l_cidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 14 bold'))
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12'))
l_data.place(x=8, y=44)

l_hora = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12 bold'))
l_hora.place(x=250, y=25)

l_temperatura=Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12 '))
l_temperatura.place(x=10, y=70)

l_temperatura_atual =Label(frame_corpo,text='', anchor='center',bg=fundo,fg=co1,font=('Arial 40'))
l_temperatura_atual.place(x=10, y=100)

l_t_atual_simbol = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_t_atual_simbol.place(x=75, y=110)

l_t_atual_nome = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_t_atual_nome.place(x=75, y=132)

l_temperatura_sensacao_atual =Label(frame_corpo,text='', anchor='center',bg=fundo,fg=co1,font=('Arial 40'))
l_temperatura_sensacao_atual.place(x=10, y=160)

l_t_sensacao_simbol = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_t_sensacao_simbol.place(x=75, y=170)

l_t_sensacao_nome = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_t_sensacao_nome.place(x=75, y=192)

l_humidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 40'))
l_humidade.place(x=160, y=100)

l_h_simbol = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_h_simbol.place(x=225, y=110)

l_h_nome = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 10 bold'))
l_h_nome.place(x=225, y=132)

l_pressao = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12 '))
l_pressao.place(x=10, y=250)

l_velocidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12 '))
l_velocidade.place(x=10, y=222)

l_descricao = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=co1, font=('Arial 12 '))
l_descricao.place(x=160, y=222)




janela.mainloop()
