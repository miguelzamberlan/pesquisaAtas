import pandas as pd
import sqlite3
from datetime import datetime as dt

print("Iniciando a conexão com SQLITE...")
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

print("Limpando a tabela de Atas...")
query = "DELETE FROM pesquisa_ata"
cur.execute(query)
con.commit()


print("Lendo o arquivo CSV...")
arquivos = ['atas_vigentesN.csv', 'atas_vigentesCO.csv', 'atas_vigentesSE.csv']

for arquivo in arquivos:
    print(arquivo)
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

    print("Formando as query's...")
    query = "INSERT INTO pesquisa_ata (gerenciador, gerenciador_nome, uf, modalidade, certame, cnpj_fornecedor, nome_fornecedor, porte_fornecedor, \
        munic_fornecedor, uf_fornecedor, tipo, cod_cat, nome_cat, desc_catalogo, grupo_material, data_homologacao, data_final_vigencia, \
        prorrogacao_ata, item, descricao_complementar_p1, descricao_complementar_p2, fabricante, marca, unidade, qtd_ofertada, valor_unitario, \
        valor_total) VALUES ("+','.join(map(str,'?'*len(full_dataset[0].columns))) + ")"

    try:
        print("Iniciando a inserção dos dados...")
        for x in range(0, len(full_dataset[0])):
            inserir_registro = tuple(full_dataset[0].iloc[x])
            print("Registro ", x)
            cur.execute(query,inserir_registro)
        erroinsere = False
    except Exception as err:
        print("Erro: ", err.args)
        erroinsere = True

    if not erroinsere:
        con.commit()


print("Atualizando os valores dos campus Valor Unitario, Valor Total e Data Vigencia...")
cur.execute("SELECT id, valor_unitario, valor_total, data_final_vigencia FROM pesquisa_ata")
for dado in cur.fetchall():
    id = dado[0]
    valor_total = dado[2]
    valor_unitario = dado[1]
    data_vigencia = dado[3]
    print("Registro %s com os dados: Valor Total: %s, Valor Unitario: %s, Nova Data: %s" % (id, valor_total, valor_unitario, data_vigencia))
    try:
        valor_totaln = valor_total.replace('.','')
        valor_totaln = valor_totaln.replace(',','.')
        valor_totaln = float(valor_totaln)
        #print("ID: %s - Valor anterior: %s - Novo Valor: %s" % (id, valor_total, valor_totaln))

        valor_unitarion = valor_unitario.replace('.','')
        valor_unitarion = valor_unitarion.replace(',','.')
        valor_unitarion = float(valor_unitarion)
        #print("ID: %s - Valor anterior: %s - Novo Valor: %s" % (id, valor_unitario, valor_unitarion))

        data = dt.strptime(data_vigencia, '%d/%m/%Y')
        novadata = dt.strftime(data, '%Y-%m-%d')
        #print("ID: %s - Data anterior: %s - Data Nova: %s" % (id, data_vigencia, novadata))

        query = "UPDATE pesquisa_ata SET valor_total = '%s', valor_unitario = '%s', data_final_vigencia = '%s' WHERE id = %s" % (valor_totaln, valor_unitarion, novadata, id)

        print(query)
        cur.execute(query)

        erroatualiza = False
    except Exception as err:
        erroatualiza = True
        print("Erro: ", err.args)
        pass


if not erroatualiza:
    con.commit()


con.close()