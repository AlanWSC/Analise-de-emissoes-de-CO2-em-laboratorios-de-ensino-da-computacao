import streamlit as st
import plotly.express as px
import pandas as pd
import time
from datetime import date

dados_finais = pd.read_csv('D:/Backup - Dev/Artigo/Códigos TCC/Nova planilha concatenada e códigos/dados_finais.csv')

st.title("Estimativas de CO₂ Totais")

with st.spinner("Carregando plots..."):
    time.sleep(2)
    st.success("Plots carregados com sucesso!")

colunas_dias = [col for col in dados_finais.columns if col.isdigit()] 
ordem_dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'] 

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

def obter_dia_e_mes(dia, mes):
    DIAS = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-feira',
        'Sexta-feira'
    ]
    MESES = ['Março', 'Abril', 'Maio', 'Junho']
    
    try:
        data = date(2024, mes, dia)
        nome_dia_semana = DIAS[data.weekday()]
        nome_mes = MESES[mes - 3]
        return nome_dia_semana, nome_mes
    except ValueError:
        return None, None 

def emissoes_lab(planilha):
    
    emissao_lab = planilha.groupby('Laboratório')[planilha.columns[4:]].sum().sum(axis = 1).reset_index() 

    emissao_lab.columns = ['Laboratórios', 'Emissão de Carbono']

    emissao_lab = emissao_lab.sort_values(by = 'Emissão de Carbono', ascending = False)

    barras_emissao_lab = px.bar( 
        emissao_lab.round(1),
        x = 'Laboratórios',
        y = 'Emissão de Carbono',
        title = 'Soma de emissões de CO₂ por laboratórios',
        labels = {'Emissão de Carbono' : 'Emissão de CO₂/Kg', 'Laboratórios' : 'Laboratórios'},
        text_auto = True,  
        color = 'Laboratórios', color_discrete_sequence = px.colors.qualitative.Pastel
    )

    barras_emissao_lab.update_layout(
        xaxis_title = 'Laboratórios',
        yaxis_title = 'Emissão de CO₂/Kg',
        yaxis_range=[emissao_lab['Emissão de Carbono'].min()* 0.9, emissao_lab['Emissão de Carbono'].max() * 1],
        showlegend = False
    )

    col1.plotly_chart(barras_emissao_lab)

def emissoes_horario(planilha):
    
    emissao_lab = dados_finais.groupby('Horario Aula')[dados_finais.columns[4:]].sum().sum(axis = 1).reset_index() 

    emissao_lab.columns = ['Horario Aula', 'Emissão de Carbono'] 

    emissao_lab = emissao_lab.sort_values(by = 'Emissão de Carbono', ascending = False)

    barras_emissao_lab = px.bar( 
        emissao_lab.round(1),
        x = 'Horario Aula',
        y = 'Emissão de Carbono',
        title = 'Soma de emissões de CO₂ por horários de aulas',
        labels = {'Emissão de Carbono' : 'Emissão de CO₂/Kg', 'Horario Aula' : 'Horario Aula'},
        text_auto = True,  
        color = 'Horario Aula', color_discrete_sequence = px.colors.qualitative.Pastel
    )

    barras_emissao_lab.update_layout(
        xaxis_title = 'Horario Aula',
        yaxis_title = 'Emissão de CO₂/Kg',
        yaxis_range=[emissao_lab['Emissão de Carbono'].min()* 0.9, emissao_lab['Emissão de Carbono'].max() * 1],
        showlegend = False
    )

    col2.plotly_chart(barras_emissao_lab)

def media_mes(planilha):

    media_por_mes = planilha.groupby('Mês')[planilha.columns[4:]].mean().reset_index()
    media_por_mes_long = media_por_mes.melt(id_vars=['Mês'], var_name='Dia', value_name='Média de CO₂')
    media_por_mes_long = media_por_mes_long.dropna()
    media_por_mes_long['Dia'] = pd.to_numeric(media_por_mes_long['Dia'], errors='coerce')

    # Cria o gráfico de linha
    linhas_media_aula = px.line(
        media_por_mes_long.round(3),
        x='Dia',
        y='Média de CO₂',
        color='Mês',
        title='Média de emissão de CO₂ por dias nos meses',
        labels={'Média de CO₂': 'Média de CO₂/Kg', 'Dia': 'Dias'},
        markers=True, 
    )

    linhas_media_aula.update_layout(
        xaxis_title='Dias',
        yaxis_title='Média de CO₂/Kg',
        legend_title='Mês',
        xaxis = dict(dtick = 1)
    )
    st.plotly_chart(linhas_media_aula)

def soma_emissoes_meses(planilha):

    emissao_lab = planilha.groupby('Mês')[planilha.columns[4:]].sum().sum(axis = 1).reset_index() 
    emissao_lab.columns = ['Mês', 'Emissão de Carbono'] 
    emissao_lab = emissao_lab.sort_values(by = 'Emissão de Carbono', ascending = False) 

    barras_emissao_lab = px.bar( 
        emissao_lab.round(1),
        x = 'Mês',
        y = 'Emissão de Carbono',
        title = 'Soma de emissões de CO₂ por meses',
        labels = {'Emissão de Carbono' : 'Emissão de CO₂/Kg', 'Meses' : 'Meses'},
        text_auto = True,  
        color = 'Mês', color_discrete_sequence = px.colors.qualitative.Pastel
    )

    # Ajustes para melhor visualização do plot
    barras_emissao_lab.update_layout(
        xaxis_title = 'Mês',
        yaxis_title = 'Emissão de CO₂/Kg',
        yaxis_range=[emissao_lab['Emissão de Carbono'].min()* 0.9, emissao_lab['Emissão de Carbono'].max() * 1],
        showlegend = False
    )

    col3.plotly_chart(barras_emissao_lab)

def soma_emissoes_semana(planilha):
    # Transforma as colunas de dias em linhas, criando as colunas 'Dia' e 'Emissão'
    soma_emissao_semana = (
        dados_finais.melt(
            id_vars=['Mês'],
            value_vars=colunas_dias,
            var_name='Dia',
            value_name='Emissão'
        )
        .dropna(subset=['Emissão'])  # Remove valores NaN da coluna de emissões
    )

    soma_emissao_semana['Dia'] = soma_emissao_semana['Dia'].astype(int)     # Converte as colunas para inteiro antes de mapear

    # Aplica a função para obter o dia da semana e o mês corretamente
    soma_emissao_semana[['Dia da Semana', 'Mês']] = soma_emissao_semana.apply(
        lambda row: pd.Series(obter_dia_e_mes(row['Dia'], {'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6}[row['Mês']])),
        axis=1
    )

    # Agrupa os dados pela coluna 'Dia da Semana' e soma as emissões
    soma_emissao_semana = (
        soma_emissao_semana
        .groupby('Dia da Semana', as_index=False)
        .agg(Soma_Emissoes =('Emissão', 'sum'))
    )

    soma_emissao_semana['Dia da Semana'] = pd.Categorical(soma_emissao_semana['Dia da Semana'], categories=ordem_dias, ordered=True)

    soma_emissao_semana = soma_emissao_semana.sort_values('Dia da Semana')

    barras_emissao_semana = px.bar(
        soma_emissao_semana.round(1),
        x='Dia da Semana',
        y='Soma_Emissoes',
        title='Soma de emissões de CO₂ por dias da semana',
        labels={'Soma_Emissoes': 'Soma de emissões de CO₂/Kg'},
        color='Dia da Semana',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text_auto=True
    )

    barras_emissao_semana.update_layout(
        xaxis_title='Dias da Semana',
        yaxis_title='Emissão de Carbono em CO₂/Kg',
        yaxis_range=[
            soma_emissao_semana['Soma_Emissoes'].min() * 0.9,
            soma_emissao_semana['Soma_Emissoes'].max() * 1.1
        ],
        showlegend=False
    )

    col4.plotly_chart(barras_emissao_semana)

emissoes_lab(dados_finais)
emissoes_horario(dados_finais)
soma_emissoes_meses(dados_finais)
soma_emissoes_semana(dados_finais)
media_mes(dados_finais)


