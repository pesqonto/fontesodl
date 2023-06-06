#Importa bibliotecas
import requests
import pandas as pd
import PySimpleGUI as gui
import xml.etree.ElementTree as et
from tkinter import filedialog, messagebox



#Lê os arquivos xml retornando os dados do serviço, de governança e de gestão
def ler_xml(nome_arquivo_enlace):
    leitura = dict()
    xml_tree_enlace = et.parse(nome_arquivo_enlace)
    for xml_row_enlace in xml_tree_enlace.findall('row'):
        #Busca as instâncias
        leitura['Enlace'] = xml_row_enlace.find('Enlace').text
        leitura['Enlace_Descricao'] = xml_row_enlace.find('Enlace_Descrição').text
        leitura['Roteador1'] = xml_row_enlace.find('Roteador1').text
        leitura['Roteador1_Localizacao'] = xml_row_enlace.find('Roteador1_Localização').text
        leitura['Roteador1_Descricao'] = xml_row_enlace.find('Roteador1_Descrição').text
        leitura['Roteador2'] = xml_row_enlace.find('Roteador2').text
        leitura['Roteador2_Localizacao'] = xml_row_enlace.find('Roteador2_Localização').text
        leitura['Roteador2_Descricao'] = xml_row_enlace.find('Roteador2_Descrição').text
        leitura['QtdEstimadaTerminais'] = xml_row_enlace.find('QtdEstimadaTerminais').text
        leitura['Protocolo'] = xml_row_enlace.find('Protocolo').text
        leitura['Meio'] = xml_row_enlace.find('Meio').text
        leitura['Demanda'] = xml_row_enlace.find('Demanda').text

    xml_tree_governanca = et.parse(nome_arquivo_enlace.replace("Enlace","Governanca"))
    for xml_row_governanca in xml_tree_governanca.findall('row'):
        #Busca as instâncias
        leitura['Governanca_SLA_Desejavel'] = xml_row_governanca.find('Governanca_SLA_Desejavel').text
        leitura['Governanca_SLA_Limitrofe'] = xml_row_governanca.find('Governanca_SLA_Limitrofe').text
        leitura['Governanca_Custo_Desejavel'] = xml_row_governanca.find('Governanca_Custo_Desejavel').text
        leitura['Governanca_Custo_Limitrofe'] = xml_row_governanca.find('Governanca_Custo_Limitrofe').text

    xml_tree_gerenciamento = et.parse(nome_arquivo_enlace.replace("Enlace","Gerenciamento"))
    for xml_row_gerenciamento in xml_tree_gerenciamento.findall('row'):
        #Busca as instâncias
        leitura['Gerenciamento_Banda_Desejavel'] = xml_row_gerenciamento.find('Gerenciamento_Banda_Desejavel').text
        leitura['Gerenciamento_Banda_Limitrofe'] = xml_row_gerenciamento.find('Gerenciamento_Banda_Limitrofe').text
        leitura['Gerenciamento_SLA_Desejavel'] = xml_row_gerenciamento.find('Gerenciamento_SLA_Desejavel').text
        leitura['Gerenciamento_SLA_Limitrofe'] = xml_row_gerenciamento.find('Gerenciamento_SLA_Limitrofe').text
        leitura['Gerenciamento_Custo_Desejavel'] = xml_row_gerenciamento.find('Gerenciamento_Custo_Desejavel').text
        leitura['Gerenciamento_Custo_Limitrofe'] = xml_row_gerenciamento.find('Gerenciamento_Custo_Limitrofe').text

    xml_tree_operacao = et.parse(nome_arquivo_enlace.replace("Enlace", "Operacao"))
    for xml_row_operacao in xml_tree_operacao.findall('row'):
        # Busca as instâncias
        leitura['Operacao_Banda_Desejavel'] = xml_row_operacao.find('Operacao_Banda_Desejavel').text
        leitura['Operacao_Banda_Limitrofe'] = xml_row_operacao.find('Operacao_Banda_Limitrofe').text
        leitura['Operacao_SLA_Desejavel'] = xml_row_operacao.find('Operacao_SLA_Desejavel').text
        leitura['Operacao_SLA_Limitrofe'] = xml_row_operacao.find('Operacao_SLA_Limitrofe').text

    lista_alertas.append('Enlace ' + leitura['Enlace'] + ' --> Leitura dos parâmetros realizada.')
    return leitura


#Recebe um dicionário com os parâmetros e respectivos valores
#Retorna uma lista com os dados formatados para exibição
def formatar_parametros(dados):
    for chave,valor in dados.items():
        lista_dados_xml.append(chave.ljust(tamanho_coluna)+valor)
    lista_dados_xml.append(separador_enlace)


def existe_enlace(teste_enlace):
    teste_enlace = '<owl:NamedIndividual rdf:about="&ontodatalink;' + teste_enlace
    for linha in lista_owl_rdfs:
        if (teste_enlace in linha):
            return True
    return False


def existe_roteador(teste_roteador):
    teste_roteador = '&ontodatalink;' + teste_roteador
    for linha in lista_owl_rdfs:
        if (teste_roteador in linha):
            return True
    return False


#Recebe um dicionário com os parâmetros e respectivos valores
#Retorna uma lista com tuplas em OWL-RDFS
def parse_owl_rdfs(dados):

    def gera_tupla(sujeito, predicado, objeto, tipo):
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + sujeito + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;' + tipo + '"/>')
        lista_owl_rdfs.append('        <' + predicado + ' rdf:resource="&ontodatalink;' + objeto + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')

    #Gerando ID
    def_enlace = dados["Enlace"]
    def_servico = "SER_" + def_enlace
    def_contrato = "CON_" + def_enlace
    def_operacao = "OPE_" + def_enlace
    def_sla = "SLA_" + def_enlace
    def_custo = "CUS_" + def_enlace
    def_banda = "BAN_" + def_enlace
    if existe_enlace(def_enlace):
        lista_alertas.append('Enlace ' + def_enlace + ' --> Já passou pelo parse; será considerada apenas a primeira instância.')
    else:
        # Instanciando SERVIÇO
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_servico + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Serviço"/>')
        lista_owl_rdfs.append('        <possuiDescriçãoServiço rdf:datatype="&xsd;string">Este serviço converge os parâmetros de Contrato, Enlace e Operação nos níveis de Governança, Gerenciamento e Operacional para o enlace ' + def_enlace + '.</possuiDescriçãoServiço>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        # Instanciando CONTRATO
        #gera_tupla(def_contrato, 'ehParteDeServiço', def_servico, 'Contrato')
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_contrato + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Contrato"/>')
        lista_owl_rdfs.append('        <possuiDescriçãoContrato rdf:datatype="&xsd;string">Contrato relativo ao serviço ' + def_servico + ' que opera o enlace ' + def_enlace + '.</possuiDescriçãoContrato>')
        lista_owl_rdfs.append('        <ehParteDeServiço rdf:resource = "&ontodatalink;' + def_servico + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        # Instanciando OPERAÇÃO E ENLACE
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_operacao + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Operação"/>')
        lista_owl_rdfs.append('        <possuiDescriçãoOperação rdf:datatype="&xsd;string">Operação relativa ao serviço ' + def_servico + ' que opera o enlace ' + def_enlace + '.</possuiDescriçãoOperação>')
        lista_owl_rdfs.append('        <possuiDemanda rdf:datatype="&xsd;string">' + dados["Demanda"] + '</possuiDemanda>')
        lista_owl_rdfs.append('        <possuiQtdEstimadaTerminais rdf:datatype="&xsd;integer">' + dados["QtdEstimadaTerminais"] + '</possuiQtdEstimadaTerminais>')
        lista_owl_rdfs.append('        <ehParteDeServiço rdf:resource = "&ontodatalink;' + def_servico + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_enlace + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Enlace"/>')
        lista_owl_rdfs.append('        <possuiDescriçãoEnlace rdf:datatype="&xsd;string">' + dados["Enlace_Descricao"] + '</possuiDescriçãoEnlace>')
        lista_owl_rdfs.append('        <possuiMeio rdf:datatype="&xsd;string">' + dados["Meio"] + '</possuiMeio>')
        lista_owl_rdfs.append('        <ehParteDeServiço rdf:resource = "&ontodatalink;' + def_servico + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        # Instanciando ROTEADORES
        if existe_roteador(dados['Roteador1']):
            lista_alertas.append('Roteador ' + dados['Roteador1'] + ' --> Já passou pelo parse em outro enlace; será considerada apenas a primeira instância.')
            lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + dados['Roteador1'] + '">')
            lista_owl_rdfs.append('        <ehParteDeEnlace rdf:resource = "&ontodatalink;' + def_enlace + '"/>')
            lista_owl_rdfs.append('    </owl:NamedIndividual>')
        else:
            lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + dados['Roteador1'] + '">')
            lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Roteador"/>')
            lista_owl_rdfs.append('        <possuiDescriçãoRoteador rdf:datatype="&xsd;string">' + dados['Roteador1_Descricao'] + '</possuiDescriçãoRoteador>')
            lista_owl_rdfs.append('        <possuiLocalização rdf:datatype="&xsd;string">' + dados['Roteador1_Localizacao'] + '</possuiLocalização>')
            lista_owl_rdfs.append('        <ehParteDeEnlace rdf:resource = "&ontodatalink;' + def_enlace + '"/>')
            lista_owl_rdfs.append('    </owl:NamedIndividual>')
        if existe_roteador(dados['Roteador2']):
            lista_alertas.append('Roteador ' + dados['Roteador2'] + ' --> Já passou pelo parse em outro enlace; será considerada apenas a primeira instância.')
        else:
            lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + dados['Roteador2'] + '">')
            lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Roteador"/>')
            lista_owl_rdfs.append('        <possuiDescriçãoRoteador rdf:datatype="&xsd;string">' + dados['Roteador2_Descricao'] + '</possuiDescriçãoRoteador>')
            lista_owl_rdfs.append('        <possuiLocalização rdf:datatype="&xsd;string">' + dados['Roteador2_Localizacao'] + '</possuiLocalização>')
            lista_owl_rdfs.append('        <ehParteDeEnlace rdf:resource = "&ontodatalink;' + def_enlace + '"/>')
            lista_owl_rdfs.append('    </owl:NamedIndividual>')
        #Instanciando PROTOCOLO, MEIO, DEMANDA E TERMINAIS
        gera_tupla(dados['Protocolo'], 'ehParteDeEnlace', def_enlace, 'Protocolo')
        # Instanciando BANDA e parâmetros
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_banda + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Banda"/>')
        lista_owl_rdfs.append('        <possuiBandaLimítrofeOperação rdf:datatype="&xsd;integer">' + dados["Operacao_Banda_Limitrofe"].replace(" Mbps","").replace(" Gbps","000") + '</possuiBandaLimítrofeOperação>')
        lista_owl_rdfs.append('        <possuiBandaDesejávelOperação rdf:datatype="&xsd;integer">' + dados["Operacao_Banda_Desejavel"].replace(" Mbps","").replace(" Gbps","000") + '</possuiBandaDesejávelOperação>')
        lista_owl_rdfs.append('        <possuiBandaLimítrofeGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_Banda_Limitrofe"].replace(" Mbps","").replace(" Gbps","000") + '</possuiBandaLimítrofeGerenciamento>')
        lista_owl_rdfs.append('        <possuiBandaDesejávelGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_Banda_Desejavel"].replace(" Mbps","").replace(" Gbps","000") + '</possuiBandaDesejávelGerenciamento>')
        lista_owl_rdfs.append('        <ehParteDeContrato rdf:resource = "&ontodatalink;' + def_contrato + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        # Instanciando CUSTO e parâmetros
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_custo + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;Custo"/>')
        lista_owl_rdfs.append('        <possuiCustoLimítrofeGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_Custo_Limitrofe"] + '</possuiCustoLimítrofeGerenciamento>')
        lista_owl_rdfs.append('        <possuiCustoDesejávelGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_Custo_Desejavel"] + '</possuiCustoDesejávelGerenciamento>')
        lista_owl_rdfs.append('        <possuiCustoLimítrofeGovernança rdf:datatype="&xsd;integer">' + dados["Governanca_Custo_Limitrofe"] + '</possuiCustoLimítrofeGovernança>')
        lista_owl_rdfs.append('        <possuiCustoDesejávelGovernança rdf:datatype="&xsd;integer">' + dados["Governanca_Custo_Desejavel"] + '</possuiCustoDesejávelGovernança>')
        lista_owl_rdfs.append('        <ehParteDeContrato rdf:resource = "&ontodatalink;' + def_contrato + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        #Instanciando SLA e parâmetros
        lista_owl_rdfs.append('    <owl:NamedIndividual rdf:about="&ontodatalink;' + def_sla + '">')
        lista_owl_rdfs.append('        <rdf:type rdf:resource="&ontodatalink;SLA"/>')
        lista_owl_rdfs.append('        <possuiSLALimítrofeOperação rdf:datatype="&xsd;integer">' + dados["Operacao_SLA_Limitrofe"].replace(" horas","") + '</possuiSLALimítrofeOperação>')
        lista_owl_rdfs.append('        <possuiSLADesejávelOperação rdf:datatype="&xsd;integer">' + dados["Operacao_SLA_Desejavel"].replace(" horas","") + '</possuiSLADesejávelOperação>')
        lista_owl_rdfs.append('        <possuiSLALimítrofeGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_SLA_Limitrofe"].replace(" horas","") + '</possuiSLALimítrofeGerenciamento>')
        lista_owl_rdfs.append('        <possuiSLADesejávelGerenciamento rdf:datatype="&xsd;integer">' + dados["Gerenciamento_SLA_Desejavel"].replace(" horas","") + '</possuiSLADesejávelGerenciamento>')
        lista_owl_rdfs.append('        <possuiSLALimítrofeGovernança rdf:datatype="&xsd;integer">' + dados["Governanca_SLA_Limitrofe"].replace(" horas","") + '</possuiSLALimítrofeGovernança>')
        lista_owl_rdfs.append('        <possuiSLADesejávelGovernança rdf:datatype="&xsd;integer">' + dados["Governanca_SLA_Desejavel"].replace(" horas","") + '</possuiSLADesejávelGovernança>')
        lista_owl_rdfs.append('        <ehParteDeContrato rdf:resource = "&ontodatalink;' + def_contrato + '"/>')
        lista_owl_rdfs.append('    </owl:NamedIndividual>')
        lista_alertas.append('Enlace ' + def_enlace + ' --> Parse concluído.')


def merge_ontologia_owl_rdfs(dados):
    arquivo = open('ODL_Ontologia_Inicial.owl', 'r', encoding='UTF-8')
    temp_lista = list()
    linha = arquivo.readline()
    while True:
        if ('General axioms' in linha):
            temp_lista.append('    // Instâncias do Projeto Onto_Data_Link\n')
            temp_lista.append('    //\n')
            temp_lista.append('    ///////////////////////////////////////////////////////////////////////////////////////\n')
            temp_lista.append('    -->\n')
            for linha_owl_rdfs in dados:
                temp_lista.append(linha_owl_rdfs+'\n')
            temp_lista.append('    <!--\n')
            temp_lista.append('    ///////////////////////////////////////////////////////////////////////////////////////\n')
            temp_lista.append('    //\n')
            temp_lista.append(linha)
            linha = arquivo.readline()
        elif (linha == ''):
            break
        else:
            temp_lista.append(linha)
            linha = arquivo.readline()
    arquivo.close()
    lista_alertas.append('Código OWL/RDFS --> Gerado.')
    lista_alertas.append('Merge com ontologia --> Realizado.')
    lista_alertas.append('Nova ontologia --> ' + str(len(temp_lista)) + ' linhas.')
    return temp_lista

def exporta_owl_rdfs(lista_exportacao):
    arquivo_owl_rdfs = open('ODL_Ontologia.owl','wt', encoding='UTF-8')
    for linha in lista_exportacao:
        arquivo_owl_rdfs.write(linha)
    arquivo_owl_rdfs.close()
    arquivo_log = open('ODL_LOG.txt', 'wt', encoding='UTF-8')
    arquivo_log.write('========================================================='+ '\n')
    arquivo_log.write('===== MENSAGENS ========================================='+ '\n')
    arquivo_log.write('========================================================='+ '\n')
    for linha in lista_alertas:
        arquivo_log.write(linha + '\n')
    arquivo_log.write('========================================================='+ '\n')
    arquivo_log.write('===== ENLACES E PARÂMETROS =============================='+ '\n')
    arquivo_log.write('========================================================='+ '\n')
    for linha in lista_dados_xml:
        arquivo_log.write(linha + '\n')
    arquivo_log.write('========================================================='+ '\n')
    arquivo_log.write('===== OWL/RDFS =PARÂMETROS =============================='+ '\n')
    arquivo_log.write('========================================================='+ '\n')
    for linha in lista_exportacao:
        arquivo_log.write(linha)
    arquivo_log.write('========================================================='+ '\n')
    arquivo_log.write('===== FINAL DO LOG ======================================'+ '\n')
    arquivo_log.write('========================================================='+ '\n')
    arquivo_log.close()

valido = True

#Testa se o arquivo "ODL_Ontologia_Inicial.owl" existe
try:
    testa_arquivo = open('ODL_Ontologia_Inicial.owl')
    testa_arquivo.close()
    valido = True
except:
    messagebox.showinfo(title='ATENÇÃO', message='O arquivo ODL_Ontologia_Inicial.owl não foi localizado na pasta corrente. Esse arquivo é essencial para o parse e a exportação pois contém a ontologia "Master".')
    valido = False
    #exit(1)

if valido:
    #Seleção de arquivo(s) xml do enlace a ser trabalhado
    lista_arquivo_enlace = filedialog.askopenfilenames(title='Escolha um ou mais arquivos XML contendo a definição de ENLACE',filetypes =[('Enlaces', '*Enlace*.xml')])
    if lista_arquivo_enlace == "":
        #exit(0)
        valido = False

if valido:
    #Lê os dados de entrada (xml), realiza o parse e gera entradas OWL/RDF-S
    global tamanho_coluna, separador_enlace, lista_dados_xml, lista_owl_rdfs, lista_alertas
    tamanho_coluna = 30
    separador_enlace = "====="
    lista_dados_xml  = list()
    lista_owl_rdfs   = list()
    lista_alertas    = list()
    lista_alertas.append('Arquivo ODL_Ontologia_Inicial.owl --> Encontrado.')
    for nome_arquivo_enlace in lista_arquivo_enlace:
        obj_pre_parse = ler_xml(nome_arquivo_enlace)
        formatar_parametros(obj_pre_parse)
        parse_owl_rdfs(obj_pre_parse)
    lista_owl_rdfs = merge_ontologia_owl_rdfs(lista_owl_rdfs)


    #Exibe tela
    gui.change_look_and_feel('DefaultNoMoreNagging')
    layout = [
        [gui.Text('FASE 2 - PARSE E EXPORTAÇÃO DE PARÂMETROS',font='Bold')],
        [gui.Text(' ')],
        [gui.Text('DADOS DO ENLACE E RESPECTIVOS PARÂMETROS')],
        [gui.LB(lista_dados_xml,size=(120,7), font='courier 11')],
        [gui.Text(' ')],
        [gui.Text('RESULTADO DO PARSE E GERAÇÃO DE CÓDIGO OWL/RDFS')],
        [gui.LB(lista_owl_rdfs, size=(120, 7), font='courier 11')],
        [gui.Text(' ')],
        [gui.Text('MENSAGENS DO PARSE')],
        [gui.LB(lista_alertas, size=(120,7), font='courier 11')],
        [gui.Text(' ')],
        [gui.Button('  Gravar Arquivo OWL-RDF/S  ', key='butInserir'), gui.Button('Cancelar')],
        [gui.Text(' ')]]
    janela = gui.Window('Projeto OntoDataLink',layout)


    #Trata eventos
    while True:
        evento, valores = janela.read()
        if (evento == gui.WIN_CLOSED or evento == 'Cancelar'):
            break
        if (evento == 'butInserir'):
            exporta_owl_rdfs(lista_owl_rdfs)
            break


    #Encerramento
    janela.close()
