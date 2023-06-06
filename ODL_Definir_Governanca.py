#Importa bibliotecas
import requests
import pandas as pd
import PySimpleGUI as gui
import os
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as et


#Escreve os dados relativos aos parâmetros do decisor no formato xml
def gerar_xml_governanca():

    if valores['sla_razoavel_3']:
        info_sla_razoavel = '3 horas'
    elif valores['sla_razoavel_6']:
        info_sla_razoavel = '6 horas'
    elif valores['sla_razoavel_12']:
        info_sla_razoavel = '12 horas'
    elif valores['sla_razoavel_24']:
        info_sla_razoavel = '24 horas'
    else:
        info_sla_razoavel = '48 horas'

    if valores['sla_maximo_3']:
        info_sla_maximo = '3 horas'
    elif valores['sla_maximo_6']:
        info_sla_maximo = '6 horas'
    elif valores['sla_maximo_12']:
        info_sla_maximo = '12 horas'
    elif valores['sla_maximo_24']:
        info_sla_maximo = '24 horas'
    else:
        info_sla_maximo = '48 horas'

    pre_xml = pd.DataFrame.from_dict(
        {'Enlace': [def_servico[0]],
         'Enlace_Descrição': [def_servico[1]],
         'Governanca_SLA_Desejavel': [info_sla_razoavel],
         'Governanca_SLA_Limitrofe': [info_sla_maximo],
         'Governanca_Custo_Desejavel': [valores['custo_desejavel']],
         'Governanca_Custo_Limitrofe': [valores['custo_maximo']]})

    nome_arquivo = 'ODL_Parametros_Governanca_' + def_servico[0].replace(' ','').upper() + '.xml'
    pd.DataFrame.to_xml(pre_xml, nome_arquivo, encoding='UTF-8', index=True)



#Lê o xml que contém os dados do serviço
def ler_xml_servico():
    #xml_tree = et.parse('ODL_Parametros_Enlace.xml')
    xml_tree = et.parse(nome_arquivo_enlace)
    xml_root = xml_tree.getroot()
    dados_servico = list()
    for xml_row in xml_tree.findall('row'):
        dados_servico.append(xml_row.find('Enlace').text)
        dados_servico.append(xml_row.find('Enlace_Descrição').text)
        dados_servico.append(xml_row.find('Roteador1').text)
        dados_servico.append(xml_row.find('Roteador1_Localização').text)
        dados_servico.append(xml_row.find('Roteador1_Descrição').text)
        dados_servico.append(xml_row.find('Roteador2').text)
        dados_servico.append(xml_row.find('Roteador2_Localização').text)
        dados_servico.append(xml_row.find('Roteador2_Descrição').text)
        dados_servico.append(xml_row.find('QtdEstimadaTerminais').text)
        dados_servico.append(xml_row.find('Protocolo').text)
        dados_servico.append(xml_row.find('Meio').text)
        dados_servico.append(xml_row.find('Demanda').text)
    return dados_servico

def validar_entrada():
    valido = True
    if (not valores['sla_razoavel_3'] and not valores['sla_razoavel_6'] and not valores['sla_razoavel_12'] and not valores['sla_razoavel_24'] and not valores['sla_razoavel_48']):
        valido = False
    if (not valores['sla_maximo_3'] and not valores['sla_maximo_6'] and not valores['sla_maximo_12'] and not valores['sla_maximo_24'] and not valores['sla_maximo_48']):
        valido = False
    if (valores['custo_desejavel'] == "") or (valores['custo_maximo'] == ""):
        valido = False

    if not valido:
        messagebox.showinfo('Atenção', 'Favor preencher todos os campos!')
        return False

    return True

#Janela para escolher o arquivo xml do enlace a ser trabalhado
nome_arquivo_enlace = filedialog.askopenfilename(title='Escolha um arquivo XML contendo a definição de um ENLACE',filetypes =[('Enlaces', '*Enlace*.xml')])
if nome_arquivo_enlace == "":
    exit(0)

#Define composição da tela
gui.change_look_and_feel('DefaultNoMoreNagging')
def_servico = ler_xml_servico()
coluna = [
    [gui.Text('FASE 1 - ENTRADA DE DADOS - PROCESSO "DEFINIR PARÂMETROS DO NÍVEL DE GOVERNANÇA"', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('Foram informados os seguintes DADOS GERAIS do enlace:', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('ID do EnlaceServiço',size=(15,0)), gui.Text(def_servico[0],size=(150, 0))],
    [gui.Text('Descrição',size=(15,0)), gui.Text(def_servico[1],size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('Roteador 1',size=(15,0)), gui.Text(def_servico[2],size=(150,0))],
    [gui.Text('Localização',size=(15,0)), gui.Text(def_servico[3],size=(150,0))],
    [gui.Text('Descrição',size=(15,0)), gui.Text(def_servico[4],size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('Roteador 2',size=(15,0)), gui.Text(def_servico[5],size=(150,0))],
    [gui.Text('Localização',size=(15,0)), gui.Text(def_servico[6],size=(150,0))],
    [gui.Text('Descrição',size=(15,0)), gui.Text(def_servico[7],size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('Quantidade Estimada de Terminais',size=(15,0)), gui.Text(def_servico[8],size=(150,0))],
    [gui.Text('Protocolo',size=(15,0)), gui.Text(def_servico[9],size=(150,0))],
    [gui.Text('Meio de Propagação',size=(15,0)), gui.Text(def_servico[10],size=(150,0))],
    [gui.Text('Demanda',size=(15,0)), gui.Text(def_servico[11],size=(150,0))],
    [gui.Text(' ')],
    [gui.Text('Considerando o valor ESTRATÉGICO desse enlace, defina os valores ACEITÁVEIS e LIMÍTROFES para os seguintes parâmetros:',font='Bold')],
    [gui.Text(' ')],
    [gui.Text('(1) SLA Razoável', size=(15,0)),
     gui.Radio('Até 03 horas','sla_razoavel',key='sla_razoavel_3'),
     gui.Radio('Até 06 horas','sla_razoavel',key='sla_razoavel_6'),
     gui.Radio('Até 12 horas','sla_razoavel',key='sla_razoavel_12'),
     gui.Radio('Até 24 horas','sla_razoavel',key='sla_razoavel_24'),
     gui.Radio('Até 48 horas','sla_razoavel',key='sla_razoavel_48')],
    [gui.Text('(2) SLA Máximo', size=(15, 0)),
     gui.Radio('Até 03 horas', 'sla_maximo', key='sla_maximo_3'),
     gui.Radio('Até 06 horas', 'sla_maximo', key='sla_maximo_6'),
     gui.Radio('Até 12 horas', 'sla_maximo', key='sla_maximo_12'),
     gui.Radio('Até 24 horas', 'sla_maximo', key='sla_maximo_24'),
     gui.Radio('Até 48 horas', 'sla_maximo', key='sla_maximo_48')],
    [gui.Text('(3) Custo Desejável (R$/Mbps)', size=(25,0)), gui.InputText(key='custo_desejavel', size=(10,0))],
    [gui.Text('(4) Custo Máximo (R$/Mbps)', size=(25,0)), gui.InputText(key='custo_maximo', size=(10,0))],
    [gui.Text(' ')],
    [gui.Button('Salvar'),gui.Button('Cancelar'),gui.Button('Ajuda')],
    [gui.Text(' ')]]

layout = [[gui.Column(coluna,scrollable='True', vertical_scroll_only='True', size=(1400,600)) ]]

#Exibe tela
janela = gui.Window('Projeto OntoDataLink',layout, resizable=True, size=(1400,600) )


#Trata eventos
while True:
    evento, valores = janela.read()
    if (evento == gui.WIN_CLOSED or evento == 'Cancelar'):
        break
    if (evento == 'Ajuda'):
        messagebox.showinfo('Orientações para a definição dos parâmetros', \
                            '(1) SLA Razoável - Informe o prazo razoável para aceitar a inoperância dos serviços em caso de falha no enlace. Defina o parâmetro de acordo com o valor estratégico do enlace para a instituição. (Polaridade: valor menor é melhor).\n\n' +\
                            '(2) SLA Máximo - Informe o “limite máximo” de tempo para aceitar a inoperância dos serviços. Acima desse valor, entende-se que o não restabelecimento dos serviços nesse prazo poderá comprometer instituição. (Polaridade: valor menor é melhor).\n\n' +\
                            '(3) Custo Desejável - Informe o valor financeiro confortável para custear a contratação do enlace (informe um valor inteiro). Defina o valor de acordo com o orçamento autorizado para o projeto. (Polaridade – valor menor é melhor).\n\n' +\
                            '(4) Custo Máximo - Informe o “limite máximo” viável para custear a contração do enlace. Acima desse valor, entende-se que não haverá recursos orçamentários suficientes para o custeio. Defina o valor de acordo com o orçamento autorizado para o projeto. (Polaridade – valor menor é melhor).')
    if (evento == 'Salvar'):
        if validar_entrada():
            gerar_xml_governanca()
            break

#Encerramento
janela.close()