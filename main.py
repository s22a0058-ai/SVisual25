import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(
    page_title="Scientific Visualization" # Changed title here
)

st.header("Scientific Visualization", divider="gray")

# --- Page Configuration (Retaining the title change from the previous step) ---
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Faculty Data Analysis", divider="gray")
st.markdown("Analyzing gender distribution from the Arts Faculty dataset using Plotly for interactive visualization.")

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads the dataset from the specified GitHub URL."""
    url = 'https://raw.githubusercontent.com/s22a0058-ai/SVisual25/refs/heads/main/arts_faculty_data.csv'
    try:
        # Load data directly into a DataFrame
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data from URL: {e}")
        return pd.DataFrame()

df = load_data()

# Check if data loaded successfully
if df.empty:
    st.stop()

st.subheader("1. Raw Data Preview")
st.dataframe(df.head(), use_container_width=True)

# --- Data Processing ---
st.subheader("2. Gender Distribution Counts")

# Calculate gender counts. Using 'df' as the variable name instead of 'arts_df'
if 'Gender' in df.columns:
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    st.dataframe(gender_counts, use_container_width=True, hide_index=True)
else:
    st.error("The DataFrame must contain a column named 'Gender' for analysis.")
    st.stop()

# --- Plotly Visualization ---

st.subheader("3. Interactive Visualizations (Plotly)")

col1, col2 = st.columns(2)

# Plotly Pie Chart (in col1)
with col1:
    st.markdown("##### Pie Chart: Percentage Distribution")
    fig_pie = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='Distribution of Gender in Arts Faculty',
        color_discrete_sequence=['#3b82f6', '#f87171'] # Tailwind blue-500 and red-400
    )
    fig_pie.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=1.5)))
    st.plotly_chart(fig_pie, use_container_width=True)

# Plotly Bar Chart (in col2)
with col2:
    st.markdown("##### Bar Chart: Absolute Counts")
    fig_bar = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        title='Distribution of Gender in Arts Faculty',
        color='Gender',
        color_discrete_sequence=['#3b82f6', '#f87171'],
        text='Count'
    )
    fig_bar.update_layout(xaxis_title='Gender', yaxis_title='Count')
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- CSV Download (Streamlit style) ---
st.subheader("4. Download Data")

# Convert the DataFrame to CSV bytes in memory
csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Arts Faculty Data as CSV",
    data=csv_data,
    file_name='arts_faculty_data_analyzed.csv',
    mime='text/csv',
    help='Click here to download the original data file.'
)

st.markdown("""
<style>
/* Custom styling for better app aesthetics */
.stDownloadButton > button {
    background-color: #10b981; /* Emerald-500 */
    color: white;
    font-weight: bold;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    transition: all 0.2s;
}
.stDownloadButton > button:hover {
    background-color: #059669; /* Emerald-600 */
}
</style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd

# Assuming 'arts_df' is a pre-loaded DataFrame.
# For this Streamlit app to run, you need to replace this with your actual data loading.
# Example:
# @st.cache_data
# def load_data():
#     data = pd.read_csv('your_data.csv') # Replace with your file path
#     return data
# arts_df = load_data()

# --- Placeholder DataFrame for Demonstration ---
# In a real app, replace this with your actual arts_df loaded from a file/database.
data = {
    'H.S.C or Equivalent study medium': ['Bangla', 'English', 'Bangla', 'English', 'Bangla', 'English', 'Bangla', 'Bangla'],
    'Did you ever attend a Coaching center?': ['Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No'],
    'S.S.C (GPA)': [4.5, 5.0, 4.0, 4.8, 5.0, 4.2, 3.9, 4.7],
    'H.S.C (GPA)': [4.0, 4.8, 3.5, 4.5, 4.9, 4.0, 3.7, 4.6]
}
arts_df = pd.DataFrame(data)
# -----------------------------------------------

st.title("Arts Faculty Student Data Analysis")
st.markdown("---")

## 1. Distribution of Study Medium (H.S.C or Equivalent)
st.header("1. Distribution of Study Medium (H.S.C or Equivalent)")

if 'H.S.C or Equivalent study medium' in arts_df.columns:
    study_medium_counts = arts_df['H.S.C or Equivalent study medium'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        study_medium_counts,
        labels=study_medium_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.3)
    )
    ax.set_title('Distribution of Study Medium (H.S.C or Equivalent) in Arts Faculty')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
else:
    st.warning("Column 'H.S.C or Equivalent study medium' not found in the DataFrame.")

st.markdown("---")

## 2. Distribution of Students Who Attended a Coaching Center
st.header("2. Distribution of Students Who Attended a Coaching Center")

if 'Did you ever attend a Coaching center?' in arts_df.columns:
    coaching_counts = arts_df['Did you ever attend a Coaching center?'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    coaching_counts.plot(kind='barh', color='lightgreen', ax=ax)
    ax.set_title('Distribution of Students Who Attended a Coaching Center')
    ax.set_xlabel('Count')
    ax.set_ylabel('Attended Coaching Center')
    st.pyplot(fig)
else:
    st.warning("Column 'Did you ever attend a Coaching center?' not found in the DataFrame.")

st.markdown("---")

## 3. Distribution of S.S.C (GPA)
st.header("3. Distribution of S.S.C (GPA)")

if 'S.S.C (GPA)' in arts_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(
        arts_df['S.S.C (GPA)'].dropna(),
        bins=20,
        color='skyblue',
        edgecolor='black'
    )
    ax.set_title('Distribution of S.S.C (GPA) in Arts Faculty')
    ax.set_xlabel('S.S.C (GPA)')
    ax.set_ylabel('Frequency')
    ax.grid(axis='y', alpha=0.75)
    st.pyplot(fig)
else:
    st.warning("Column 'S.S.C (GPA)' not found in the DataFrame.")

st.markdown("---")

## 4. Distribution of H.S.C (GPA)
st.header("4. Distribution of H.S.C (GPA)")

if 'H.S.C (GPA)' in arts_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(
        arts_df['H.S.C (GPA)'].dropna(),
        bins=20,
        color='lightcoral',
        edgecolor='black'
    )
    ax.set_title('Distribution of H.S.C (GPA) in Arts Faculty')
    ax.set_xlabel('H.S.C (GPA)')
    ax.set_ylabel('Frequency')
    ax.grid(axis='y', alpha=0.75)
    st.pyplot(fig)
else:
    st.warning("Column 'H.S.C (GPA)' not found in the DataFrame.")

st.markdown("---")

## 5. Scatter Plot of H.S.C (GPA) vs S.S.C (GPA)
st.header("5. Scatter Plot of H.S.C (GPA) vs S.S.C (GPA)")

gpa_cols = ['S.S.C (GPA)', 'H.S.C (GPA)']

if all(col in arts_df.columns for col in gpa_cols):
    gpa_df = arts_df[gpa_cols].dropna()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=gpa_df,
        x='S.S.C (GPA)',
        y='H.S.C (GPA)',
        ax=ax # Pass the subplot axis to seaborn
    )
    ax.set_title('Scatter Plot of H.S.C (GPA) vs S.S.C (GPA)')
    ax.set_xlabel('S.S.C (GPA)')
    ax.set_ylabel('H.S.C (GPA)')
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning(f"One or more required GPA columns ({', '.join(gpa_cols)}) not found in the DataFrame.")
