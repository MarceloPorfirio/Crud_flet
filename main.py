from flet import *
import sqlite3

class App(UserControl):
    def __init__(self):
        super().__init__()
    
        self.todos_dados = Column(auto_scroll=True)
        self.add_dados = TextField(label='Nome')
        self.editar_dados = TextField(label='Editar')

    def build(self):
        return Column([
            Text("CRUD COM SQLITE",size=20, weight='bold'),
            self.add_dados
        ])

def main(page:Page):
    meu_app = App()

    page.add(meu_app)

app(target=main)