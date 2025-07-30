from pathlib import Path
from datetime import datetime
import warnings

from sqlalchemy import create_engine, String, Boolean, Integer, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

from werkzeug.security import generate_password_hash, check_password_hash

pasta_atual = Path(__file__).parent

PATH_TO_BD = pasta_atual/'bd_usuarios.sqlite'

class Base(DeclarativeBase):
  pass

class UsuarioFerias(Base):
  __tablename__ = 'usuarios_ferias'

  id: Mapped[int] = mapped_column(primary_key=True)
  nome: Mapped[str] = mapped_column(String(30))
  senha: Mapped[str] = mapped_column(String(128))
  email: Mapped[str] = mapped_column(String(30))
  acesso_gestor: Mapped[bool] = mapped_column(Boolean(), default=False)
  inicio_na_empresa: Mapped[str] = mapped_column(String(30))
  eventos_ferias: Mapped[list['EventosFerias']] = relationship(
    back_populates="pai",
    lazy='subquery',
    )

  def __repr__(self):
    return f"Usuario({self.id=}, {self.nome=})"

  def define_senha(self, senha):
    self.senha = generate_password_hash(senha)

  def verifica_senha(self, senha):
    return check_password_hash(self.senha, senha)

  

  def adicionar_ferias(self, inicio_ferias, fim_ferias):
    total_dias = (datetime.strptime(fim_ferias, '%Y-%m-%d') - datetime.strptime(inicio_ferias, '%Y-%m-%d')).days + 1
    with Session(bind=engine) as session:
      ferias = EventosFerias(
        id_pai=self.id,
        inicio_ferias=inicio_ferias,
        fim_ferias=fim_ferias,
        total_dias=total_dias)
      session.add(ferias)
      session.commit()

  def deletar_todos_eventos_ferias(self):
      with Session(bind=engine) as session:
          comando_sql = select(EventosFerias).filter_by(id_pai=self.id)
          eventos = session.execute(comando_sql).scalars().all()
          for evento in eventos:
              session.delete(evento)
          session.commit()

  def lista_ferias(self):
    lista_eventos = []
    for evento in self.eventos_ferias:
      lista_eventos.append({
        'title': f'Férias de {self.nome}',
        'start': evento.inicio_ferias,
        'end': evento.fim_ferias,
        'resourceId': self.id
        })
    return lista_eventos
   
  def dias_para_solicitar(self):
    formatos = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
    
    data_inicio = None
    for formato in formatos:
        try:
            data_inicio = datetime.strptime(self.inicio_na_empresa, formato)
            break
        except ValueError:
            continue

    if data_inicio is None:
        raise ValueError(f"Data inválida: {self.inicio_na_empresa}")

    # Cálculo proporcional (limite anual: 30 dias)
    dias_proporcionais = (datetime.now() - data_inicio).days * (30 / 365)
    dias_proporcionais = min(dias_proporcionais, 30)  # Limita a no máximo 30 dias

    dias_tirados = sum(evento.total_dias for evento in self.eventos_ferias)

    if dias_tirados >= dias_proporcionais:
        warnings.warn("Você já utilizou o total de dias disponíveis. Não é possível solicitar mais férias no momento.")
        return 0

    dias_disponiveis = int(dias_proporcionais - dias_tirados)

    return dias_disponiveis


  
class EventosFerias(Base):
  __tablename__ = 'eventos_ferias'
  
  id: Mapped[int] = mapped_column(primary_key=True)
  id_pai: Mapped[int] = mapped_column(ForeignKey('usuarios_ferias.id'))
  pai: Mapped["UsuarioFerias"] = relationship(lazy='subquery')
  inicio_ferias: Mapped[str] = mapped_column(String(30))
  fim_ferias: Mapped[str] = mapped_column(String(30))
  total_dias: Mapped[int] = mapped_column(Integer())
  

engine = create_engine(f'sqlite:///{PATH_TO_BD}')
Base.metadata.create_all(bind=engine)

# CRUD 
def cria_usuarios(
  nome, 
  senha, 
  email, 
  **kwargs
  ):
      with Session(bind=engine) as session:
          usuario = UsuarioFerias(
              nome=nome,
              email=email,
              **kwargs
          )
          usuario.define_senha(senha)
          session.add(usuario)
          session.commit()

def ler_todos_usuarios():
  with Session(bind=engine) as session:
    comando_sql = select(UsuarioFerias)
    usuarios = session.execute(comando_sql).fetchall()
    usuarios = [usuario[0] for usuario in usuarios]  
    return usuarios

def ler_usuario_id(id):
  with Session(bind=engine) as session:
    comando_sql = select(UsuarioFerias).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    return usuarios[0][0]

def modifica_usuario(
      id,
     **kwargs
      ):

  with Session(bind=engine) as session:
    comando_sql = select(UsuarioFerias).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    for usuario in usuarios:
      for key, value in kwargs.items():
        if key == 'senha':
          usuario[0].define_senha(value)
        else:
          setattr(usuario[0], key, value)
    session.commit()

def deleta_usuario(id):
  with Session(bind=engine) as session:
    comando_sql = select(UsuarioFerias).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    for usuario in usuarios:
      session.delete(usuario[0])
    session.commit()

if __name__ == '__main__':
  pass
#   cria_usuarios(
#     'Gustavo Biscaro',
#     senha='123',
#     email='gustavo.biscaro@gmail.com',
#     inicio_na_empresa='2025-01-01',
#     acesso_gestor=True
#     )
  
# if __name__ == '__main__':
#   cria_usuarios(
#     'Jerry Smith',
#     senha='123@',
#     email='jerry@linkedIn.com',
#     inicio_na_empresa='2025-02-02',
#     acesso_gestor=False,
#     )
