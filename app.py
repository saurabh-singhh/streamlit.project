import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv("vgsales.csv")

df = pd.read_csv('vgsales.csv')
df['Publisher'].fillna("Unknown",inplace= True)

ts = df['Global_Sales'].sum()
tg = df.shape[0]
tp = len(df["Publisher"].unique())


# sidebar
st.sidebar.title("Sales Dashboard📊")
st.sidebar.markdown("---")
inp = st.sidebar.radio('Select',['Overview.',
        'Year wise Analyis.',
        'Genre wise Analysis.',
        'Platform wise Analysis.',
        'Publisher wise Analysis.'])

#overview

if inp == 'Overview.':
    st.title("Video Games Sales Analysis...🎮")
    st.markdown("---")

    col1,col2,col3 = st.columns([1,1,1])

    col1.metric("Total Sales.",value=ts,delta="+")
    col2.metric("Total Games Released.", value=tg, delta="+")
    col3.metric("Total Publishers.", value=tp, delta="+")

    st.markdown("---")

    st.image("games.png")
    st.markdown("""

    ---        
    #### *※ Columns in the data along with their description.*

    - `Rank:` The ranking position of the game in terms of global sales.
    - `Name:` The name of the video game.
    - `Platform:` The gaming platform (console or system) on which the game was released.
    - `Year:` The year when the game was released.
    - `Genre:` The genre or category of the game (e.g., action, adventure, sports).
    - `Publisher:` The company or entity responsible for publishing and distributing the game.
    - `NA_Sales:` Sales of the game in North America (in millions of units).
    - `EU_Sales:` Sales of the game in Europe (in millions of units).
    - `JP_Sales:` Sales of the game in Japan (in millions of units).
    - `Other_Sales:` Sales of the game in regions other than North America, Europe, and Japan (in millions of units).
    - `Global_Sales:` Total global sales of the game (sum of sales across all regions, in millions of units).
    ---
            """)
    
    st.header("Data.")
    st.dataframe(df)

    st.sidebar.markdown("---")
    games = df["Name"].unique()
    game = st.sidebar.selectbox('Select',games)

    temp = df[df['Name']== game]

    btn = st.sidebar.button("Click")

    st.markdown('---')
    if btn:
        st.header(f"Info of{game}")
        st.dataframe(temp)

elif inp == "Year wise Analyis.":
    st.title ("Year wise Analyis📅.")

    st.header ("Year wise sales")
    temp = df.groupby("Year")['Global_Sales'].sum().reset_index()
    fig = px.line(temp, x="Year" , y= "Global_Sales")
    st.plotly_chart(fig)

    st.header("Games Released Per Year.")
    temp = df['Year'].value_counts().sort_index()
    fig = px.bar(temp, x = temp.index, y= temp)
    st.plotly_chart(fig)

# Genre wise Analysis.
elif inp == 'Genre wise Analysis.':
    st.title('Genre wise Analysis🧿')

    # top genres based on GLoabal Sales
    st.header("Gloabal Sales in each genre.")
    temp = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    fig = px.bar(temp, x=temp.index, y=temp)
    st.plotly_chart(fig)

    temp = temp.reset_index()
    st.header("Contribution of each genre in sales.")
    fig = px.pie(temp, values='Global_Sales', names='Genre')
    st.plotly_chart(fig)

elif inp == 'Platform wise Analysis.':
    st.title("Platform wise Analysis.")

    st.markdown('---')
    st.header("Platform wise Analysis.")
    temp = df.groupby('Platform')["Global_Sales"].sum().sort_values()
    fig = px.bar(temp, x= temp.index, y= temp)
    st.plotly_chart(fig)

    st.header("Best selling Game at every platform")
    temp = (df.groupby('Platform').
            apply(lambda x: x.nlargest(1, 'Global_Sales')).
            reset_index(drop=True))
    st.dataframe(temp[["Platform",'Name']])

elif inp == 'Publisher wise Analysis.':
    st.title("Publisher wise Analysis.")

    st.header("Top 10 publishers by sales.")
    temp = (df.groupby("Publisher")['Global_Sales'].sum()
            .reset_index()
            .sort_values("Global_Sales", ascending=False)
            .head(10))

    fig = px.bar(temp, x='Publisher', y='Global_Sales')
    st.plotly_chart(fig)

    st.subheader("Contriution in Sales.")
    fig = px.pie(temp, values='Global_Sales', names='Publisher')
    st.plotly_chart(fig)

    st.subheader("Running Bar chart , Publisher and Sales.")
    df1 = df[df['Publisher'].isin(temp.Publisher.unique())]
    fig = px.bar(df1, x='Publisher', y='Global_Sales', animation_frame='Year', animation_group='Publisher', range_y=[0, 60])
    st.plotly_chart(fig)
