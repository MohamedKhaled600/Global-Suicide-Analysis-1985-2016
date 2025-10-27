
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide', page_title='Global Suicide Analysis 1985-2016')

html_title = """<h1 style="color:white;text-align:center;">Global Suicide Rates Analysis (1985-2016)</h1>"""
st.markdown(html_title, unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://www.corriestmedicalclinic.com.au/wp-content/uploads/2025/04/What-is-the-chronic-disease-management-plan.jpg' width='700'>
    </div>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv('cleaned_df.csv', index_col= 0)

page = st.sidebar.radio('Pages', ['Home', 'Global Trends', 'Country Analysis'])

if page == 'Home':
    st.subheader('Dataset Overview')
    st.dataframe(df)

    st.markdown("### 📘 Dataset Column Descriptions")

    st.markdown("""
    | **Column Name** | **Description** |
    |------------------|-----------------|
    | **country** | The name of the country where the data was collected. |
    | **year** | The year of observation (e.g., 1990, 2005). |
    | **sex** | The gender of the individuals in that group — usually **male** or **female**. |
    | **age** | The age group category (e.g., "15-24 years", "35-54 years"). |
    | **suicides_no** | The **total number of suicides** recorded for that demographic (country + year + sex + age). |
    | **population** | The **total population** size for that same group (country + year + sex + age). |
    | **suicides/100k pop** | The **suicide rate per 100,000 people** — a standardized measure that allows comparing countries with different population sizes. |
    | **country-year** | A combined field of `country` and `year` (e.g., "United States-2010"). It’s useful as a **unique identifier** for each year in each country. |
    | **HDI for year** | The **Human Development Index (HDI)** for that year — a measure of a country’s development based on life expectancy, education, and income (values usually between 0 and 1). |
    | **gdp_for_year ($)** | The **total Gross Domestic Product (GDP)** for that country in that year, measured in **U.S. dollars**. This represents the country’s overall economic activity. |
    | **gdp_per_capita ($)** | The **GDP per person**, calculated as total GDP divided by the population — shows **average income** per person in that country and year. |
    | **generation** | The **generation group** of the people in that record (e.g., “Generation X”, “Millennials”, “Silent Generation”). Derived from birth year and useful for generational analysis. |
    """)

elif page == 'Global Trends':
    st.header("🌍 Global Suicide Trends")
    
    # Basic statistics
    total_suicides = df['suicides_no'].sum()
    avg_rate = df['suicides_per_100k_pop'].mean()
    total_countries = df['country'].nunique()

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", f"{total_suicides:,}")
    col2.metric("Average Rate per 100k", f"{avg_rate:.2f}")
    col3.metric("Countries Covered", total_countries)

    st.markdown("---")

    st.subheader("📈 Time Series Analysis")
    # Global time trend
    yearly = df.groupby('year').agg({
        'suicides_no':'sum', 
        'suicides_per_100k_pop':'mean'
    }).reset_index()
    st.plotly_chart(px.line(yearly, 
                           x='year', 
                           y=['suicides_no','suicides_per_100k_pop'],
                           labels={'value':'Count / Rate','variable':'Metric'},
                           title='Global Trends Over Time', markers=True))
    
    st.markdown("---")

    st.subheader("👥 Demographics")
    # Gender distribution over time
    year_sex = df.groupby(['year','sex'], as_index=False).suicides_no.sum()
    st.plotly_chart(px.line(year_sex, 
                           x='year', 
                           y='suicides_no', 
                           color='sex',
                           title='Yearly Trends by Gender', markers=True))

    # Age groups analysis
    age_avg = df.groupby('age', as_index=False).suicides_per_100k_pop.mean().sort_values('suicides_per_100k_pop', ascending=False)
    st.plotly_chart(px.bar(age_avg, 
                          x='age', 
                          y='suicides_per_100k_pop',
                          text_auto='.2f',
                          title='Average Rate by Age Group',
                          color_discrete_sequence=['blue']))
    
    st.markdown("---")

    st.subheader("💰 Economic Indicators")
    # Income category analysis
    df_grouped = df.groupby('income_category')['suicides_per_100k_pop'].mean().reset_index()
    st.plotly_chart(px.bar(df_grouped,
                          x='income_category', 
                          y='suicides_per_100k_pop',
                          text_auto='.2f',
                          title='Average Rate by Income Category',
                          color_discrete_sequence=['blue']))
    
    # HDI correlation
    st.plotly_chart(px.scatter(df, 
                              x='hdi_for_year', 
                              y='suicides_per_100k_pop',
                              color='income_category',
                              title='Rate vs Human Development Index'))
    st.markdown("---")

    st.subheader("🌍 Geographic Distribution")
    # Top countries
    top_countries = df.groupby('country', as_index=False)['suicides_no'].sum().sort_values('suicides_no', ascending=False).head(10)
    st.plotly_chart(px.bar(top_countries, 
                          x='country', 
                          y='suicides_no',
                          text_auto='.2f',
                          title='Top 10 Countries by Total Cases',
                          color_discrete_sequence=['blue']))

elif page == 'Country Analysis':
    st.header("🗺️ Country-Level Analysis")

    # Country selector
    countries = sorted(df['country'].unique())
    selected_country = st.selectbox('Select a Country:', countries)

    # Filter data for selected country
    country_data = df[df['country'] == selected_country]

    # Basic country statistics
    total_cases = country_data['suicides_no'].sum()
    avg_rate = country_data['suicides_per_100k_pop'].mean()
    years_covered = country_data['year'].nunique()
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", f"{total_cases:,}")
    col2.metric("Average Rate per 100k", f"{avg_rate:.2f}")
    col3.metric("Years of Data", years_covered)
    
    st.markdown("---")

    # Time series for selected country
    yearly_country = country_data.groupby('year').agg({
        'suicides_no':'sum',
        'suicides_per_100k_pop':'mean'
    }).reset_index()
    
    st.plotly_chart(px.line(yearly_country,
                           x='year',
                           y=['suicides_no', 'suicides_per_100k_pop'],
                           title=f'Trends Over Time - {selected_country}', markers=True))

    # Demographics for selected country
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        gender_data = country_data.groupby('sex')['suicides_no'].sum()
        st.plotly_chart(px.pie(values=gender_data.values,
                              names=gender_data.index,
                              title='Cases by Gender'))
    
    with col2:
        st.subheader("Age Distribution")
        age_data = country_data.groupby('age')['suicides_no'].sum()
        st.plotly_chart(px.pie(values=age_data.values,
                              names=age_data.index,
                              title='Cases by Age Group'))
    
    # Economic indicators
    st.subheader("Economic Indicators")
    gdp_data = country_data.groupby('year').agg({
        'gdp_per_capita':'mean',
        'suicides_per_100k_pop':'mean'
    }).reset_index()
    
    st.plotly_chart(px.scatter(gdp_data,
                              x='gdp_per_capita',
                              y='suicides_per_100k_pop',
                              title='GDP per Capita vs Suicide Rate',
                              ))
