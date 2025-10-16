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
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Setup for a placeholder DataFrame (Replace with your actual data loading) ---
# Since I don't have access to 'arts_df', I'll create a synthetic one for the code to run.
# REPLACE THIS BLOCK with your actual data loading, e.g., arts_df = pd.read_csv('your_data.csv')

np.random.seed(42)
data_size = 200
arts_df = pd.DataFrame({
    'S.S.C (GPA)': np.random.uniform(3.5, 5.0, data_size).round(2),
    'H.S.C (GPA)': np.random.uniform(3.0, 5.0, data_size).round(2),
    'Did you ever attend a Coaching center?': np.random.choice(['Yes', 'No'], data_size, p=[0.6, 0.4]),
    'H.S.C or Equivalent study medium': np.random.choice(['Bangla', 'English', 'Other'], data_size, p=[0.75, 0.20, 0.05])
})
# Introduce some NaNs to simulate real data
arts_df.loc[arts_df.sample(frac=0.05).index, 'S.S.C (GPA)'] = np.nan
arts_df.loc[arts_df.sample(frac=0.03).index, 'H.S.C (GPA)'] = np.nan

# --- Streamlit Application ---

def run_arts_analysis():
    st.title("Arts Faculty Student Data Analysis 🎨")

    # Display a portion of the data
    st.header("Raw Data Snapshot")
    st.dataframe(arts_df.head())

    # ----------------------------------------------------------------------
    # 1. Scatter Plot: H.S.C (GPA) vs S.S.C (GPA)
    # ----------------------------------------------------------------------
    st.header("1. GPA Correlation: H.S.C vs S.S.C")

    # Select only the GPA columns and drop NaNs for the scatter plot
    gpa_df = arts_df[['S.S.C (GPA)', 'H.S.C (GPA)']].dropna()

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=gpa_df, x='S.S.C (GPA)', y='H.S.C (GPA)', ax=ax1)
    ax1.set_title('Scatter Plot of H.S.C (GPA) vs S.S.C (GPA)')
    ax1.set_xlabel('S.S.C (GPA)')
    ax1.set_ylabel('H.S.C (GPA)')
    ax1.grid(True)
    
    st.pyplot(fig1)
    st.markdown("This scatter plot helps visualize the **relationship between a student's S.S.C and H.S.C GPAs**.")

    st.markdown("---") # Separator

    # ----------------------------------------------------------------------
    # 2. Distribution of H.S.C (GPA)
    # ----------------------------------------------------------------------
    st.header("2. Distribution of H.S.C (GPA)")

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.hist(arts_df['H.S.C (GPA)'].dropna(), bins=20, color='lightcoral', edgecolor='black')
    ax2.set_title('Distribution of H.S.C (GPA) in Arts Faculty')
    ax2.set_xlabel('H.S.C (GPA)')
    ax2.set_ylabel('Frequency')
    ax2.grid(axis='y', alpha=0.75)
    
    st.pyplot(fig2)

    st.markdown("---") # Separator

    # ----------------------------------------------------------------------
    # 3. Distribution of S.S.C (GPA)
    # ----------------------------------------------------------------------
    st.header("3. Distribution of S.S.C (GPA)")

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.hist(arts_df['S.S.C (GPA)'].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax3.set_title('Distribution of S.S.C (GPA) in Arts Faculty')
    ax3.set_xlabel('S.S.C (GPA)')
    ax3.set_ylabel('Frequency')
    ax3.grid(axis='y', alpha=0.75)
    
    st.pyplot(fig3)

    st.markdown("---") # Separator

    # ----------------------------------------------------------------------
    # 4. Distribution of Coaching Center Attendance
    # ----------------------------------------------------------------------
    st.header("4. Coaching Center Attendance")

    coaching_counts = arts_df['Did you ever attend a Coaching center?'].value_counts()

    fig4, ax4 = plt.subplots(figsize=(8, 6))
    coaching_counts.plot(kind='barh', color='lightgreen', ax=ax4)
    ax4.set_title('Distribution of Students Who Attended a Coaching Center')
    ax4.set_xlabel('Count')
    ax4.set_ylabel('Attended Coaching Center')
    
    st.pyplot(fig4)

    st.markdown("---") # Separator

    # ----------------------------------------------------------------------
    # 5. Donut Chart: Study Medium
    # ----------------------------------------------------------------------
    st.header("5. H.S.C Study Medium Distribution")

    study_medium_counts = arts_df['H.S.C or Equivalent study medium'].value_counts()

    # Create a donut chart
    fig5, ax5 = plt.subplots(figsize=(8, 8))
    ax5.pie(
        study_medium_counts, 
        labels=study_medium_counts.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops=dict(width=0.3)
    )
    ax5.set_title('Distribution of Study Medium (H.S.C or Equivalent) in Arts Faculty')
    ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig5)

# Run the application
if __name__ == '__main__':
    run_arts_analysis()
