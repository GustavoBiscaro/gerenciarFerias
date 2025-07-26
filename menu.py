import streamlit as st
from time import sleep

from crud import ler_todos_usuarios

st.set_page_config(
  layout="wide",
  page_icon="🎆",
  page_title="RH MAX"
)

def login():
  with st.container(border=True):
    st.markdown('Bem-vindo ao RH Max!')
    usuarios = ler_todos_usuarios()
    usuarios = {usuario.nome: usuario for usuario in usuarios}
    nome_usuario = st.selectbox(
      'Selecione o usuário',
      list(usuarios.keys())
      )
    senha = st.text_input('Digite sua senha', type='password')

    if st.button('Acessar'):
      usuario = usuarios[nome_usuario]
      if usuario.verifica_senha(senha):
        st.success(f'Bem-vindo, {usuario.nome}!')
        st.session_state['usuario'] = usuario
        st.session_state['logado'] = True
        sleep(1)
        st.rerun()
      else:
        st.error('Senha incorreta. Tente novamente.')
    

def main():
  if not 'logado' in st.session_state:
    st.session_state['logado'] = False
  if not st.session_state['logado']:
    login()
  else:
    st.markdown('# Saudações, RH Max!')

if __name__ == '__main__':
  main()