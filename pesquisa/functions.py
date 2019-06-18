import pandas as pd

from pesquisa.models import Ata


def importa_dados_csv():

    data = pd.read_csv("atas_vigentesN.csv", sep=',')
    full_dataset = []
    full_dataset.append(data)

    registros = []

    for i in range(0, len(full_dataset)):
        # print(full_dataset[i].head(0))
        nomeColunas = list(full_dataset[i].head(0))
        registros.append(nomeColunas)

    full_dataset[0] = full_dataset[0].astype(str)

    for x in range(0, len(full_dataset[0])):
        dado = tuple(full_dataset[0].iloc[x])

        dt16 = dado[16].split('/')
        data_final_vigencia = f'{dt16[2]}-{dt16[1]}-{dt16[0]}'

        try:
            Ata.objects.update_or_create(
                gerenciador=dado[0],
                gerenciador_nome = dado[1][:200],
                uf = dado[2][:2],
                modalidade = dado[3][:200],
                certame = dado[4][:200],
                cnpj_fornecedor = dado[5][:200],
                nome_fornecedor = dado[6][:200],
                porte_fornecedor = dado[7][:200],
                munic_fornecedor = dado[8][:200],
                uf_fornecedor = dado[9][:200],
                tipo = dado[10][:200],
                cod_cat = dado[11][:200],
                nome_cat = dado[12],
                desc_catalogo = dado[13],
                grupo_material = dado[14][:200],
                data_homologacao = dado[15][:200],
                data_final_vigencia = data_final_vigencia,
                prorrogacao_ata = dado[17][:200],
                item = dado[18][:200],
                descricao_complementar_p1 = dado[19],
                descricao_complementar_p2 = dado[20],
                fabricante = dado[21][:200],
                marca = dado[22][:200],
                unidade = dado[23][:200],
                qtd_ofertada=int(dado[24].replace('.', '')),
                valor_unitario=float(dado[25].replace('.', '').replace(',','.')),
                valor_total=float(dado[26].replace('.', '').replace(',','.')),
            )

        except Exception as e:
            print(f'Erro nessa linha: {dado}')
            print(f'detalhe do erro {e}')

