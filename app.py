import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide', page_title='Dashboard')

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/skathirmani/datasets/refs/heads/main/odi-batting.csv'
    data = pd.read_csv(url)
    data['MatchDate'] = pd.to_datetime(data['MatchDate'], format='%m-%d-%Y')
    data['Year'] = data['MatchDate'].dt.year
    return data
data= load_data()
st.sidebar.header('Cricket Analysis')

#countries= ['India', 'Afghanistan', 'Australia']
countries= data['Country'].unique()
country_filter= st.sidebar.multiselect(
    label='Select one or more Country',
    options=countries
)


year_filter= st.sidebar.slider(
    label='Select a year',
    min_value=1971,
    max_value=2012,
    step=1
)
st.write(f'You have selected the country:{country_filter},type of this filter:{type(country_filter)}')
st.write(f'You have selected the year:{year_filter}')
#filtered_data= data[data['Country']== country_filter]
filtered_data= data[(data['Country'].isin (country_filter)) & (data['Year']== year_filter)]

#playerwise_total_runs = filtered_data.groupby(['Country','Player']).agg(TotalRuns=('Runs','sum')).reset_index()
#st.dataframe(filtered_data, use_container_width=True)
#playerwise_total_runs = playerwise_total_runs.sort_values(by='TotalRuns', ascending=False).head(10)


players_summary = filtered_data.groupby(['Country','Player']).agg(
  TotalRuns=('Runs', 'sum'),
  Centuries=('Runs', lambda v: sum(v>=100)),
  Fifties=('Runs', lambda v: sum((v>49) & (v<99))),
  Ducks=('Runs', lambda v: sum(v==0)),
  AvgRuns=('Runs', 'mean'),
  AvgStrikeRate=('ScoreRate', 'mean'),
).reset_index()


col1,col2 = st.columns(2)

with col1:
    st.header('Top 5 players by Total Runs')
    playerwise_total_runs_fig = px.bar(
        data_frame=players_summary.sort_values(by='TotalRuns', ascending=False).head(5),
        x='Player',
        y='TotalRuns'
    )
    st.plotly_chart(playerwise_total_runs_fig)

with col2:
    st.header('Top 5 players by Centuries')
    playerwise_totals_centuries_fig = px.bar(
        data_frame=players_summary.sort_values(by='Centuries', ascending=False).head(5),
        x='Player',
        y='Centuries'
    )
    st.plotly_chart(playerwise_totals_centuries_fig)
col3, col4 = st.columns(2)
with col3:
  st.header('Top 5 Players by Fifties')
  playerwise_fifties_fig = px.bar(
    data_frame=players_summary.sort_values(by='Fifties', ascending=False).head(5),
    x='Player',
    y='Fifties'
  )
  st.plotly_chart(playerwise_fifties_fig)

with col4:
  st.header('Top 5 Players by Average Runs')
  playerwise_avgruns_fig = px.bar(
    data_frame=players_summary.sort_values(by='AvgRuns', ascending=False).head(5),
    x='Player',
    y='AvgRuns'
  )
  st.plotly_chart(playerwise_avgruns_fig)


st.header('Filtered data')
st.dataframe(players_summary,use_container_width=True)


