from pathlib import Path
from sqlalchemy import create_engine, String, Boolean, Integer, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

pasta_atual = Path(__file__).parent

PATH_TO_BD = pasta_atual/'bd_usuarios.sqlite'

class Base(DeclarativeBase):
  pass

class Usuario(Base):
  __tablename__ = 'usuarios'

  id: Mapped[int] = mapped_column(primary_key=True)
  nome: Mapped[str] = mapped_column(String(30))
  senha: Mapped[str] = mapped_column(String(30))
  email: Mapped[str] = mapped_column(String(30))
  acesso_gestor: Mapped[bool] = mapped_column(Boolean(), default=False)

  def __repr__(self):
    return f"Usuario({self.id=}, {self.nome=})"

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
          usuario = Usuario(
              nome=nome,
              senha=senha,
              email=email,
              **kwargs
          )
          session.add(usuario)
          session.commit()

def ler_todos_usuarios():
  with Session(bind=engine) as session:
    comando_sql = select(Usuario)
    usuarios = session.execute(comando_sql).fetchall()
    usuarios = [usuario[0] for usuario in usuarios]  
    return usuarios

def ler_usuario_id(id):
  with Session(bind=engine) as session:
    comando_sql = select(Usuario).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    return usuarios[0][0]

def modifica_usuario(
      id,
     **kwargs
      ):

  with Session(bind=engine) as session:
    comando_sql = select(Usuario).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    for usuario in usuarios:
      for key, value in kwargs.items():
        setattr(usuario[0], key, value)
        
    session.commit()

def deleta_usuario(id):
  with Session(bind=engine) as session:
    comando_sql = select(Usuario).filter_by(id=id)
    usuarios = session.execute(comando_sql).fetchall()
    for usuario in usuarios:
      session.delete(usuario[0])
    session.commit()

   
  
     
    

if __name__ == '__main__':
    # cria_usuarios(
    #   'Leo Bakerly',
    #   senha='123',
    #   email='leo@gmail.com',
    #   acesso_gestor=True
    #   )

    # usuarios = ler_todos_usuarios()
    # usuario_0 = usuarios[0]
    # print(usuario_0)
    # print(usuario_0.nome)
    # print(usuario_0.senha)
    # print(usuario_0.email)

    # usuario_gustavo = ler_usuario_id(id=1)
    # print(usuario_gustavo)
    # print(usuario_gustavo.nome, usuario_gustavo.senha, usuario_gustavo.email)

    # modifica_usuario(id=1, nome='Jorge Prioeli', email='jorgeprioelit@gmail.com', senha="123@", acesso_gestor=True)

    deleta_usuario(id=1)

    
      