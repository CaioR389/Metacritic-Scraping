import csv
import os
import pandas as pd
#usa os dados obtidos e faz uma comparação ano por ano
def media_pub_favorita(df):
    soma_pub = {}
    qnt_jogos = {}

    for i in range(len(df)):
        pub = df['publisher'][i]
        nota = df['metascore'][i]

        if pub != "tbd" and pub != "tdb" and nota != "-":
            try:
                nota = float(nota)
                if pub not in soma_pub:
                    soma_pub[pub] = nota
                    qnt_jogos[pub] = 1
                else:
                    soma_pub[pub] += nota
                    qnt_jogos[pub] += 1
            except ValueError:
                continue

    maior_media = 0
    favorita = ""
    for pub in soma_pub:
        if qnt_jogos[pub] >= 5:
            media = soma_pub[pub] / qnt_jogos[pub]
            if media > maior_media:
                maior_media = media
                favorita = pub

    print(f"publicadora favorita: {favorita} ({maior_media:.2f})")
    return favorita

def extrair_quantitativo():

    # diz onde o jogos_geral.csv tá
    caminho_csv = os.path.join("..", "Dados dos jogos", "jogos_geral.csv")
    colunas_desejadas = ['nome', 'ano', 'metascore', 'qnt_meta', 'userscore', 'qnt_user', 'publisher', 'genero']
    csv_final = "comparativo_dados.csv"
    
    try:
        df = pd.read_csv(caminho_csv, sep='\t', usecols=colunas_desejadas)
        
        #salva o arquivo final na pasta atual, é bom mudar, acho)
        df.to_csv(csv_final, sep='\t', index=False, encoding="utf-8")
        
        print(f"dados extraídos do jogos_geral.csv e csv gerado: {csv_final}")
        return df
    except Exception as e:
        print(f"deu erro chefe 'tem dia que é noite', foi isso aqui: {e}")
        return None

def media_metascore(df):
    soma_meta = {}
    cont_meta = {}
    soma_user = {}
    cont_user = {}

    for i in range(len(df)):
        ano = df['ano'][i]
        meta = df['metascore'][i]
        user = df['userscore'][i]

        if ano not in soma_meta:
            soma_meta[ano] = 0
            cont_meta[ano] = 0
            soma_user[ano] = 0
            cont_user[ano] = 0

        if meta != "-" and meta != "tbd" and meta != "tdb":
            try:
                soma_meta[ano] += float(meta)
                cont_meta[ano] += 1
            except ValueError:
                continue

        if user != "-" and user != "tbd" and user != "tdb":
            try:
                soma_user[ano] += float(user)
                cont_user[ano] += 1
            except ValueError:
                continue

    print("\nmedia metascore e userscore por ano:")
    for ano in soma_meta:
        if cont_meta[ano] > 0 and cont_user[ano] > 0:
            m_meta = soma_meta[ano] / cont_meta[ano]
            m_user = soma_user[ano] / cont_user[ano]
            print(f"{ano}: metascore {m_meta:.2f} | userscore {m_user:.2f}")

def media_qntcriticos(df):
    soma_criticos = {}
    cont_criticos = {}
    soma_usuarios = {}
    cont_usuarios = {}

    for i in range(len(df)):
        ano = df['ano'][i]
        q_meta = str(df['qnt_meta'][i]).replace(",", "")
        q_user = str(df['qnt_user'][i]).replace(",", "")

        if ano not in soma_criticos:
            soma_criticos[ano] = 0
            cont_criticos[ano] = 0
            soma_usuarios[ano] = 0
            cont_usuarios[ano] = 0

        if q_meta != "-" and q_meta != "tbd" and q_meta != "tdb":
            try:
                soma_criticos[ano] += int(q_meta)
                cont_criticos[ano] += 1
            except ValueError:
                continue

        if q_user != "-" and q_user != "tbd" and q_user != "tdb":
            try:
                soma_usuarios[ano] += int(q_user)
                cont_usuarios[ano] += 1
            except ValueError:
                continue

    print("\nmedia de avaliacoes por ano:")
    for ano in soma_criticos:
        if cont_criticos[ano] > 0 and cont_usuarios[ano] > 0:
            m_crit = soma_criticos[ano] / cont_criticos[ano]
            m_user = soma_usuarios[ano] / cont_usuarios[ano]
            print(f"{ano}: criticos {m_crit:.1f} | usuarios {m_user:.1f}")

def qnt_publicada_genero(df):
    generos = {}

    for i in range(len(df)):
        gen = df['genero'][i]
        if gen != "tbd" and gen != "tdb" and gen != "-":
            if gen not in generos:
                generos[gen] = 1
            else:
                generos[gen] += 1

    print("\nquantidade por genero:")
    for gen in generos:
        print(f"{gen}: {generos[gen]}")

def main():
    df = extrair_quantitativo()
    if df is not None:
        media_metascore(df)
        media_qntcriticos(df)
        qnt_publicada_genero(df)
        media_pub_favorita(df)

if __name__ == "__main__":
	main()
