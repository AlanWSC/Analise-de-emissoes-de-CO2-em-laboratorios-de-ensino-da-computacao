import streamlit as st
import plotly.express as px
import pandas as pd
import time

dados_labs_marco = pd.read_csv('Códigos/Dashboard/dados_labs_marco.csv')

st.title("Estimativas de CO₂ em Março")

with st.spinner("Carregando plots..."):
    time.sleep(2)
    st.success("Plots carregados com sucesso!")

col1, col2 = st.columns(2)

def emissao_lab(planilha):
    soma_emissao_lab = planilha.groupby('Laboratório')[planilha.columns[4:]].sum().sum(axis=1).reset_index()
    soma_emissao_lab.columns = ['Laboratórios', 'Emissão de Carbono']
    soma_emissao_lab = soma_emissao_lab.sort_values(by='Emissão de Carbono', ascending=False)

    barras_emissao_lab = px.bar(
        soma_emissao_lab.round(1),
        x='Laboratórios',
        y='Emissão de Carbono',
        title='Soma das emissões de CO₂ por laboratórios',
        labels={'Emissão de Carbono': 'Emissão de CO₂/Kg', 'Laboratórios': 'Laboratórios'},
        text_auto=True,
        color='Laboratórios',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    barras_emissao_lab.update_layout(
        xaxis_title='Laboratórios',
        yaxis_title='Emissão de CO₂/Kg',
        yaxis_range=[soma_emissao_lab['Emissão de Carbono'].min() * 0.9, soma_emissao_lab['Emissão de Carbono'].max() * 1.1],
        showlegend=False
    )

    col1.plotly_chart(barras_emissao_lab)

def emissao_horario(planilha):
    soma_emissao_horario = planilha.groupby('Horario Aula')[planilha.columns[4:]].sum().sum(axis = 1).reset_index()

    soma_emissao_horario.columns = ['Horario Aula', 'Emissão de Carbono'] 

    soma_emissao_horario = soma_emissao_horario.sort_values(by = 'Emissão de Carbono', ascending = False)

    barras_emissao_horario = px.bar(
        soma_emissao_horario.round(1),
        x = 'Horario Aula',
        y = 'Emissão de Carbono',
        title = 'Soma das emissões de CO₂ por horários de aulas',
        labels = {'Emissão de Carbono': 'Emissão de CO₂/Kg', 'Horario Aula': 'Horario Aula'},
        text_auto = True,  
        color = 'Horario Aula', color_discrete_sequence = px.colors.qualitative.Pastel
    )

    barras_emissao_horario.update_layout(
        xaxis_title = 'Horario Aula',
        yaxis_title = 'Emissão de CO₂/Kg',
        yaxis_range=[soma_emissao_horario['Emissão de Carbono'].min()* 0.9, soma_emissao_horario['Emissão de Carbono'].max() * 1],
        showlegend = False
    )

    col2.plotly_chart(barras_emissao_horario)

def emissao_media(planilha):
    media_aula_mes = planilha.groupby('Horario Aula')[planilha.columns[4:]].mean().reset_index() 

    media_aula_geral = media_aula_mes.melt(id_vars = ['Horario Aula'], var_name = 'Dia', value_name = 'Média de CO₂') 

    media_aula_geral['Dia'] = media_aula_geral['Dia'].astype('category')

    linhas_media = px.line(
        media_aula_geral.round(3),
        x = 'Dia',
        y = 'Média de CO₂',
        color = 'Horario Aula',
        title = 'Média das emissões de CO₂ por dias nos horários de aulas',
        labels = {'Média de CO₂': 'Média de CO₂/Kg', 'Dia': 'Dias'},
        markers = True, 
    )

    linhas_media.update_layout(
        xaxis_title = 'Dias',
        yaxis_title = 'Média de CO₂/Kg',
        legend_title = 'Aula',
    )
    
    linhas_media.update_xaxes(type='category')
    st.plotly_chart(linhas_media)

emissao_lab(dados_labs_marco)
emissao_horario(dados_labs_marco)
emissao_media(dados_labs_marco)
