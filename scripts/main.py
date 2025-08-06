# scripts/main.py

from scripts.pipeline import pipeline_clusterizacao
from scripts.logger import logger

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    path_raw = "/home/felipe/pipeline_cluster_processing/data_raw/marketing_campaign.csv"  
    path_processed = "data_processed/clientes_com_cluster.csv"

    logger.info("Iniciando pipeline de clusterização...")
    pipeline_clusterizacao(path_raw, path_processed)
    logger.info("Pipeline finalizado com sucesso.")
