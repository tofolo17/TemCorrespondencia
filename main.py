from sys import platform
from tkinter import *
from tkinter.ttk import Notebook

import pyautogui

largura, altura = pyautogui.size()
fonte_padrao = ("Arial", "10")


class ConfigRoot:
    def __init__(
            self,
            master,
            largura_janela: int,
            altura_janela: int,
            titulo: str,
            x=0
    ):
        self.master = master
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        self.titulo = self.master.title(titulo)
        if platform != 'linux':
            self.icone = self.master.iconbitmap('images/icon.ico')
        self.geometria = self.master.geometry(
            f"{self.largura_janela}x"
            f"{self.altura_janela}+"
            f"{int(largura / 2) - int(self.largura_janela / 2) + x}+"
            f"{int(altura / 2) - int(self.altura_janela / 2) + x}"
        )
        self.redimensionavel = self.master.resizable(0, 0)

    def iniciar(self):
        self.master.mainloop()


class Login(ConfigRoot):
    def __init__(self, master=None, largura_janela=300, altura_janela=170, titulo='Login'):
        super().__init__(master, largura_janela, altura_janela, titulo)
        self.master.bind('<Return>', self.verifica_senha)
        self.master.focus_force()

        self.primeiroContainer = Frame(self.master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Insira seus dados")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nome_label = Label(self.segundoContainer, text="Nome", font=fonte_padrao, width=5)
        self.nome_label.grid(row=0, column=0)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = fonte_padrao
        self.nome.grid(row=0, column=1)
        self.nome.focus()

        self.senha_label = Label(self.terceiroContainer, text="Senha", font=fonte_padrao, width=5)
        self.senha_label.grid(row=0, column=0)

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = fonte_padrao
        self.senha["show"] = "*"
        self.senha.grid(row=0, column=1)

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Autenticar"
        self.autenticar["font"] = ("Arial", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.verifica_senha
        self.autenticar.pack()

        self.mensagem = Label(self.quartoContainer, text="", font=fonte_padrao)
        self.mensagem.pack()

    def verifica_senha(self, event=None):
        usuario = self.nome.get()
        senha = self.senha.get()
        with open('data/users', 'r') as f:
            data = [line for line in f.read().splitlines()]
        if usuario == "a" and senha == "a":
            self.master.destroy()
            cad_root = Tk()
            CadUser(master=cad_root).iniciar()
        elif f'{usuario} {senha}' in data:
            self.master.destroy()
            menu_root = Tk()
            MenuUser(master=menu_root, usuario=usuario, senha=senha).iniciar()
        else:
            self.mensagem['text'] = "Erro na autenticação"
        if event:
            pass


class MenuUser(ConfigRoot):
    def __init__(
            self, usuario, senha, master=None, largura_janela=400, altura_janela=400, titulo='Correspondência Ipê'
    ):
        super().__init__(master, largura_janela, altura_janela, titulo)
        self.master.focus_force()

        self.usuario = usuario
        self.senha = senha

        """
        Morador (cadastrar, ver por bloco, histórico)
        Encomendas (registrar, ver, enviar/reenviar e-mail, dar baixa)
        """

        self.tab_control = Notebook(self.master)
        self.tab1 = Frame(self.tab_control)
        self.tab2 = Frame(self.tab_control)
        self.tab3 = Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Moradores')
        self.tab_control.add(self.tab2, text='Encomendas')
        self.tab_control.pack(expand=1, fill="both")

        self.primeiroContainer = Frame(self.master)
        self.primeiroContainer['pady'] = 10
        self.primeiroContainer.pack()

        self.perfil = Button(self.primeiroContainer)
        self.perfil["text"] = "Perfil"
        self.perfil["font"] = ("Arial", "8")
        self.perfil["width"] = 14
        self.perfil["command"] = self.ver_perfil
        self.perfil.grid(row=0, column=0, padx=30)

        self.finalizar = Button(self.primeiroContainer)
        self.finalizar["text"] = "Finalizar sessão"
        self.finalizar["font"] = ("Arial", "8")
        self.finalizar["width"] = 14
        self.finalizar["command"] = self.finaliza_sessao
        self.finalizar.grid(row=0, column=1, padx=30)

    def finaliza_sessao(self):
        self.master.destroy()
        login_root = Tk()
        Login(master=login_root).iniciar()

    def ver_perfil(self):
        perfil = Toplevel(self.master)
        Profile(master=perfil, usuario=self.usuario, senha=self.senha).iniciar()


class Profile(ConfigRoot):
    def __init__(self, usuario, senha, master=None, largura_janela=300, altura_janela=170, titulo='Perfil'):
        super().__init__(master, largura_janela, altura_janela, titulo)
        self.master.focus_force()
        self.master.grab_set()

        self.usuario_bd = usuario
        self.senha_bd = senha

        self.primeiroContainer = Frame(self.master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Seus dados")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nome_label = Label(self.segundoContainer, text="Nome", font=fonte_padrao, width=5)
        self.nome_label.grid(row=0, column=0)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = fonte_padrao
        self.nome.insert(END, usuario)
        self.nome.grid(row=0, column=1)
        self.nome.focus()

        self.senha_label = Label(self.terceiroContainer, text="Senha", font=fonte_padrao, width=5)
        self.senha_label.grid(row=0, column=0)

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = fonte_padrao
        self.senha.insert(END, senha)
        self.senha.grid(row=0, column=1)

        self.alterar = Button(self.quartoContainer)
        self.alterar["text"] = "Alterar"
        self.alterar["font"] = ("Arial", "8")
        self.alterar["width"] = 12
        self.alterar["command"] = self.alterar_perfil
        self.alterar.pack()

        self.mensagem = Label(self.quartoContainer, text="", font=fonte_padrao)
        self.mensagem.pack()

    def alterar_perfil(self):
        data = f'{self.usuario_bd} {self.senha_bd}'
        new_data = f'{self.nome.get()} {self.senha.get()}'
        if (self.nome.get() and self.senha.get()) != '' and len(self.senha.get()) >= 5 and data != new_data:
            linhas = [line for line in open("data/users", "r").read().splitlines() if line]
            with open("data/users", "w") as f:
                for linha in linhas:
                    if linha.strip('\n') != data:
                        f.write(f'{linha}\n')
                    else:
                        f.write(f'{new_data}\n')
            self.mensagem['text'] = 'Valores alterados.'
        else:
            self.mensagem['text'] = 'Valores inválidos.'


class CadUser(ConfigRoot):
    def __init__(self, master=None, largura_janela=325, altura_janela=170, titulo='Cadastro de usuário'):
        super().__init__(master, largura_janela, altura_janela, titulo)
        self.master.bind('<Return>', self.verifica_cadastro)
        self.master.focus_force()

        self.primeiroContainer = Frame(self.master)
        self.primeiroContainer['pady'] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer, text="Nome", font=fonte_padrao, width=5)
        self.nomeLabel.grid(row=0, column=0)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = fonte_padrao
        self.nome.grid(row=0, column=1)
        self.nome.focus()

        self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=fonte_padrao, width=5)
        self.senhaLabel.grid(row=0, column=0)

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = fonte_padrao
        self.senha["show"] = "*"
        self.senha.grid(row=0, column=1)

        self.cadastrar = Button(self.quartoContainer)
        self.cadastrar["text"] = "Cadastrar"
        self.cadastrar["font"] = ("Arial", "8")
        self.cadastrar["width"] = 10
        self.cadastrar["command"] = self.verifica_cadastro
        self.cadastrar.grid(row=0, column=0, padx=3)

        self.ver_cadastros = Button(self.quartoContainer)
        self.ver_cadastros["text"] = "Ver cadastros"
        self.ver_cadastros["font"] = ("Arial", "8")
        self.ver_cadastros["width"] = 14
        self.ver_cadastros["command"] = self.ver_cadastrados
        self.ver_cadastros.grid(row=0, column=1, padx=3)

        self.voltar = Button(self.quartoContainer)
        self.voltar["text"] = "Voltar"
        self.voltar["font"] = ("Arial", "8")
        self.voltar["width"] = 10
        self.voltar["command"] = self.volta_login
        self.voltar.grid(row=0, column=2, padx=3)

        self.texto = StringVar()
        self.mensagem = Label(self.quartoContainer, textvariable=self.texto, font=fonte_padrao)
        self.mensagem.grid(columnspan=3)

    def verifica_cadastro(self, event=None):
        usuario = self.nome.get().strip()
        senha = self.senha.get()
        try:
            usuarios = [line.split()[0] for line in open("data/users", "r").read().splitlines() if line]
            if usuario not in usuarios and (usuario and senha) != '' and len(senha) >= 5:
                with open('data/users', 'a') as f:
                    f.write(f'\n{usuario} {senha}')
                self.nome.delete(0, END)
                self.senha.delete(0, END)
                self.nome.focus()
                self.texto.set("Cadastro realizado")
            else:
                if usuario == '' or senha == '':
                    self.texto.set("Campos vazios não são aceitos")
                elif usuario in usuarios:
                    self.texto.set("Nome de usuário já cadastrado")
                else:
                    self.texto.set("A senha deve ter no mínimo 5 caracteres")
        except IndexError:
            print('alo')
            self.texto.set("Campos vazios não são aceitos")
        if event:
            pass

    def ver_cadastrados(self):
        cad_list = Toplevel(self.master)
        CadList(master=cad_list).iniciar()

    def volta_login(self):
        self.master.destroy()
        login_root = Tk()
        Login(master=login_root).iniciar()


class CadList(ConfigRoot):
    def __init__(self, master=None, w_witdh=300, altura_janela=300, titulo='Cadastrados', x=75):
        super().__init__(master, w_witdh, altura_janela, titulo, x)
        self.master.bind('<Return>', self.deletar_ativo)
        self.master.focus_force()
        self.master.grab_set()

        self.primeiroContainer = Frame(self.master)
        self.primeiroContainer["pady"] = 5
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.master)
        self.segundoContainer['padx'] = 43
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.master)
        self.terceiroContainer['pady'] = 10
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.master)
        self.quartoContainer.pack()

        self.quintoContainer = Frame(self.master)
        self.quintoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Usuários cadastrados")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.listbox_cadastrados = Listbox(
            master=self.segundoContainer,
            font=fonte_padrao,
            width=30,
            selectmode='SINGLE'
        )
        cadastrados = [line.split()[0] for line in open("data/users", "r").read().splitlines() if line]
        for cadastrado in cadastrados:
            self.listbox_cadastrados.insert(END, cadastrado)
        self.listbox_cadastrados.pack()
        self.listbox_cadastrados.bind('<<ListboxSelect>>', self.pegar_ativo)

        self.senha_label = Label(self.terceiroContainer, text='Senha', font=('Arial', '10', 'bold'))
        self.senha_label.grid(row=0, column=0)

        self.senha_usuario = StringVar()
        self.mensagem_senha = Label(
            self.terceiroContainer, textvariable=self.senha_usuario, width=20, font=fonte_padrao
        )
        self.mensagem_senha.grid(row=0, column=1)

        self.botao_deletar = Button(self.quartoContainer)
        self.botao_deletar["text"] = "Apagar usuário"
        self.botao_deletar["font"] = ("Arial", "8")
        self.botao_deletar["width"] = 30
        self.botao_deletar["command"] = self.deletar_ativo
        self.botao_deletar.pack()

        self.mensagem = Label(self.quintoContainer, text="", font=fonte_padrao)
        self.mensagem.pack()

        self.listbox_cadastrados.select_set(0)
        self.listbox_cadastrados.event_generate("<<ListboxSelect>>")

    def pegar_ativo(self, event=None):
        try:
            self.mensagem['text'] = ''
            index = self.listbox_cadastrados.curselection()
            senhas = [line.strip('\n').split()[1] for line in open("data/users", "r").read().splitlines() if line]
            valor = senhas[index[0]]
            self.senha_usuario.set(valor)
            if event:
                pass
        except IndexError:
            pass

    def deletar_ativo(self, event=None):
        senha_ativa = self.senha_usuario.get()
        if senha_ativa == "":
            self.mensagem['text'] = "Selecione algum usuário."
        else:
            self.mensagem['text'] = "Usuário apagado."
            linhas = [line for line in open("data/users", "r").read().splitlines() if line]
            with open("data/users", "w") as f:
                for linha in linhas:
                    if linha.strip('\n').split(' ')[1] != senha_ativa:
                        f.write(f'{linha}\n')
            self.listbox_cadastrados.delete(0, END)
            with open('data/users', 'r') as f:
                cadastrados = [line.split()[0] for line in f]
            for cadastrado in cadastrados:
                self.listbox_cadastrados.insert(END, cadastrado)
            self.senha_usuario.set('')
        if event:
            pass


root = Tk()

Login(master=root).iniciar()

root.mainloop()