import pandas as pd
from pathlib import Path

arquivos = sorted(Path("jogos_por_ano").glob("jogos*_limpo.csv"))
print(len(arquivos))   

partes = []
for a in arquivos:
    d = pd.read_csv(a, sep="\t", dtype=str, keep_default_na=False)
    d["ano"] = a.stem[5:9]   
    partes.append(d)

todos = pd.concat(partes, ignore_index=True)
print(todos.shape)

todos.to_csv("jogos_geral.csv", sep="\t", index=False)