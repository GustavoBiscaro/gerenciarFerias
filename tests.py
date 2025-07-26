class Veiculo:
    rodas = None
    def __init__(self, cor, modelo):
      self.cor = cor
      self.modelo = modelo
      self.ligado = False

    # Ação
    def descricao(self):
      print(f'Meu modelo é {self.modelo} e minha cor é {self.cor}')

    def ligar(self):
      self.ligado = True
      print(f'O veículo {self.modelo} está ligado.')  

    def pintar(self, nova_cor):
      self.cor = nova_cor
      print(f'O veículo {self.modelo} agora é {self.cor}')

    def desligar(self):
      self.ligado = False
      print(f'O veículo {self.modelo} está desligado.')

class Carro(Veiculo):
  rodas = 4
  def descricao(self):
    print(f'Meu modelo de carro é {self.modelo} e minha cor é {self.cor}')


meu_carro = Veiculo('azul', 'Fusca')
carro = Carro('preto', 'Civic')

carro.descricao()
print(meu_carro.rodas)
print(carro.rodas)

meu_carro.descricao()
meu_carro.ligar()
meu_carro.desligar()
meu_carro.pintar('vermelho')
    

