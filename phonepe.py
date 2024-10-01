import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px

import requests
import json
mydb=psycopg2.connect(host="localhost",
                      port="5432",
                      database="postgres",
                      user="postgres",
                      password="1402"
                      )
cursor=mydb.cursor()

cursor.execute("SELECT  *FROM aggregated_insurance ")
mydb.commit()
table1=cursor.fetchall()

aggre_insurance=pd.DataFrame(table1, columns=("states" ,"years","Quarter","Transaction_type",
                                                         "Transaction_count","Transaction_amount"))


cursor.execute("SELECT  *FROM aggregated_transaction ")
mydb.commit()
table2=cursor.fetchall()

aggre_transaction=pd.DataFrame(table2, columns=("states","years","Quarter","Transaction_type",
                                                         "Transaction_count","Transaction_amount"))


cursor.execute("SELECT  *FROM aggregated_user ")
mydb.commit()
table3=cursor.fetchall()

aggre_user=pd.DataFrame(table3, columns=("states","years","Quarter","Brands",
                                                         "Transaction_count","percentage"))


cursor.execute("SELECT  *FROM map_insurance ")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("states","years","Quarter","District",
                                                         "Transaction_count","Transaction_amount"))
cursor.execute("SELECT  *FROM map_transaction ")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("states","years","Quarter","District",
                                                         "Transaction_count","Transaction_amount"))


cursor.execute("SELECT  *FROM map_user ")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("states","years","Quarter","District",
                                                         "RegisteredUser","AppOpens"))


cursor.execute("SELECT  *FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insur=pd.DataFrame(table7,columns=("states","years","Quarter","pincodes",
                                                         "Transaction_count","Transaction_amount"))


cursor.execute("SELECT  *FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_trans=pd.DataFrame(table8,columns=("states","years","Quarter","pincodes",
                                                         "Transaction_count","Transaction_amount"))


cursor.execute("SELECT  *FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("states","years","Quarter","pincodes",
                                                         "registeredUsers"))

def transaction_count_amount_y(df,year):
    tacy=df[df["years"] == year]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("states")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig_amount=px.bar(tacyg,x="states",y="Transaction_amount",title="TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=650)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyg,x="states",y="Transaction_count",title="TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=650)
        st.plotly_chart(fig_count)


    
    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
    
        
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="states",title="f{year} TRANSACTION_AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)


    with col2:    


        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="states",title="f{year} TRANSACTION_count",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def transaction_count_amount_y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("states")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2= st.columns(2)
    with col1:

            fig_amount=px.bar(tacyg,x="states",y="Transaction_amount",title=f"{tacy["years"].unique()} YEAR{quarter} TRANSACTION AMOUNT",
                              color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=650)
            st.plotly_chart(fig_amount)
    with col2:                

        fig_count=px.bar(tacyg,x="states",y="Transaction_count",title=f"{tacy["years"].unique()} YEAR{quarter}TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=650)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:
    
                
            url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response=requests.get(url)
            data1=json.loads(response.content)
            data1
            states_name=[]
            for feature in data1["features"]:
                states_name.append(feature["properties"]["ST_NM"])

            states_name.sort()
            
            fig_india_1=px.choropleth(tacyg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name="states",title=f"{tacy["years"].unique()} YEAR{quarter} TRANSACTION_AMOUNT",fitbounds="locations",
                                    height=650,width=650)
            fig_india_1.update_geos(visible=False)
            st.plotly_chart(fig_india_1)
    with col2:        

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="states",title=f"{tacy["years"].unique()} YEAR{quarter} TRANSACTION_count",fitbounds="locations",
                                height=650,width=650)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)


def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["states"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)



def Aggre_user_plot_1(df, year):
    aguy= df[df["years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy



def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


def Aggre_user_plot_3(df, state):
    auyqs= df[df["states"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


def Map_insur_District(df, state):

    tacy= df[df["states"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    col1,col2= st.columns(2)
    with col1:


        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 400,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 400,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


def map_user_plot_1(df, year):
    muy= df[df["years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("states")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "states", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("states")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "states", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

def map_user_plot_3(df, states):
    muyqs= df[df["states"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 400, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 400, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

def Top_insurance_plot_1(df, state):
    tiy= df[df["states"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)
def top_user_plot_1(df, year):
    tuy= df[df["years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["states", "Quarter"])["registeredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "states", y= "registeredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "states",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    pass

elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])


        if method=="Insurance Analysis":

             col1,col2= st.columns(2)
             with col1:

                years= st.slider("Select The Year",aggre_insurance["years"].min(), aggre_insurance["years"].max(),aggre_insurance["years"].min())
                tac_Y= transaction_count_amount_y(aggre_insurance, years)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter",tac_Y["Quarter"].min(), tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
                transaction_count_amount_y_Q(tac_Y, quarters)



        elif method=="Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggre_transaction["years"].min(), aggre_transaction["years"].max(),aggre_transaction["years"].min())
                Aggre_tran_tac_y=transaction_count_amount_y(aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("select the state",Aggre_tran_tac_y["states"].unique())
                Aggre_Tran_Transaction_type(Aggre_tran_tac_y,states)
            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter",Aggre_tran_tac_y["Quarter"].min(), Aggre_tran_tac_y["Quarter"].max(),Aggre_tran_tac_y["Quarter"].min())
                    Aggre_tran_tac_Y_Q=transaction_count_amount_y_Q(Aggre_tran_tac_y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_Yt",Aggre_tran_tac_Y_Q["states"].unique())
                Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)
            

    

            
        elif method=="User Analysis":
                col1,col2= st.columns(2)
                with col1:

                  years= st.slider("Select The Year",aggre_user["years"].min(), aggre_user["years"].max(),aggre_user["years"].min())
                  Aggre_user_Y=Aggre_user_plot_1(aggre_user, years)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
                    Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

                col1,col2= st.columns(2)
                with col1:
                 states= st.selectbox("Select The State", Aggre_user_Y_Q["states"].unique())

                 Aggre_user_plot_3(Aggre_user_Y_Q, states)


    with tab2:

        method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2=="Map Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_insurance["years"].min(), map_insurance["years"].max(),map_insurance["years"].min())
                Map_insur_tac_Y=transaction_count_amount_y(map_insurance, years)
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_mi",Map_insur_tac_Y["states"].unique())
                Map_insur_District(Map_insur_tac_Y,states)

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mi",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
                    map_insur_tac_Y_Q=transaction_count_amount_y_Q(Map_insur_tac_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_m",Map_insur_tac_Y["states"].unique())
                Map_insur_District(Map_insur_tac_Y,states)

                            

        elif method_2=="Map Transaction":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mtr",map_transaction["years"].min(), map_transaction["years"].max(),map_transaction["years"].min())
                Map_tran_tac_Y=transaction_count_amount_y(map_transaction, years)
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_mtr",Map_tran_tac_Y["states"].unique())
                Map_insur_District(Map_tran_tac_Y,states)

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mt",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
                    Map_tran_tac_Y_Q=transaction_count_amount_y_Q(Map_tran_tac_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_mt",Map_tran_tac_Y["states"].unique())
                Map_insur_District(Map_tran_tac_Y,states)

        elif method_2=="Map User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mtr",map_user["years"].min(), map_user["years"].max(),map_user["years"].min())
                Map_user_Y=map_user_plot_1(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mt",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
                    Map_user_Y_Q=map_user_plot_2(Map_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                 states= st.selectbox("Select The State_mu", Map_user_Y_Q["states"].unique())

                 map_user_plot_3(Map_user_Y_Q, states)

    with tab3:

        method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3=="Top Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_Ti",top_insur["years"].min(), top_insur["years"].max(),top_insur["years"].min())
                Top_insur_tac_Y=transaction_count_amount_y(top_insur, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_ti",Top_insur_tac_Y["states"].unique())
            

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_t",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
                    Top_insur_tac_Y_Q=transaction_count_amount_y_Q(Top_insur_tac_Y, quarters)



        elif method_3=="Top Transaction":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_Tt",top_trans["years"].min(), top_trans["years"].max(),top_trans["years"].min())
                Top_tran_tac_Y=transaction_count_amount_y(top_trans, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_tT",Top_tran_tac_Y["states"].unique())
            

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_tt",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
                    Top_tran_tac_Y_Q=transaction_count_amount_y_Q(Top_tran_tac_Y, quarters)

        elif method_3=="Top User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_Tt",top_trans["years"].min(), top_trans["years"].max(),top_trans["years"].min())
                Top_tran_tac_Y=transaction_count_amount_y(top_trans, years)
elif select=="TOP CHARTS":
    pass
