# Importa bibliotecas
import requests
import pandas as pd
import PySimpleGUI as gui
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as et


# Escreve os dados de OPERAÇÃO no formato xml
def gerar_xml_operacao():
    if valores['banda_desejavel_100mbps']:
        info_banda_desejavel = '100 Mbps'
    elif valores['banda_desejavel_250mbps']:
        info_banda_desejavel = '250 Mbps'
    elif valores['banda_desejavel_500mbps']:
        info_banda_desejavel = '500 Mbps'
    elif valores['banda_desejavel_1gbps']:
        info_banda_desejavel = '1 Gbps'
    else:
        info_banda_desejavel = '10 Gbps'

    if valores['banda_minima_100mbps']:
        info_banda_minima = '100 Mbps'
    elif valores['banda_minima_250mbps']:
        info_banda_minima = '250 Mbps'
    elif valores['banda_minima_500mbps']:
        info_banda_minima = '500 Mbps'
    elif valores['banda_minima_1gbps']:
        info_banda_minima = '1 Gbps'
    else:
        info_banda_minima = '10 Gbps'

    if valores['sla_desejavel_3']:
        info_sla_desejavel = '3 horas'
    elif valores['sla_desejavel_6']:
        info_sla_desejavel = '6 horas'
    elif valores['sla_desejavel_12']:
        info_sla_desejavel = '12 horas'
    elif valores['sla_desejavel_24']:
        info_sla_desejavel = '24 horas'
    else:
        info_sla_desejavel = '48 horas'

    if valores['sla_minimo_3']:
        info_sla_minimo = '3 horas'
    elif valores['sla_minimo_6']:
        info_sla_minimo = '6 horas'
    elif valores['sla_minimo_12']:
        info_sla_minimo = '12 horas'
    elif valores['sla_minimo_24']:
        info_sla_minimo = '24 horas'
    else:
        info_sla_minimo = '48 horas'

    pre_xml = pd.DataFrame.from_dict(
        {'Enlace': [def_servico[0]],
         'Enlace_Descrição': [def_servico[1]],
         'Operacao_Banda_Desejavel': info_banda_desejavel,
         'Operacao_Banda_Limitrofe': info_banda_minima,
         'Operacao_SLA_Desejavel': info_sla_desejavel,
         'Operacao_SLA_Limitrofe': info_sla_minimo})

    nome_arquivo = 'ODL_Parametros_Operacao_' + def_servico[0].replace(' ', '').upper() + '.xml'
    pd.DataFrame.to_xml(pre_xml, nome_arquivo, encoding='UTF-8', index=True)


# Lê o xml que contém os dados do serviço
def ler_xml_servico():
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
    if (not valores['banda_desejavel_100mbps'] and not valores['banda_desejavel_250mbps'] and not valores['banda_desejavel_500mbps'] and not valores['banda_desejavel_1gbps'] and not valores ['banda_desejavel_10gbps']):
        valido = False
    if (not valores['banda_minima_100mbps'] and not valores['banda_minima_250mbps'] and not valores['banda_minima_500mbps'] and not valores['banda_minima_1gbps'] and not valores['banda_minima_10gbps']):
        valido = False
    if (not valores['sla_desejavel_3'] and not valores['sla_desejavel_6'] and not valores['sla_desejavel_12'] and not valores['sla_desejavel_24'] and not valores['sla_desejavel_48']):
        valido = False
    if (not valores['sla_minimo_3'] and not valores['sla_minimo_6'] and not valores['sla_minimo_12'] and not valores['sla_minimo_24'] and not valores['sla_minimo_48']):
        valido = False

    if not valido:
        messagebox.showinfo('Atenção', 'Favor preencher todos os campos!')
        return False

    return True


#Janela para escolher o arquivo xml do enlace a ser trabalhado
nome_arquivo_enlace = filedialog.askopenfilename(title='Escolha um arquivo XML contendo a definição de um ENLACE', filetypes=[('Enlaces', '*Enlace*.xml')])
if nome_arquivo_enlace == "":
    exit(0)

# Define composição da tela
gui.change_look_and_feel('DefaultNoMoreNagging')
def_servico = ler_xml_servico()
coluna = [
    [gui.Text('FASE 1 - ENTRADA DE DADOS - PROCESSO "DEFINIR PARÂMETROS DO NÍVEL DE OPERAÇÃO"', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('Foram informados os seguintes DADOS GERAIS do enlace:', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('ID do EnlaceServiço', size=(15, 0)), gui.Text(def_servico[0], size=(150, 0))],
    [gui.Text('Descrição', size=(15, 0)), gui.Text(def_servico[1], size=(150, 0))],
    [gui.Text(' ')],
    [gui.Text('Roteador 1', size=(15, 0)), gui.Text(def_servico[2], size=(150, 0))],
    [gui.Text('Localização', size=(15, 0)), gui.Text(def_servico[3], size=(150, 0))],
    [gui.Text('Descrição', size=(15, 0)), gui.Text(def_servico[4], size=(150, 0))],
    [gui.Text(' ')],
    [gui.Text('Roteador 2', size=(15, 0)), gui.Text(def_servico[5], size=(150, 0))],
    [gui.Text('Localização', size=(15, 0)), gui.Text(def_servico[6], size=(150, 0))],
    [gui.Text('Descrição', size=(15, 0)), gui.Text(def_servico[7], size=(150, 0))],
    [gui.Text(' ')],
    [gui.Text('Quantidade Estimada de Terminais', size=(15, 0)), gui.Text(def_servico[8], size=(150, 0))],
    [gui.Text('Protocolo', size=(15, 0)), gui.Text(def_servico[9], size=(150, 0))],
    [gui.Text('Meio de Propagação', size=(15, 0)), gui.Text(def_servico[10], size=(150, 0))],
    [gui.Text('Demanda', size=(15, 0)), gui.Text(def_servico[11], size=(150, 0))],
    [gui.Text(' ')],
    [gui.Text('Considerando a OPERACIONALIDADE do enlace, informe os valores DESEJÁVEIS e LIMÍTROFES para os seguintes parâmetros:', font='Bold')],
    [gui.Text(' ')],
    [gui.Text('(1) Banda mínima', size=(15, 0)),
     gui.Radio('100 Mbps', 'banda_minima', key='banda_minima_100mbps'),
     gui.Radio('250 Mbps', 'banda_minima', key='banda_minima_250mbps'),
     gui.Radio('500 Mbps', 'banda_minima', key='banda_minima_500mbps'),
     gui.Radio('1 Gbps', 'banda_minima', key='banda_minima_1gbps'),
     gui.Radio('10 Gbps', 'banda_minima', key='banda_minima_10gbps')],
    [gui.Text('(2) Banda desejável', size=(15, 0)),
     gui.Radio('100 Mbps', 'banda_desejavel', key='banda_desejavel_100mbps'),
     gui.Radio('250 Mbps', 'banda_desejavel', key='banda_desejavel_250mbps'),
     gui.Radio('500 Mbps', 'banda_desejavel', key='banda_desejavel_500mbps'),
     gui.Radio('1 Gbps', 'banda_desejavel', key='banda_desejavel_1gbps'),
     gui.Radio('10 Gbps', 'banda_desejavel', key='banda_desejavel_10gbps')],
    [gui.Text('(3) SLA Mínimo', size=(15, 0)),
     gui.Radio('Até 03 horas', 'sla_minimo', key='sla_minimo_3'),
     gui.Radio('Até 06 horas', 'sla_minimo', key='sla_minimo_6'),
     gui.Radio('Até 12 horas', 'sla_minimo', key='sla_minimo_12'),
     gui.Radio('Até 24 horas', 'sla_minimo', key='sla_minimo_24'),
     gui.Radio('Até 48 horas', 'sla_minimo', key='sla_minimo_48')],
    [gui.Text('(4) SLA Desejável', size=(15,0)),
     gui.Radio('Até 03 horas','sla_desejavel',key='sla_desejavel_3'),
     gui.Radio('Até 06 horas','sla_desejavel',key='sla_desejavel_6'),
     gui.Radio('Até 12 horas','sla_desejavel',key='sla_desejavel_12'),
     gui.Radio('Até 24 horas','sla_desejavel',key='sla_desejavel_24'),
     gui.Radio('Até 48 horas','sla_desejavel',key='sla_desejavel_48')],
    [gui.Text(' ')],
    [gui.Button('Salvar'),gui.Button('Cancelar'),gui.Button('Ajuda')],
    [gui.Text(' ')]]


layout = [[gui.Column(coluna,scrollable='True', vertical_scroll_only='True', size=(1400,600)) ]]


#Exibe tela
janela = gui.Window('Projeto OntoDataLink',layout, resizable=True, size=(1400,600) )

# Trata eventos
while True:
    evento, valores = janela.read()
    if (evento == gui.WIN_CLOSED or evento == 'Cancelar'):
        break
    if (evento == 'Ajuda'):
        messagebox.showinfo(title='Orientações para a definição dos parâmetros', \
                            message='(1) Banda Mínima - Informe o “limite mínimo” de largura de banda para operar o enlace sem comprometer a operacionalidade. Abaixo desse valor, entende-se que a atividade é inviável. Defina o valor de acordo com a perspectiva da operacionalidade do enlace. (Polaridade – valor maior é melhor).\n\n' + \
                            '(2) Banda Desejável - Informe o valor confortável de largura de banda para operar o enlace. Defina o valor de acordo com a perspectiva da operacionalidade do enlace. (Polaridade – valor maior é melhor).\n\n' + \
                            '(3) SLA Mínimo - O “limite mínimo” de tempo para restabelecer a conectividade em caso de falha no enlace. Abaixo desse valor, entende-se que não haverá condição de reativar o enlace no prazo. Defina o valor de acordo com a perspectiva da operacionalidade do enlace. (Polaridade – valor maior é melhor).\n\n' + \
                            '(4) SLA Desejável - Informe o prazo razoável para restabelecer a conectividade em caso de falha no enlace. Defina o valor de acordo com a perspectiva da operacionalidade do enlace. (Polaridade – valor maior é melhor).')
    if (evento == 'Salvar'):
        if validar_entrada():
            gerar_xml_operacao()
            break

# Encerramento
janela.close()
