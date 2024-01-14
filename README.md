# InventoGPT: A Versatile Inventory Management and Analytics System

Welcome to the InventoGPT project repository, DODS_CyberCypher3.0. This comprehensive system is designed to streamline inventory management and provide valuable insights through various analytical tools. The project consists of several components, including data analysis, frequent itemset mining, association rule mining, and a user agent for real-time inventory monitoring.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Apriori Association Rules](#apriori-association-rules)
- [Detailed Apriori Analysis](#detailed-apriori-analysis)
- [Demand Forecasting](#demand-forecasting)
- [User Agent and Inventory Monitoring](#user-agent-and-inventory-monitoring)
- [File Descriptions](#file-descriptions)
- [Configuration](#configuration)

## Project Overview
InventoGPT is a powerful inventory management and analytics system that offers the following features:

- **Apriori Association Rules:** Identify frequently bought items together and association rules to optimize inventory and marketing strategies.
- **Detailed Apriori Analysis:** Perform in-depth analysis of specific items to understand their association rules.
- **Demand Forecasting:** Predict future demand for products based on historical data.
- **User Agent and Inventory Monitoring:** Real-time inventory monitoring and alerting system.

## Project Structure
The project is organized into the following directories and files:

- `apriori_page`: Contains the Streamlit app for Apriori Association Rules.
- `catboost_info`: Contains CatBoost model training information and error logs.
- `config.yaml`: Configuration file for user authentication.
- `data`: Contains sample data files.
- `pages`: Contains Streamlit apps for Demand Forecasting and Frequently Bought Items.
- `StreamlitWebApp`: Contains the Streamlit web app for user authentication and navigation.
- `uagent`: Contains the UserAgent and InventoryManagerAgent for real-time inventory monitoring.

## Getting Started
To run the project, follow these steps:

1. Clone the repository: `git clone https://github.com/DODS-CyberCypher3.0/InventoGPT.git`
2. Install required packages: `pip install -r requirements.txt`
3. Run the Streamlit web app: `streamlit run StreamlitWebApp/main.py`
4. Access the web app at [http://localhost:8501](http://localhost:8501)

## Apriori Association Rules
The Apriori Association Rules app allows users to upload a dataset containing transactions and identify frequently bought items together and association rules. The app provides a user-friendly interface for uploading data, viewing frequent items, and visualizing association rules.

## Detailed Apriori Analysis
The Detailed Apriori Analysis app enables users to perform in-depth analysis of specific items and their association rules. Users can select an item and view the association rules related to that item.

## Demand Forecasting
The Demand Forecasting app predicts future demand for products based on historical data. Users can upload a dataset containing product demand data and view the predicted demand for each product.

## User Agent and Inventory Monitoring
The UserAgent and InventoryManagerAgent provide real-time inventory monitoring and alerting capabilities. The UserAgent listens for incoming inventory alerts, while the InventoryManagerAgent periodically checks inventory levels and sends alerts when necessary.

## File Descriptions
- `apriori_page/new.py`: Streamlit app for Apriori Association Rules.
- `catboost_info/catboost_training.json`: CatBoost model training information.
- `catboost_info/learn_error.tsv`: CatBoost model learning error logs.
- `catboost_info/test_error.tsv`: CatBoost model testing error logs.
- `catboost_info/time_left.tsv`: CatBoost model time left logs.
- `config.yaml`: Configuration file for user authentication.
- `data/GroceryStoreDataSet_(1).csv`: Sample dataset for Apriori Association Rules.
- `data/groceries.csv`: Sample dataset for Demand Forecasting.
- `data/test.csv`: Sample dataset for Demand Forecasting.
- `data/train.csv`: Sample dataset for Demand Forecasting.
- `pages/1_Demand_Forecasting_🌎.py`: Streamlit app for Demand Forecasting.
- `pages/2_Frequently_Bought_Items_💸.py`: Streamlit app for Frequently Bought Items.
- `pages/3_Detailed_Analytics_🕵️.py`: Streamlit app for Detailed Apriori Analysis.
- `StreamlitWebApp/main.py`: Main Streamlit web app file.
- `StreamlitWebApp/Login.py`: User authentication for Streamlit web app.
- `uagent/InventoryManagerAgent.py`: InventoryManagerAgent for real-time inventory monitoring.
- `uagent/UserAgent.py`: UserAgent for real-time inventory monitoring.

## Configuration
- `config.yaml`: Configuration file for user authentication.
