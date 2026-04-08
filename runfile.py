import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="AI Impact Dashboard",
    layout="wide"
)

# =============================
# STYLE (LIGHT + CLEAN)
# =============================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}

h1 {
    color: #2E86C1;
}

h2, h3 {
    color: #1F618D;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    df = pd.read_excel("AI_Education_MockDataset.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Debug (REMOVE later if you want)
st.write("📌 Columns in dataset:", df.columns)

# =============================
# TITLE
# =============================
st.title("📊 AI Impact on Tertiary Education")
st.write("Interactive Data Analysis Dashboard")

st.markdown("---")

# =============================
# SIDEBAR FILTERS
# =============================
st.sidebar.header("🔎 Filters")

# Gender filter (safe)
if 'gender' in df.columns:
    gender_options = ["All"] + list(df['gender'].dropna().unique())
    gender = st.sidebar.selectbox("Gender", gender_options)

    if gender != "All":
        df = df[df['gender'] == gender]

# Age filter (safe)
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
    st.metric("📊 Total Records", len(df))

with col2:
    if 'todep' in df.columns:
        st.metric("😔 Avg Depression", round(df['todep'].mean(), 2))

with col3:
    if 'toas' in df.columns:
        st.metric("😰 Avg Anxiety", round(df['toas'].mean(), 2))

st.markdown("---")

# =============================
# DATA PREVIEW
# =============================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

# =============================
# CHART STYLE
# =============================
sns.set_style("whitegrid")

# =============================
# VISUALS
# =============================
st.subheader("📊 Analysis")

col1, col2 = st.columns(2)

# Histogram
with col1:
    if 'todep' in df.columns:
        st.write("📉 Depression Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['todep'], kde=True, color="#3498db", ax=ax)
        st.pyplot(fig)

# Scatter
with col2:
    if 'toas' in df.columns and 'todep' in df.columns:
        st.write("📈 Anxiety vs Depression")
        fig, ax = plt.subplots()
        sns.scatterplot(x=df['toas'], y=df['todep'], color="#e74c3c", ax=ax)
        ax.set_xlabel("Anxiety")
        ax.set_ylabel("Depression")
        st.pyplot(fig)

st.markdown("---")

# =============================
# SOCIAL SUPPORT
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
# CORRELATION
# =============================
st.subheader("🔥 Correlation Analysis")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

# =============================
# INSIGHTS
# =============================
st.subheader("🧠 Key Insights")

st.write("""
- Higher anxiety is linked to higher depression.
- Social support can influence mental health.
- Internet usage may affect student well-being.
""")
