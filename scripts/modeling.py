# scripts/model.py

from typing import List
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scripts.logger import logger

def selecionar_variaveis(df: pd.DataFrame, features: List[str] = None) -> np.ndarray:
    if features is None:
        features = [
            'Total_Spent', 'Total_Purchases', 'MntWines', 'MntMeatProducts',
            'Income', 'Campaign_Response_Flag', 'Total_Accepted_Campaigns',
            'NumCatalogPurchases', 'NumStorePurchases', 'Online_Ratio'
        ]
    ausentes = [col for col in features if col not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas ausentes no DataFrame: {ausentes}")

    X = df[features].copy()
    X_scaled = StandardScaler().fit_transform(X)

    logger.info("Variáveis selecionadas e normalizadas para KMeans.")
    return X_scaled

def aplicar_kmeans(X: np.ndarray, n_clusters: int = 3, random_state: int = 42) -> np.ndarray:
    modelo = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = modelo.fit_predict(X)
    logger.info("KMeans aplicado com sucesso.")
    return labels

def adicionar_rotulos_cluster(df: pd.DataFrame, labels: np.ndarray, coluna: str = "Cluster_KMeans") -> pd.DataFrame:
    df_final = df.copy()
    df_final[coluna] = labels

    cluster_map = {
        0: "Baixa Conversão",
        1: "Alta Conversão",
        2: "Média Conversão"
    }
    df_final["Conversion_Level"] = df_final[coluna].map(cluster_map)

    logger.info("Rótulos de cluster adicionados.")
    return df_final