from flet import *
import sqlite3

# CRIAR BANCO DE DADOS
conn = sqlite3.connect('Novo_banco.db',check_same_thread=False)
cursor = conn.cursor()

# Criar Tabela no banco
def tabela_base():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS cadastro( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   nome TEXT,
                   celular INT,
                   email VARCHAR
                   )
 """)

class App(UserControl):
    def __init__(self):
        super().__init__()
    
        self.todos_dados = Column(auto_scroll=True)

        self.add_dados = TextField(label='Nome')
        self.add_cel = TextField(label='Telefone')
        self.add_email = TextField(label='E-mail')

        self.editar_dados = TextField(label='Nome')
        
        
        

        tabela_base()
        
       
    # FUNÇÃO DELETAR, PASSAMOS O PARAMETRO X PARA REPRESENTAR
    def deletar(self, x , y):
        cursor.execute("DELETE FROM cadastro WHERE id = ?", (x,))

        # Após deletar, fechar o modal
        y.open = False

        # chamar a função de renderizar
        self.todos_dados.controls.clear() # limpa
        self.mostrar_dados()
        self.page.update()

       

    def atualizar(self, x, y, z):
        cursor.execute("UPDATE cadastro SET nome = ?, celular = ?, email = ? WHERE id = ?", (y.value, self.add_cel.value, self.add_email.value, x))
         # usar o y = nome x = id (parametros)
        conn.commit()

        z.open = False

         # Limpe os campos após a atualização
        self.add_dados.value = ""
        self.add_cel.value = ""
        self.add_email.value = ""
        # Dê foco ao campo "nome" após a atualização
        

        self.todos_dados.controls.clear()
        self.mostrar_dados()
        self.page.update()
        
    def abrir_acoes(self, e):
        id = e.control.subtitle.value  # aqui irá apontar para o id desejado

        # Recupere os dados do registro com base no ID
        cursor.execute("SELECT nome, celular, email FROM cadastro WHERE id = ?", (id,))
        dados = cursor.fetchone()
        if dados:
            nome, celular, email = dados
        else:
            nome, celular, email = "", "", ""  # Defina valores padrão caso o registro não seja encontrado

        # Preencha os campos do modal com os dados
        self.add_dados.value = nome
        self.add_cel.value = celular
        self.add_email.value = email

        # Abra a caixa de diálogo
        alerta_dialogo = AlertDialog(
            title=Text(f'Editar ID {id}'),
            content=Column([
                self.add_dados,
                self.add_cel,
                self.add_email
            ]),

            actions=[
                ElevatedButton(
                    'Deletar',
                    color='white', bgcolor='red',
                    on_click=lambda e: self.deletar(id, alerta_dialogo)
                ),
                ElevatedButton(
                    "Atualizar", on_click=lambda e: self.atualizar(id, self.editar_dados, alerta_dialogo)
                )
            ],
            actions_alignment='spaceBetween'
        )

        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True

        

        self.page.update()


    # AQUI USAREMOS O SELECT PARA MOSTRAR OS DADOS
    def mostrar_dados(self):
        cursor.execute('SELECT * FROM cadastro')
        conn.commit()
        dados = cursor.fetchall() # percorrer todos dados da tabela
        for dado in dados:
            self.todos_dados.controls.append(
                
                    ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(f"Nome: {dado[1]}\nCelular: {dado[2]}\nEmail: {dado[3]}"),
                    on_click=self.abrir_acoes

                )
                 
                
            )
            self.update()

      

    # CRIAR NOVO DADO PARA O BANCO
    def adicionar_novo_dado(self, e):
        
        cursor.execute("INSERT INTO cadastro (nome , celular , email) VALUES (?, ? , ?)",(self.add_dados.value,self.add_cel.value,self.add_email.value))
        conn.commit()
        self.todos_dados.controls.clear()
        self.mostrar_dados()
        self.page.update()
        
        # Adicionar um alertdialog
        dlg= AlertDialog(
            title=Text('Dados adicionados com sucesso!'),
            content=Text('Os dados foram adicionados com sucesso.'),
            # actions=[
            #     ElevatedButton(
            #         'OK',
            #         on_click=lambda e: dlg.close()
            #     )
            # ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()



    def ciclo(self):
        self.mostrar_dados()

    # Aqui irá tudo o que renderizar a aplicação   
    def build(self):
        return Column([
            Text("CRUD COM SQLITE",size=20, weight='bold'),
            self.add_dados,
            self.add_cel,
            self.add_email,
            ElevatedButton('Adicionar',on_click=self.adicionar_novo_dado),
            self.todos_dados,
            

        ])
    
    

def main(page:Page):
    page.update()
    meu_app = App()
    
    page.add(meu_app)

app(target=main)