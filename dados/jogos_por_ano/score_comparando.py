import csv
import os
import pandas as pd
#usa os dados obtidos e faz uma comparação ano por ano
    #os dados são extraídos da pasta

def contador_publicadora_favorita_media():#fazer
    return 0:

def extrair_quantitativo():
    
    listar_dados = []
    pasta_atual = os.getcwd()
    colunas_desejadas = ['nome','ano','metascore','qnt_críticos','userscore','qnt_usuário']
    csv_final = "comparativo_dados.csv"
        

        #junta as colunas pedidas
    for csv in os.listdir(pasta_atual):
        if csv.endswith(".csv") and csv != csv_final:

        try:
            # lê o nome do jogo e os dados quantitativos
            df = pd.read_csv(csv, usecols = colunas_desejadas)
            lista_dados.append(df)
            print(f"teste: {csv}")
            
        except Exception as e:
        print(f"deu erro chefe, foi isso aqui {csv}: {e}")

    #criando csv
    if lista_dados:
        df_final = pd.concat(lista_dados, ignore_index=True) 
        df_final.to_csv(csv_final, index=False, encoding="utf-8")
        print(f"\ncsv gerado : {csv_final}")
    else:
        print("sobrou nada")


def media_metascore():#fazer
    return 0:

def media_qntcriticos():#fazer
    return 0:

def qnt_publicada_genero():#fazer
    return 0:
