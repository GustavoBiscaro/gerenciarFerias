import streamlit as st
from streamlit_calendar import calendar
from crud import (
    ler_todos_usuarios,
    cria_usuarios,
    modifica_usuario,
    deleta_usuario,
    ler_usuario_id
)
import json

def exibir_calendario():
    from datetime import datetime  # caso ainda não esteja importado

    with open('calendar_options.json', "r", encoding="utf-8") as f:
        calendar_options = json.load(f)

    if 'ultimo_clique' not in st.session_state:
        st.session_state['ultimo_clique'] = ''

    def limpar_datas():
        if 'data_inicio' in st.session_state:
            del st.session_state['data_inicio']
        if 'data_final' in st.session_state:
            del st.session_state['data_final']

    usuarios = ler_todos_usuarios()
    calendar_events = []
    for usuario in usuarios:
        calendar_events.extend(usuario.lista_ferias())

    usuario = st.session_state['usuario']

    with st.expander('Dias para solicitar'):
        usuario = ler_usuario_id(usuario.id)
        st.markdown(f'O usuário {usuario.nome} tem **{usuario.dias_para_solicitar()}** dias para solicitar férias.')

    # Botão visível apenas para gestor
    if usuario.acesso_gestor and usuario.eventos_ferias:
        if st.button('🗑️ Deletar todos os eventos de férias', use_container_width=True, type='primary'):
            usuario.deletar_todos_eventos_ferias()
            st.success('Todos os eventos de férias foram excluídos com sucesso!')
            st.experimental_rerun()

    calendar_widget = calendar(
        events=calendar_events,
        options=calendar_options,
    )

    if 'callback' in calendar_widget and calendar_widget['callback'] == 'dateClick':
        raw_date = calendar_widget['dateClick']['date']
        if raw_date != st.session_state['ultimo_clique']:
            st.session_state['ultimo_clique'] = raw_date

        st.session_state['ultimo_clique'] = calendar_widget['dateClick']['date']

        date = calendar_widget['dateClick']['date'].split('T')[0]

        if 'data_inicio' not in st.session_state:
            st.session_state['data_inicio'] = date
            st.warning(f'Data de início de férias selecionada {date}')
        else:
            st.session_state['data_final'] = date
            date_inicio = st.session_state['data_inicio']

            cols = st.columns([0.7, 0.3])
            with cols[0]:
                st.warning(f'Data de início de férias selecionada {date_inicio}')
            with cols[1]:
                st.button('Limpar', use_container_width=True, on_click=limpar_datas)

            cols = st.columns([0.7, 0.3])
            with cols[0]:
                st.warning(f'Data final de férias selecionada {date}')
            with cols[1]:
                st.button("Adicionar Férias", use_container_width=True,
                          on_click=usuario.adicionar_ferias,
                          args=(date_inicio, date))
