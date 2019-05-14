import pandas as pd
import sqlite3
import pymysql
from datetime import datetime as dt

print("Iniciando a conexão com SQLITE...")
#con = sqlite3.connect('db.sqlite3')
try:
    con = pymysql.connect("mysql.miguelzamberlan.com.br","miguelzamberla02","a1b4k9ph","miguelzamberla02" )
    print(con)
    cur = con.cursor()
except Exception as err:
    print("Erro: ", err.args)


print("Limpando a tabela de Atas...")
query = "DELETE FROM pesquisa_ata"
cur.execute(query)
con.commit()


print("Lendo o arquivo CSV...")
arquivos = ['atas_vigentesN.csv', 'atas_vigentesCO.csv', 'atas_vigentesSE.csv']
#arquivos = ['atas_vigentesN.csv']

log_erro = []

for arquivo in arquivos:
    print("Lendo arquivo: ", arquivo)
    data = pd.read_csv(arquivo)

    print("Criando o DATASET para inclusão...")
    full_dataset = []
    full_dataset.append(data)

    registros = []

    for i in range(0,len(full_dataset)):
        #print(full_dataset[i].head(0))
        nomeColunas = list(full_dataset[i].head(0))
        registros.append(nomeColunas)

    full_dataset[0] = full_dataset[0].astype(str)

    #print(full_dataset)

    print("Formando as query's...")
    #query = "INSERT INTO pesquisa_ata (gerenciador, gerenciador_nome, uf, modalidade, certame, cnpj_fornecedor, nome_fornecedor, porte_fornecedor, \
    #    munic_fornecedor, uf_fornecedor, tipo, cod_cat, nome_cat, desc_catalogo, grupo_material, data_homologacao, data_final_vigencia, \
    #    prorrogacao_ata, item, descricao_complementar_p1, descricao_complementar_p2, fabricante, marca, unidade, qtd_ofertada, valor_unitario, \
    #    valor_total) VALUES ("+','.join(map(str,'?'*len(full_dataset[0].columns))) + ")"

    #print(query)

    #print("Iniciando a inserção dos dados...")
    for x in range(0, len(full_dataset[0])):

        inserir_registro = list(full_dataset[0].iloc[x])
        #print("PRIMEIRO: ", inserir_registro)

        # Corrigindo dados
        inserir_registro[0] = int(inserir_registro[0]) #Codigo gerenciador
        inserir_registro[16] = dt.strftime(dt.strptime(str(inserir_registro[16]), '%d/%m/%Y'), '%Y-%m-%d') #data vigencia
        inserir_registro[24] = float(inserir_registro[24].replace('.','')) #qtd_ofertada

        # valor unitario
        #valor_unitario = '200'
        valor_unitario = str(inserir_registro[25])
        valor_unitario = valor_unitario.replace('.','')
        valor_unitario = valor_unitario.replace(',','.')
        inserir_registro[25] = float(valor_unitario)

        # valor total
        #valor_total = '500'
        valor_total = str(inserir_registro[26])
        valor_total = valor_total.replace('.','')
        valor_total = valor_total.replace(',','.')
        inserir_registro[26] = float(valor_total)

        #print("SEGUNDO: ", inserir_registro)

        d = inserir_registro

        query = "INSERT INTO pesquisa_ata (gerenciador, gerenciador_nome, uf, modalidade, certame, cnpj_fornecedor, nome_fornecedor, porte_fornecedor, \
munic_fornecedor, uf_fornecedor, tipo, cod_cat, nome_cat, desc_catalogo, grupo_material, data_homologacao, data_final_vigencia, \
prorrogacao_ata, item, descricao_complementar_p1, descricao_complementar_p2, fabricante, marca, unidade, qtd_ofertada, valor_unitario, \
valor_total) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17], d[18], d[19], d[20], d[21], d[22], d[23], d[24], d[25], d[26])

        print(query)

        print("Registro ", x)
        try:
            result = cur.execute(query)
            print(result)
            if result:
                con.commit()

        except Exception as err:
            print("Erro: ", err.args)
            log_erro.append(err.args)
            con.rollback()
            continue


con.close()

print("Erros")
for mostra in log_erro:
    print(mostra)