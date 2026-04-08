import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# PAGE CONFIG + STYLE
# =============================
st.set_page_config(
    page_title="AI Impact Dashboard",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    df = pd.read_excel("AI_Education_MockDataset.xlsx")
    df.columns = df.columns.str.strip()  # clean column names
    return df

df = load_data()

# Debug view (you can remove later)
st.write("📌 Columns in dataset:", df.columns)

# =============================
# TITLE
# =============================
st.title("📊 Impact of AI on Tertiary Education")
st.write("Exploratory Data Analysis Dashboard")

st.markdown("---")

# =============================
# SIDEBAR FILTERS
# =============================
st.sidebar.header("🔎 Filters")

# Safe column checks (prevents errors)
if 'gender' in df.columns:
    gender_options = ["All"] + list(df['gender'].dropna().unique())
    gender = st.sidebar.selectbox("Gender", gender_options)

    if gender != "All":
        df = df[df['gender'] == gender]

if 'age' in df.columns:
    min_age = int(df['age'].min())
    max_age = int(df['age'].max())

    age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))
    df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]

# =============================
# KPI METRICS
# =============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    if 'todep' in df.columns:
        st.metric("Avg Depression", round(df['todep'].mean(), 2))

with col3:
    if 'toas' in df.columns:
        st.metric("Avg Anxiety", round(df['toas'].mean(), 2))

st.markdown("---")

# =============================
# DATA PREVIEW
# =============================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

# =============================
# VISUALS
# =============================
st.subheader("📊 Analysis")

col1, col2 = st.columns(2)

# --- Histogram ---
with col1:
    if 'todep' in df.columns:
        st.write("📉 Depression Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['todep'], kde=True, ax=ax)
        st.pyplot(fig)

# --- Scatter Plot ---
with col2:
    if 'toas' in df.columns and 'todep' in df.columns:
        st.write("📈 Anxiety vs Depression")
        fig, ax = plt.subplots()
        sns.scatterplot(x=df['toas'], y=df['todep'], ax=ax)
        ax.set_xlabel("Anxiety")
        ax.set_ylabel("Depression")
        st.pyplot(fig)

st.markdown("---")

# =============================
# SOCIAL / SUPPORT ANALYSIS
# =============================
if 'friends' in df.columns and 'todep' in df.columns:
    st.subheader("👥 Social Support Impact")

    fig, ax = plt.subplots()
    sns.boxplot(x=df['friends'], y=df['todep'], ax=ax)
    st.pyplot(fig)

st.markdown("---")

# =============================
# INTERNET USAGE
# =============================
if 'internet' in df.columns and 'todep' in df.columns:
    st.subheader("🌐 Internet Usage vs Depression")

    fig, ax = plt.subplots()
    sns.boxplot(x=df['internet'], y=df['todep'], ax=ax)
    st.pyplot(fig)

st.markdown("---")

# =============================
# CORRELATION HEATMAP
# =============================
st.subheader("🔥 Correlation Matrix")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

# =============================
# INSIGHTS
# =============================
st.subheader("🧠 Key Insights")

st.write("""
- Higher anxiety levels are associated with higher depression scores.
- Social support (friends) appears to influence mental health outcomes.
- Internet usage may play a role in student well-being.
""")
