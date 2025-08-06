#Scripts/pipeline.py

import pandas as pd
from scripts.logger import logger
from scripts.processing import (
    ler_dados, composicao, nulos, feature_engineering, clean_df, normalizar_df
)

from scripts.modeling import (
    selecionar_variaveis, aplicar_kmeans, adicionar_rotulos_cluster
)


def pipeline_clusterizacao(path_raw: str, path_processed: str) -> pd.DataFrame:
    df = ler_dados(path_raw)
    if df.empty:
        logger.error("DataFrame vazio. Encerrando execução.")
        return df

    composicao(df)
    nulos(df)
    feature_engineering(df)
    _, df_clean = clean_df(df)
    df_cluster = normalizar_df(df_clean)
    X = selecionar_variaveis(df_clean)

    labels = aplicar_kmeans(X)
    df_final = adicionar_rotulos_cluster(df_clean, labels)
    df_final.to_csv(path_processed, index=False)
    logger.info(f"Arquivo final salvo em: {path_processed}")

    return df_final