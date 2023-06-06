
#Importa bibliotecas
import requests
import pandas as pd
import PySimpleGUI as gui
from tkinter import messagebox
import xml.etree.ElementTree as et


#Escreve os dados relativos ao desenho do serviço no formato xml
def gerar_xml_servico():
    if valores['meio_optico']:
        info_meio = 'Óptico'
    elif valores['meio_ondas']:
        info_meio = 'Ondas'
    else:
        info_meio = 'Elétrico'

    if valores['demanda_alta']:
        info_demanda = 'Alta'
    else:
        info_demanda ='Normal'

    pre_xml = pd.DataFrame.from_dict(
        {'Enlace': [valores['enlace_id']],
         'Enlace_Descrição': [valores['enlace_descrição']],
         'Roteador1': [valores['roteador1_id']],
         'Roteador1_Localização': [valores['roteador1_localização']],
         'Roteador1_Descrição': [valores['roteador1_descrição']],
         'Roteador2': [valores['roteador2_id']],
         'Roteador2_Localização': [valores['roteador2_localização']],
         'Roteador2_Descrição': [valores['roteador2_descrição']],
         'QtdEstimadaTerminais':[valores['qtd_estimada_terminais']],
         'Protocolo': [valores['protocolo']],
         'Meio': info_meio,
         'Demanda':info_demanda,})


    nome_arquivo = 'ODL_Parametros_Enlace_' + valores['enlace_id'].replace(' ','').upper() + '.xml'
    pd.DataFrame.to_xml(pre_xml, nome_arquivo, encoding='UTF-8', index=True)

def validar_entrada():
    valido = True
    if (valores['enlace_id'] == "") or (valores['enlace_descrição'] == "") or (valores['roteador1_id'] == "") or (valores['roteador1_localização'] == "") or (valores['roteador1_descrição'] == "") or (valores['roteador2_id'] == ""):
        valido = False
    if (valores['roteador2_localização'] == "") or (valores['roteador2_descrição'] == "") or (valores['qtd_estimada_terminais'] == "") or (valores['protocolo'] == "") or (not valores['meio_optico'] and not valores['meio_ondas'] and not valores['meio_eletrico']):
        valido = False
    if (not valores['demanda_alta'] and not valores['demanda_normal']):
        valido = False

    if not valido:
        messagebox.showinfo('Atenção', 'Favor preencher todos os campos!')
        return False

    if (valores['enlace_id'] == valores['roteador1_id']) or (valores['enlace_id'] == valores['roteador2_id']) or (valores['roteador1_id'] == valores['roteador2_id']):
        messagebox.showinfo('Atenção', 'Os ID (Enlace, Roteador 1 e Roteador 2) não podem ser iguais!')
        return False

    return True

#Define composição da tela
#gui.change_look_and_feel('GreenMono')
gui.change_look_and_feel('DefaultNoMoreNagging')
coluna = [
    [gui.Text('FASE 1 - ENTRADA DE DADOS - PROCESSO "DESENHAR ENLACE"', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('Informe os DADOS GERAIS do enlace:', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('ID do enlace', size=(15,0)), gui.InputText(key='enlace_id', size=(15,0))],
    [gui.Text('Descrição', size=(15,0)), gui.InputText(key='enlace_descrição', size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('ID do Roteador 1', size=(15,0)), gui.InputText(key='roteador1_id', size=(15,0))],
    [gui.Text('Localização', size=(15,0)), gui.InputText(key='roteador1_localização', size=(40,0))],
    [gui.Text('Descrição', size=(15,0)), gui.InputText(key='roteador1_descrição', size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('ID do Roteador 2', size=(15,0)), gui.InputText(key='roteador2_id', size=(15,0))],
    [gui.Text('Localização', size=(15,0)), gui.InputText(key='roteador2_localização', size=(40,0))],
    [gui.Text('Descrição', size=(15,0)), gui.InputText(key='roteador2_descrição', size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('Qtd. Estimada de Terminais', size=(15,0)), gui.InputText(key='qtd_estimada_terminais', size=(10,0))],
    [gui.Text('Protocolo', size=(15,0)), gui.InputText(key='protocolo', size=(10,0))],
    [gui.Text('Meio de Propagação', size=(15,0)),
     gui.Radio('Óptico','meio',key='meio_optico'),
     gui.Radio('Ondas','meio',key='meio_ondas'),
     gui.Radio('Elétrico','meio',key='meio_eletrico')],
    [gui.Text('Perfil Estimado da Demanda', size=(15, 0)),
     gui.Radio('Alta', 'demanda', key='demanda_alta'),
     gui.Radio('Normal', 'demanda', key='demanda_normal')],
    [gui.Text(' ')],
    [gui.Button('Salvar'),gui.Button('Cancelar')],
    [gui.Text(' ')]]


layout = [[gui.Column(coluna,scrollable='True', vertical_scroll_only='True', size=(1400,650)) ]]


#Exibe tela
janela = gui.Window('Projeto OntoDataLink',layout, resizable=True, size=(1400,650) )

#Trata eventos
while True:
    evento, valores = janela.read()
    if (evento == gui.WIN_CLOSED or evento == 'Cancelar'):
        break
    if (evento == 'Salvar'):
        if validar_entrada():
            gerar_xml_servico()
            break

#Encerramento
janela.close()