from limpar import limpar
from pathlib import Path

from limpar import limpar
from pathlib import Path

for arq in sorted(Path(".").glob("jogos*.csv")):
    if "_limpo" in arq.stem:
        continue
    try:
        limpar(arq)
    except Exception as e:
        print("ERRO em", arq.name, "->", e)