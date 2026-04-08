import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config (MUST be at the top)
st.set_page_config(page_title="AI Impact on Students", layout="wide")

# Load data FIRST
@st.cache_data
def load_data():
    df = pd.read_csv("Book1_Impact of AI Datatset.csv")
    return df

df = load_data()

# Clean column names
df.columns = df.columns.str.strip()

# Debug
st.write("Columns in dataset:", df.columns)

st.title("📊 Impact of AI on Tertiary Education")
st.write("Exploratory Data Analysis Dashboard")

# Sidebar
st.sidebar.header("Filter Data")

# Safe check
if 'Gender' in df.columns:
    gender = st.sidebar.selectbox("Select Gender", ["All"] + list(df['Gender'].dropna().unique()))

    if gender != "All":
        df = df[df['Gender'] == gender]
else:
    st.warning("⚠️ 'Gender' column not found")

# Show dataset
st.subheader("Dataset Overview")
st.dataframe(df.head())

# Missing values
st.subheader("Missing Values")
st.bar_chart(df.isnull().sum())

# Distribution
st.subheader("Depression Score Distribution")
fig, ax = plt.subplots()
sns.histplot(df['todep'], kde=True, ax=ax)
st.pyplot(fig)

# Scatter plot
st.subheader("Anxiety vs Depression")
fig, ax = plt.subplots()
sns.scatterplot(x=df['toas'], y=df['todep'], ax=ax)
st.pyplot(fig)

# Social support
st.subheader("Social Support Impact")
fig, ax = plt.subplots()
sns.boxplot(x=df['friends'], y=df['todep'], ax=ax)
st.pyplot(fig)

# Internet
st.subheader("Internet Usage vs Depression")
fig, ax = plt.subplots()
sns.boxplot(x=df['internet'], y=df['todep'], ax=ax)
st.pyplot(fig)

st.write("✅ Insights:")
st.write("- Higher anxiety is associated with higher depression levels")
st.write("- Social support appears to reduce depression")
st.write("- Internet usage may influence mental health trends")
