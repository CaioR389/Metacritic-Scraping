import csv
from pathlib import Path
from config import cabeçalho
import pandas as pd

def juntar_anos(pasta="jogos_por_ano"):
    arquivos_limpos = sorted(Path(pasta).glob("jogos*_limpo.csv"))

    partes = []
    for a in arquivos_limpos:
        partes.append(pd.read_csv(a, sep="\t", dtype=str, keep_default_na=False))

    todos = pd.concat(partes, ignore_index=True)
    todos.to_csv("jogos_geral.csv", sep="\t", index=False)

    print("Gerado o CSV geral.")

def limpar_por_ano(pasta="jogos_por_ano"):
    for arq in sorted(Path(pasta).glob("jogos*.csv")):
        if "_limpo" in arq.stem or "geral" in arq.stem:
            continue

        todas_linhas = [cabeçalho]  

        with open(arq, newline="", encoding="utf-8") as f:
            linhas = csv.reader(f, delimiter="\t")
            next(linhas) 

            for verificar in linhas:
                verificar = ["" if c in ("tbd", "tdb") else c for c in verificar]
                
                if verificar[10].strip(" ,\xa0") == "":
                    verificar[10] = ""
                
                verificar[4] = verificar[4].replace(",", "")
                verificar[7] = verificar[7].replace(",", "")

                if verificar[3] != "" and verificar[3] == verificar[6]:
                    if float(verificar[3]) > 10:
                        verificar[6] = ""
                    else:
                        verificar[3] = ""

                todas_linhas.append(verificar)

        saida = arq.with_name(arq.stem + "_limpo.csv")
        with open(saida, "w", newline="", encoding="utf-8") as f_saida:
            csv.writer(f_saida, delimiter="\t").writerows(todas_linhas)

        print("Gerado:", saida.name)

def main():
    limpar_por_ano()
    juntar_anos()

if __name__ == "__main__":
	main()
