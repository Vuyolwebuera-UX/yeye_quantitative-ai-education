import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config (MUST be first)
st.set_page_config(page_title="AI Education EDA", layout="wide")

st.title("📊 Impact of AI on Tertiary Education")
st.write("Exploratory Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("AI_Education_MockDataset.xlsx")
    return df

df = load_data()

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Debug: show columns
st.subheader("📋 Columns in Dataset")
st.write(df.columns)

# Dataset preview
st.subheader("📌 Data Preview")
st.dataframe(df.head())

# Sidebar
st.sidebar.header("Filters")

# Example filter (only if column exists)
if 'gender' in df.columns:
    gender = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + list(df['gender'].dropna().unique())
    )

    if gender != "All":
        df = df[df['gender'] == gender]

# Missing values
st.subheader("❗ Missing Values")
st.bar_chart(df.isnull().sum())

# Summary stats
st.subheader("📈 Summary Statistics")
st.dataframe(df.describe())

# Correlation heatmap
st.subheader("🔥 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Distribution plot
st.subheader("📊 Distribution")

numeric_cols = df.select_dtypes(include='number').columns

if len(numeric_cols) > 0:
    selected_col = st.selectbox("Select variable", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_col].dropna(), kde=True, ax=ax)
    st.pyplot(fig)
else:
    st.warning("No numeric columns found")
