import pandas as pd
import numpy as np
from pathlib import Path

colunas = ["nome", "url", "lancamento", "metascore", "qnt_meta", "pmn_meta",
           "userscore", "qnt_user", "pmn_user", "plataforma_nota",
           "desenvolvedora", "publisher", "genero"]

def limpar(arquivo):
    df = pd.read_csv(arquivo, sep=r"\s{3,}", engine="python",
                     skiprows=1, header=None, names=colunas)
    assert df.shape[1] == 13, f"{arquivo}: {df.shape[1]} colunas"

    for col in ["metascore", "userscore"]:
        df[col] = pd.to_numeric(df[col].replace("tbd", np.nan), errors="coerce")
    for col in ["qnt_meta", "qnt_user"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce")

    rep = df["metascore"] == df["userscore"]
    n_rep = rep.sum()
    df.loc[rep & (df["metascore"] > 10), "userscore"] = np.nan
    df.loc[rep & (df["metascore"] <= 10), "metascore"] = np.nan

    print(arquivo.name, df.shape,
          "| repetidas:", n_rep,
          "| userscore NaN:", df["userscore"].isna().sum(),
          "| qnt_user NaN:", df["qnt_user"].isna().sum(),
          "| ainda iguais:", (df["metascore"] == df["userscore"]).sum())

    for col in ["qnt_meta", "qnt_user"]:
        df[col] = df[col].astype("Int64").astype(object)
    cols_traco = ["metascore", "userscore", "qnt_meta", "qnt_user"]
    df[cols_traco] = df[cols_traco].fillna("-")

    saida = arquivo.with_name(arquivo.stem + "_limpo.csv")
    df.to_csv(saida, sep="\t", index=False)
    return df