# ML Intake - Purchase Proposal

Projeto de ciência de dados e machine learning para clusterização de clientes com base em dados de campanhas de marketing.
O objetivo é identificar perfis de consumidores com diferentes níveis de propensão à conversão para otimizar ações comerciais e de marketing.

## 📂 Estrutura do Projeto

pipeline_cluster_processing/
│
├── scripts/
│ ├── main.py # Script principal que executa a pipeline completa
│ ├── logger.py # Configuração de logs
│ ├── preprocessing.py # Limpeza, engenharia de features e normalização
│ ├── pipeline.py # Orquestra a execução da pipeline
│ └── model.py # Lógica de modelagem e clusterização com KMeans
│
├── data_raw/ # Base de dados original (.csv)
├── data_processed/ # Dados finais com cluster atribuídos
├── pipeline_log.txt # Log da execução
└── README.md # Documentação do projeto


## Como executar

1. **Clone o repositório**
git clone https://github.com/luisfelipe-nomadlab/purchase_proposal.git
cd purchase_proposal

2. **Crie o ambiente virtual**
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. **Instale as dependencias**
pip install -r requirements.txt

4. **Execute**
python scripts/main.py

*O arquivo processado será salvo em data_processed/clientes_com_cluster.csv.*

## Funcionalidades
* Leitura e validação da base de dados
* Análise de composição e valores ausentes
* Engenharia de atributos (idade, gastos, perfil de compras, tempo como cliente etc.)
* Limpeza e padronização de dados
* Normalização de variáveis numéricas e encoding de categóricas
* Clusterização com KMeans
* Rotulagem dos perfis de clientes:
  * Alta Conversão
  * Média Conversão
  * Baixa Conversão

## Tecnologias utilizadas
* Python 3.10+
* pandas
* scikit-learn
* logging

## Resultados esperados
O script final gera um CSV com a segmentação dos clientes em clusters, auxiliando times de marketing e vendas a definirem estratégias personalizadas para cada grupo de consumidores.


