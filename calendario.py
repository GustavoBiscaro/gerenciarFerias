import streamlit as st
from streamlit_calendar import calendar
from crud import (
    ler_todos_usuarios,
    ler_usuario_id
)
import json

def exibir_calendario():
    from datetime import datetime

    with open('calendar_options.json', "r", encoding="utf-8") as f:
        calendar_options = json.load(f)

    if 'ultimo_clique' not in st.session_state:
        st.session_state['ultimo_clique'] = ''

    def limpar_datas():
        st.session_state.pop('data_inicio', None)
        st.session_state.pop('data_final', None)

    usuarios = ler_todos_usuarios()
    calendar_events = []
    for usuario_loop in usuarios:
        calendar_events.extend(usuario_loop.lista_ferias())

    usuario = st.session_state['usuario']
    usuario = ler_usuario_id(usuario.id)  # Garantir dados atualizados

    with st.expander('Dias para solicitar'):
        st.markdown(f'O usuário {usuario.nome} tem **{usuario.dias_para_solicitar()}** dias para solicitar férias.')

    # ✅ Todos os usuários podem deletar seus próprios eventos (e da base)
    if usuario.eventos_ferias:
        if st.button('🗑️ Deletar meus eventos de férias', use_container_width=True, type='primary'):
            usuario.deletar_todos_eventos_ferias()  # <- esta função deve deletar no banco também
            st.success('Seus eventos de férias foram excluídos com sucesso!')
            st.rerun()

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
