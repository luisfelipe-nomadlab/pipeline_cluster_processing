# scripts/preprocessing.py

from datetime import datetime
from typing import List, Tuple

import pandas as pd
from sklearn.preprocessing import StandardScaler
from scripts.logger import logger


def ler_dados(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path,sep = "\t")
        logger.info(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler os dados: {e}")
        return pd.DataFrame()

def composicao(df: pd.DataFrame) -> None:
    linhas, colunas = df.shape
    cat = df.select_dtypes(include="object").columns.tolist()
    num = df.select_dtypes(exclude="object").columns.tolist()

    logger.info("**Estrutura da base de dados**")
    logger.info(f"- Total de linhas: {linhas}, colunas: {colunas}")
    logger.info(f"- Colunas: {df.columns.tolist()}")
    logger.info(f"- Variáveis categóricas: {cat}")
    logger.info(f"- Variáveis numéricas: {num}")

def nulos(df: pd.DataFrame) -> None:
    total = df.isna().sum()
    perc = (total / len(df)) * 100
    df_nulos = pd.DataFrame({'total': total, 'percentual': perc})
    logger.info("**Distribuição de nulos por variável**\n%s", df_nulos)

def feature_engineering(df: pd.DataFrame) -> None:
    df['Age'] = 2025 - df['Year_Birth']
    df['Total_Children'] = df['Kidhome'] + df['Teenhome']
    df['Total_Spent'] = df[[
        'MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
    ]].sum(axis=1)
    df['Total_Purchases'] = df[[
        'NumDealsPurchases', 'NumWebPurchases',
        'NumCatalogPurchases', 'NumStorePurchases'
    ]].sum(axis=1)

    df['Online_Ratio'] = (df['NumWebPurchases'] + df['NumCatalogPurchases']) / (df['Total_Purchases'] + 1)
    df['Store_Ratio'] = df['NumStorePurchases'] / (df['Total_Purchases'] + 1)

    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')
    df['Customer_Tenure_Days'] = (datetime(2025, 8, 1) - df['Dt_Customer']).dt.days

    campanhas = [f'AcceptedCmp{i}' for i in range(1, 6)]
    df['Total_Accepted_Campaigns'] = df[campanhas].sum(axis=1)
    df['Campaign_Response_Flag'] = (df['Total_Accepted_Campaigns'] > 0).astype(int)

    logger.info("Feature engineering concluída.")

def clean_df(df: pd.DataFrame) -> Tuple[str, pd.DataFrame]:
    drop_cols = ['ID', 'Year_Birth', 'Kidhome', 'Teenhome', 'Dt_Customer', 'Z_CostContact', 'Z_Revenue']
    df_clean = df.drop(columns=drop_cols, errors="ignore")

    imputar = ['Income', 'Customer_Tenure_Days']
    for col in imputar:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

    relatorio = (
        f"\n[Limpeza de Dados]\n"
        f"- Colunas removidas: {drop_cols}\n"
        f"- Colunas imputadas com média: {imputar}\n"
        f"- Total de colunas após limpeza: {len(df_clean.columns)}"
    )
    logger.info(relatorio)

    return relatorio, df_clean

def normalizar_df(df: pd.DataFrame, categoricas: List[str] = None) -> pd.DataFrame:
    if categoricas is None:
        categoricas = ['Education', 'Marital_Status']

    df_numeric = df.drop(columns=categoricas, errors='ignore')
    numeric_cols = df_numeric.select_dtypes(include=['int64', 'float64']).columns.tolist()

    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numeric_cols] = scaler.fit_transform(df_scaled[numeric_cols])

    df_dummies = pd.get_dummies(df[categoricas], drop_first=True)
    df_cluster = pd.concat([df_scaled[numeric_cols], df_dummies], axis=1)

    logger.info("Normalização e encoding concluídos.")