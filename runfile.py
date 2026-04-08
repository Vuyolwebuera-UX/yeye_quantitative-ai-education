import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="AI Impact on Students", layout="wide")

st.title("📊 Impact of AI on Tertiary Education")
st.write("Exploratory Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Book1_Impact of AI Datatset.csv")
    return df

df = load_data()
df.columns = df.columns.str.strip()
# Sidebar filters
st.sidebar.header("Filter Data")

gender = st.sidebar.selectbox("Select Gender", ["All"] + list(df['Gender'].dropna().unique()))

if gender != "All":
    df = df[df['Gender'] == gender]

# Show dataset
st.subheader("Dataset Overview")
st.dataframe(df.head())

# --- SECTION 1: Missing Values ---
st.subheader("Missing Values")
missing = df.isnull().sum()
st.bar_chart(missing)

# --- SECTION 2: Distribution ---
st.subheader("Depression Score Distribution")

fig, ax = plt.subplots()
sns.histplot(df['todep'], kde=True, ax=ax)
st.pyplot(fig)

# --- SECTION 3: Anxiety vs Depression ---
st.subheader("Anxiety vs Depression")

fig, ax = plt.subplots()
sns.scatterplot(x=df['toas'], y=df['todep'], ax=ax)
ax.set_xlabel("Anxiety Score")
ax.set_ylabel("Depression Score")
st.pyplot(fig)

# --- SECTION 4: Social Support ---
st.subheader("Social Support Impact")

fig, ax = plt.subplots()
sns.boxplot(x=df['friends'], y=df['todep'], ax=ax)
st.pyplot(fig)

# --- SECTION 5: Internet Usage ---
st.subheader("Internet Usage vs Depression")

fig, ax = plt.subplots()
sns.boxplot(x=df['internet'], y=df['todep'], ax=ax)
st.pyplot(fig)

st.write("✅ Insights:")
st.write("- Higher anxiety is associated with higher depression levels")
st.write("- Social support appears to reduce depression")
st.write("- Internet usage may influence mental health trends")
