import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("Apriori Association Rules : Frequently Bought Items using Apriori Algorithm 🍲")

# File Upload
uploaded_file = st.file_uploader("Choose a file", type=["xls", "xlsx", "csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Check file type
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension in ["xls", "xlsx"]:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
    elif file_extension == "csv":
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload an Excel (xls, xlsx) or CSV file.")
        st.stop()

    # Show the uploaded data
    st.write("Uploaded Data:")
    st.write(df)

    # Preprocess the data
    te = TransactionEncoder()
    te_data = te.fit(df.values).transform(df.values)
    df_encoded = pd.DataFrame(te_data, columns=te.columns_)

    # Apriori function
    frequent_items = apriori(df_encoded, min_support=0.1, use_colnames=True)

    # Show frequent items
    st.write("Frequently Bought Together:")
    for itemset in frequent_items['itemsets']:
        st.write(', '.join(itemset))

    # Bar plot of top 10 frequent items
    top_items = frequent_items.sort_values(by="support", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="support", y="itemsets", data=top_items)
    plt.title("Top 10 Frequent Items Bought Together")
    plt.xlabel("Support")
    plt.ylabel("Itemsets")
    st.pyplot(plt)

    # Association Rules
    rules = association_rules(frequent_items, metric="confidence", min_threshold=0.5)

    # Show Association Rules
    st.write("Association Rules: Frequently Bought Items using Apriori Algorithm")
    st.write(rules)

    # Bar plot of association rules
    filtered_rules = rules[(rules["support"] > 0.15) & (rules["confidence"] > 0.5)]
    plt.figure(figsize=(10, 6))
    sns.barplot(x="confidence", y="antecedents", data=filtered_rules.sort_values(by="confidence", ascending=False))
    plt.title("Association Rules with Support > 0.15 and Confidence > 0.5")
    plt.xlabel("Confidence")
    plt.ylabel("Antecedents")
    st.pyplot(plt)
