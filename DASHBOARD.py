import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Enquiries Dashboard For ELGI", page_icon="📊", layout="wide")
st.title("Companies Enquiries Dashboard")


df = pd.read_excel('/Users/Pranav/Documents/ELGi Website Entries 2024 (1).xlsx')
st.success("Excel file loaded successfully!")
st.write("### Data Preview:")
st.dataframe(df)


# remoing spaces and stuff to prevent later error while referencing to it
df.columns = df.columns.str.strip()

# ConvertingEntry Date to datetime
df['Entry Date'] = pd.to_datetime(df['Entry Date'], errors='coerce')

# kpi mais
st.markdown("### 🔢 Main metric Detals")
col1, col2, col3 = st.columns(3)
col1.metric("Total Enquiries", len(df))
col2.metric("Countries", df['Country'].nunique())
col3.metric("Top Equipment Type", df['Equipment Type'].mode(dropna=True)[0] if not df['Equipment Type'].isnull().all() else "N/A")



#this is basically reducing granularity adn grouping industries 
def group_industries(industry):
    if pd.isna(industry):
        return "Unknown"
    industry = industry.strip().lower()
    if industry in ['agri', 'agriculture','food','fmcg']:
        return 'Consumer Sector'
    elif industry in ['automobile','auto', 'vehicle']:
        return 'Automotive'
    elif industry in ['pharma ','healthcare','medical']:
        return 'Healthcare'
    else:
        return industry.title()  # default
df['Grouped Industry'] = df['Industry'].apply(group_industries)





# Side Filtering dropbox/lists
st.sidebar.header("📊 Filter Data")
selected_country = st.sidebar.multiselect("Country", df['Country'].dropna().unique())
selected_grouped = st.sidebar.multiselect("Grouped Industry", df['Grouped Industry'].dropna().unique())


min_date = df['Entry Date'].min()
max_date = df['Entry Date'].max()
start_date, end_date = st.sidebar.date_input("Filter by Entry Date Range", [min_date, max_date])

#filtered data 
filtered_df = df.copy()
if selected_country:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
if selected_grouped:
    filtered_df = filtered_df[filtered_df['Grouped Industry'].isin(selected_grouped)]


# to put the range of date u want to choose
filtered_df = filtered_df[
    (filtered_df['Entry Date'] >= pd.to_datetime(start_date)) &
    (filtered_df['Entry Date'] <= pd.to_datetime(end_date))
]


def topn(series, n=10):
    counts = series.value_counts()
    top_values = counts.nlargest(n)
    others = counts[n:].sum()
    
    #  the rest stuff will be under others
    top_series = top_values.append(pd.Series({'Others': others})) if others > 0 else top_values
    return top_series.reset_index().rename(columns={'index': series.name, 0: 'Count'})


# PIe chart for enquiries by Contry
st.subheader("🌍 Enquiries by Country")

if not filtered_df.empty and 'Country' in filtered_df.columns:
    # Get Top 20 countries
    country_counts = (
        filtered_df['Country']
        .value_counts()
        .head(20)
        .rename_axis('Country')        # Rename the index properly
        .reset_index(name='Count')     # Reset index and name column correctly
    )

    st.write(country_counts)  # Debug check

    fig_pie = px.pie(
        country_counts,
        names='Country',     # ← This column must exist, now it does!
        values='Count',
        title="Top 20 Countries by Enquiries",
        hole=0.3
    )

    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        showlegend=True,
        margin=dict(t=50, b=20, l=40, r=40)
    )

    st.plotly_chart(fig_pie, use_container_width=True)





# Equipment usage pi chart
if 'Equipment Type' in filtered_df.columns:
    st.subheader("⚙️ Equipment Type Distribution")
    eq_counts = filtered_df['Equipment Type'].value_counts().reset_index()
    eq_counts.columns = ['Equipment Type', 'Count']
    fig2 = px.pie(eq_counts, values='Count', names='Equipment Type', title="Equipment Interest")
    fig2.update_layout(
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig2, use_container_width=True, config={"responsive": True})


# Industry list and a bar chart of it
st.subheader("🏭 Industry Breakdown")
industry_counts = filtered_df['Grouped Industry'].value_counts().reset_index()
industry_counts.columns = ['Industry', 'Count']
fig3 = px.bar(industry_counts, x='Industry', y='Count', title="Industry-wise Enquiries")
fig3.update_layout(
    dragmode='zoom',
    hovermode='x',
    margin=dict(l=40, r=40, t=60, b=40)
)
st.plotly_chart(fig3, use_container_width=True, config={"responsive": True, "scrollZoom": True})


# choosing range of date u want written text
st.markdown(f"Showing enquiries from **{start_date}** to **{end_date}**")

# Monthhywise line graph
st.subheader("📅 Monthly Enquiry Trend")
if 'Entry Date' in filtered_df.columns:
    time_series = filtered_df.dropna(subset=['Entry Date'])
    time_series = time_series.groupby(time_series['Entry Date'].dt.to_period("M")).size().reset_index(name='Count')
    time_series['Entry Date'] = time_series['Entry Date'].dt.to_timestamp()
    fig4 = px.line(time_series, x='Entry Date', y='Count', title="Monthly Enquiries Over Time")
    fig4.update_layout(
        dragmode='zoom',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig4, use_container_width=True, config={"responsive": True, "scrollZoom": True})


# final filtered Data output
with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df)
