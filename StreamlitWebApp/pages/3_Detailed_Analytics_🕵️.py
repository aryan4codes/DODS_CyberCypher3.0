import streamlit as st
import pandas as pd
from io import StringIO
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import itertools

# Load the grocery dataset
data = """JAM,MAGGI,BREAD,MILK
MAGGI,TEA,BISCUIT
BREAD,TEA,BOURNVITA
MAGGI,TEA,CORNFLAKES
MAGGI,BREAD,TEA,BISCUIT
JAM,MAGGI,BREAD,TEA
BREAD,MILK
COFFEE,CHICKEN,BISCUIT,CORNFLAKES
COFFEE,CHICKEN,BISCUIT,CORNFLAKES
COFFEE,SUGER,BOURNVITA
BREAD,COFFEE,CHICKEN
BREAD,SUGER,BISCUIT
COFFEE,SUGER,CORNFLAKES
BREAD,SUGER,BOURNVITA
BREAD,COFFEE,SUGER
BREAD,COFFEE,SUGER
TEA,MILK,COFFEE,CORNFLAKES
"""

df = pd.read_csv(StringIO(data), header=None)

# Convert all values to strings
df = df.applymap(str)

# Preprocess the data
te = TransactionEncoder()
te_data = te.fit(df.values).transform(df.values)
df_encoded = pd.DataFrame(te_data, columns=te.columns_)

# Apriori function
def run_apriori(data, min_support=0.1, min_confidence=0.5):
    frequent_items = apriori(data, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_items, metric="confidence", min_threshold=min_confidence)
    return frequent_items, rules

# Streamlit app
st.title("Detailed Apriori Analysis 🕵️")

# User input for item selection
selected_item = st.selectbox("Select an item to check for association rules", df.columns)+1

# Get frequent items and association rules
frequent_items, rules = run_apriori(df_encoded)

# Display frequent items
st.subheader("Frequent Items")
st.write(frequent_items)

# Display association rules
st.subheader("Association Rules")
st.write(rules)

# Display association rules for the selected item
st.subheader(f"Association Rules for {selected_item} column")
filtered_rules = rules[rules["consequents"].apply(lambda x: selected_item in x)]
st.write(filtered_rules)
