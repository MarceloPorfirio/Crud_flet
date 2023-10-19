from flet import *
import sqlite3

# CRIAR BANCO DE DADOS
conn = sqlite3.connect('Novo_banco.db',check_same_thread=False)
cursor = conn.cursor()

# Criar Tabela no banco
def tabela_base():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS pessoas( id INTEGER PRIMARY KEY AUTO INCREMENT, 
                   nome TEXT)
 """)

class App(UserControl):
    def __init__(self):
        super().__init__()
    
        self.todos_dados = Column(auto_scroll=True)
        self.add_dados = TextField(label='Nome')
        self.editar_dados = TextField(label='Editar')

    # FUNÇÃO DELETAR, PASSAMOS O PARAMETRO X PARA REPRESENTAR
    def deletar(self, x , y):
        cursor.execute("DELETE FROM pessoas WHERE id = ?", [x])

        # Após deletar, fechar o modal
        y.open = False

        # chamar a função de renderizar
        self.todos_dados.controls.clear() # limpa
        self.mostrar_dados()
        self.page.update()

    def atualizar(self, x, y, z):
        cursor.execute("UPDATE pessoas SET nome = ? WHERE id = ?",(y,x)) # usar o y = nome x = id (parametros)
        conn.commit()

        z.open = False
        self.todos_dados.controls.clear()
        self.mostrar_dados()
        self.page.update()

    def abrir_acoes(self, e):
        id = e.control.subtitle.value # aqui ira apontar para o id desejado 
        self.editar_dados.value = e.control.title.value # aqui iremos editar os dados
        self.update()

        # Aqui vamos abrir a caixa de dialogo 
        alerta_dialogo = AlertDialog(
            title=Text(f'Editar ID {id}'),
            content=self.editar_dados,

            # Botões de ações
            actions=[
                ElevatedButton(
                    'Deletar',
                    color='white',bgcolor='red',
                    on_click= lambda e: self.deletar(id, alerta_dialogo)
                ),
                ElevatedButton(
                    "Atualizar", on_click=lambda e:self.atualizar(id, self.editar_dados.value, alerta_dialogo)
                )
            ],
            actions_alignment='spaceBetween'
        )

    # AQUI USAREMOS O SELECT PARA MOSTRAR OS DADOS
    def mostrar_dados(self):
        cursor.execute('SELECT * FROM pessoas')
        conn.commit()
        dados = cursor.fetchall() # percorrer todos dados da tabela
        for dado in dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes

                )
            )






    # CRIAR NOVO DADO PARA O BANCO
    def adicionar_novo_dado(self, e):
        cursor.execute("INSER INTO pessoas (nome) VALUES (?)",[self.add_dados.value])
        self.todos_dados.controls.clear()
        self.mostrar_dados()
        self.page.update()

    def ciclo(self):
        self.mostrar_dados()

    # Aqui irá tudo o que renderizar a aplicação   
    def build(self):
        return Column([
            Text("CRUD COM SQLITE",size=20, weight='bold'),
            self.add_dados,
            ElevatedButton('Adicionar',on_click=self.adicionar_novo_dado),
            self.todos_dados

        ])

def main(page:Page):
    page.update()
    meu_app = App()

    page.add(meu_app)

app(target=main)