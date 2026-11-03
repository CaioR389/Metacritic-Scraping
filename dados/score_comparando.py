import os
import pandas as pd
#usa os dados obtidos e faz uma comparação ano por ano

def extrair_quantitativo():
    lista_dados = []
    # pega todos os anos direto da pasta onde estao os arquivos de 2000 a 2026
    pasta_dados = os.path.join("..", "dados", "jogos_por_ano")

    # se ja tiver os arquivos limpos na pasta atual, prioriza eles
    arquivos_locais = [f for f in os.listdir(".") if f.startswith("jogos") and f.endswith("_limpo.csv")]
    if arquivos_locais:
        pasta_dados = "."

    for nome_csv in sorted(os.listdir(pasta_dados)):
        if nome_csv.startswith("jogos") and nome_csv.endswith(".csv") and "geral" not in nome_csv:
            try:
                caminho_arquivo = os.path.join(pasta_dados, nome_csv)
                df = pd.read_csv(caminho_arquivo, sep='\t')

                # padroniza o nome da coluna caso venha dos brutos (com acento) ou limpos (sem acento)
                if 'gênero' in df.columns:
                    df['genero'] = df['gênero']

                df['ano'] = nome_csv[5:9]
                lista_dados.append(df)
                print(f"lido: {nome_csv}")
            except Exception as e:
                print(f"deu erro chefe, foi isso aqui {nome_csv}: {e}")

    if lista_dados:
        df_final = pd.concat(lista_dados, ignore_index=True)
        return df_final
    else:
        print("sobrou nada")
        return None

def analisar_anos(df):
    total_jogos_ano = {}

    soma_meta = {}
    cont_meta = {}
    soma_user = {}
    cont_user = {}

    melhor_jogo_meta = {}
    nota_melhor_meta = {}
    user_do_melhor_meta = {}

    pior_jogo_meta = {}
    nota_pior_meta = {}
    user_do_pior_meta = {}

    melhor_jogo_user = {}
    nota_melhor_user = {}
    meta_do_melhor_user = {}

    pior_jogo_user = {}
    nota_pior_user = {}
    meta_do_pior_user = {}

    soma_qnt_meta = {}
    cont_qnt_meta = {}
    soma_qnt_user = {}
    cont_qnt_user = {}

    # primeiro loop: calcula somas, quantidades e acha os melhores/piores jogos de cada ano
    for i in range(len(df)):
        nome = str(df['nome'][i])
        ano = str(df['ano'][i])

        if "====" in nome or ano == "nan":
            continue

        ano = ano.replace(".0", "")
        meta = str(df['metascore'][i])
        user = str(df['userscore'][i])
        q_meta = str(df['qnt_meta'][i]).replace(",", "")
        q_user = str(df['qnt_user'][i]).replace(",", "")

        if ano not in soma_meta:
            total_jogos_ano[ano] = 0
            soma_meta[ano] = 0
            cont_meta[ano] = 0
            soma_user[ano] = 0
            cont_user[ano] = 0

            melhor_jogo_meta[ano] = "-"
            nota_melhor_meta[ano] = -1
            user_do_melhor_meta[ano] = "-"

            pior_jogo_meta[ano] = "-"
            nota_pior_meta[ano] = 101
            user_do_pior_meta[ano] = "-"

            melhor_jogo_user[ano] = "-"
            nota_melhor_user[ano] = -1
            meta_do_melhor_user[ano] = "-"

            pior_jogo_user[ano] = "-"
            nota_pior_user[ano] = 11
            meta_do_pior_user[ano] = "-"

            soma_qnt_meta[ano] = 0
            cont_qnt_meta[ano] = 0
            soma_qnt_user[ano] = 0
            cont_qnt_user[ano] = 0

        total_jogos_ano[ano] += 1

        if meta != "-" and meta != "tbd" and meta != "tdb" and meta != "nan":
            try:
                nota_m = float(meta)
                soma_meta[ano] += nota_m
                cont_meta[ano] += 1

                if nota_m > nota_melhor_meta[ano]:
                    nota_melhor_meta[ano] = nota_m
                    melhor_jogo_meta[ano] = nome
                    user_do_melhor_meta[ano] = user

                if nota_m < nota_pior_meta[ano]:
                    nota_pior_meta[ano] = nota_m
                    pior_jogo_meta[ano] = nome
                    user_do_pior_meta[ano] = user
            except ValueError:
                pass

        if user != "-" and user != "tbd" and user != "tdb" and user != "nan":
            try:
                nota_u = float(user)
                soma_user[ano] += nota_u
                cont_user[ano] += 1

                if nota_u > nota_melhor_user[ano]:
                    nota_melhor_user[ano] = nota_u
                    melhor_jogo_user[ano] = nome
                    meta_do_melhor_user[ano] = meta

                if nota_u < nota_pior_user[ano]:
                    nota_pior_user[ano] = nota_u
                    pior_jogo_user[ano] = nome
                    meta_do_pior_user[ano] = meta
            except ValueError:
                pass

        if q_meta != "-" and q_meta != "tbd" and q_meta != "tdb" and q_meta != "nan":
            try:
                soma_qnt_meta[ano] += int(float(q_meta))
                cont_qnt_meta[ano] += 1
            except ValueError:
                pass

        if q_user != "-" and q_user != "tbd" and q_user != "tdb" and q_user != "nan":
            try:
                soma_qnt_user[ano] += int(float(q_user))
                cont_qnt_user[ano] += 1
            except ValueError:
                pass

    # calcula as medias do ano para comparar no segundo loop
    media_meta = {}
    media_user = {}
    for ano in soma_meta:
        media_meta[ano] = soma_meta[ano] / cont_meta[ano] if cont_meta[ano] > 0 else 0
        media_user[ano] = soma_user[ano] / cont_user[ano] if cont_user[ano] > 0 else 0

    # segundo loop: conta quantos jogos do ano ficaram na media/acima ou abaixo da media
    acima_media_meta = {}
    abaixo_media_meta = {}
    acima_media_user = {}
    abaixo_media_user = {}

    for ano in soma_meta:
        acima_media_meta[ano] = 0
        abaixo_media_meta[ano] = 0
        acima_media_user[ano] = 0
        abaixo_media_user[ano] = 0

    for i in range(len(df)):
        nome = str(df['nome'][i])
        ano = str(df['ano'][i])

        if "====" in nome or ano == "nan":
            continue

        ano = ano.replace(".0", "")
        meta = str(df['metascore'][i])
        user = str(df['userscore'][i])

        if meta != "-" and meta != "tbd" and meta != "tdb" and meta != "nan":
            try:
                nota_m = float(meta)
                if nota_m >= media_meta[ano]:
                    acima_media_meta[ano] += 1
                else:
                    abaixo_media_meta[ano] += 1
            except ValueError:
                pass

        if user != "-" and user != "tbd" and user != "tdb" and user != "nan":
            try:
                nota_u = float(user)
                if nota_u >= media_user[ano]:
                    acima_media_user[ano] += 1
                else:
                    abaixo_media_user[ano] += 1
            except ValueError:
                pass

    # colunas deixando expresso o que e de um jogo especifico e o que e de todos os jogos do ano
    csv_final = "comparativo_dados.csv"
    colunas = [
        "ano",
        "total_jogos_do_ano",
        "melhor_jogo_ano_metacritic",
        "nota_metacritic_melhor_jogo_meta",
        "nota_usuario_melhor_jogo_meta",
        "pior_jogo_ano_metacritic",
        "nota_metacritic_pior_jogo_meta",
        "nota_usuario_pior_jogo_meta",
        "melhor_jogo_ano_usuario",
        "nota_usuario_melhor_jogo_user",
        "nota_metacritic_melhor_jogo_user",
        "pior_jogo_ano_usuario",
        "nota_usuario_pior_jogo_user",
        "nota_metacritic_pior_jogo_user",
        "media_metascore_todos_jogos_ano",
        "qnt_jogos_ano_acima_media_metacritic",
        "qnt_jogos_ano_abaixo_media_metacritic",
        "media_userscore_todos_jogos_ano",
        "qnt_jogos_ano_acima_media_usuario",
        "qnt_jogos_ano_abaixo_media_usuario",
        "total_avaliacoes_metacritic_todos_jogos_ano",
        "media_avaliacoes_metacritic_todos_jogos_ano",
        "total_avaliacoes_usuario_todos_jogos_ano",
        "media_avaliacoes_usuario_todos_jogos_ano"
    ]

    with open(csv_final, 'w', encoding="utf-8") as arquivo:
        arquivo.write("\t".join(colunas) + "\n")

        for ano in sorted(soma_meta.keys()):
            m_meta = round(media_meta[ano], 2)
            m_user = round(media_user[ano], 2)
            m_qmeta = round(soma_qnt_meta[ano] / cont_qnt_meta[ano], 1) if cont_qnt_meta[ano] > 0 else 0
            m_quser = round(soma_qnt_user[ano] / cont_qnt_user[ano], 1) if cont_qnt_user[ano] > 0 else 0

            linha = [
                ano,
                str(total_jogos_ano[ano]),
                melhor_jogo_meta[ano],
                str(nota_melhor_meta[ano]),
                str(user_do_melhor_meta[ano]),
                pior_jogo_meta[ano],
                str(nota_pior_meta[ano]),
                str(user_do_pior_meta[ano]),
                melhor_jogo_user[ano],
                str(nota_melhor_user[ano]),
                str(meta_do_melhor_user[ano]),
                pior_jogo_user[ano],
                str(nota_pior_user[ano]),
                str(meta_do_pior_user[ano]),
                str(m_meta),
                str(acima_media_meta[ano]),
                str(abaixo_media_meta[ano]),
                str(m_user),
                str(acima_media_user[ano]),
                str(abaixo_media_user[ano]),
                str(soma_qnt_meta[ano]),
                str(m_qmeta),
                str(soma_qnt_user[ano]),
                str(m_quser)
            ]
            arquivo.write("\t".join(linha) + "\n")
            print(f"{ano} ({total_jogos_ano[ano]} jogos) -> media_meta: {m_meta} | media_user: {m_user}")

    print(f"\ncsv gerado : {csv_final}")

def qnt_publicada_genero(df):
    generos = {}

    for i in range(len(df)):
        gen = str(df['genero'][i])
        if gen != "tbd" and gen != "tdb" and gen != "-" and gen != "nan":
            if gen not in generos:
                generos[gen] = 1
            else:
                generos[gen] += 1

    print("\nquantidade por genero:")
    for gen in generos:
        print(f"{gen}: {generos[gen]}")

def contador_publicadora_favorita_media(df):
    soma_pub = {}
    qnt_jogos = {}

    for i in range(len(df)):
        pub = str(df['publisher'][i])
        nota = str(df['metascore'][i])

        if pub != "tbd" and pub != "tdb" and pub != "nan" and nota != "-" and nota != "nan":
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

    print(f"\npublicadora favorita: {favorita} ({maior_media:.2f})")
    return favorita

def main():
    df = extrair_quantitativo()
    if df is not None:
        analisar_anos(df)
        qnt_publicada_genero(df)
        contador_publicadora_favorita_media(df)

if __name__ == "__main__":
	main()
