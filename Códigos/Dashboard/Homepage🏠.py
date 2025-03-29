import streamlit as st

st.set_page_config(
    layout="wide"
)

st.title("Estimativas das Emissões de CO₂ nos Laboratórios da FACOMP-UFPA")

st.write("Bem-vindo ao dashboard das emissões CO₂!")
st.write("O objetivo deste dashboard é mostrar os resultados das estimativas de carbono dos computadores nos três laboratórios da faculdade de computação da UFPA."
"Os dados estão distribuídos em horários de aulas, laboratórios, dias da semana e meses")
st.write("A leitura para os horários de aula são as seguintes:"
"(Aula 1 = 13:00/14:40)"
 "(Aula 2 = 14:50/16:30)"
 "(Aula 3 = 16:40/18:20)")
st.write("Use o menu à esquerda para navegar entre os meses e os dados finais.")
