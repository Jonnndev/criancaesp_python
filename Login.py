import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import subprocess  # Import subprocess
from datetime import datetime

class CriancaEsperancaLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Criança Esperança - Sistema de Acesso")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#FFD93D')
        
        # Centralizar janela
        self.center_window()
        
        # Database
        self.init_database()
        
        # Variáveis
        self.is_login_mode = True
        
        # Interface
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"400x600+{x}+{y}")
    
    def init_database(self):
        """Inicializa banco SQLite"""
        try:
            self.conn = sqlite3.connect("crianca_esperanca.db")
            cursor = self.conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nome_completo TEXT,
                    email TEXT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print("✅ Banco inicializado!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro no banco: {e}")
    
    def create_widgets(self):
        # Container principal
        main_frame = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        main_frame.pack(expand=True, fill='both', padx=20, pady=30)
        
        # Header
        self.create_header(main_frame)
        
        # Formulário
        self.create_form(main_frame)
        
        # Botões
        self.create_buttons(main_frame)
        
        # Status
        self.status_label = tk.Label(
            main_frame, text="", font=('Arial', 10), 
            fg='#666', bg='white'
        )
        self.status_label.pack(pady=10)
    
    def create_header(self, parent):
        # Logo
        logo_label = tk.Label(
            parent, text="🎪 CRIANÇA ESPERANÇA 🎭",
            font=('Comic Sans MS', 16, 'bold'),
            fg='#FF6B9D', bg='white'
        )
        logo_label.pack(pady=10)
        
        # Título dinâmico
        self.title_label = tk.Label(
            parent, text="🌟 ENTRAR 🌟",
            font=('Comic Sans MS', 20, 'bold'),
            fg='#4D96FF', bg='white'
        )
        self.title_label.pack(pady=5)
        
        # Subtítulo
        self.subtitle_label = tk.Label(
            parent, text="Juntos fazemos a diferença! 💝",
            font=('Arial', 11), fg='#666', bg='white'
        )
        self.subtitle_label.pack(pady=(0, 20))
    
    def create_form(self, parent):
        # Frame do formulário
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill='x', padx=20)
        
        # Username
        tk.Label(form_frame, text="👤 Nome de usuário:", 
                font=('Arial', 10, 'bold'), fg='#333', bg='white').pack(anchor='w', pady=(10,2))
        
        self.username_entry = tk.Entry(
            form_frame, font=('Arial', 11), relief='solid', bd=1
        )
        self.username_entry.pack(fill='x', pady=(0,10), ipady=8)
        
        # Password
        tk.Label(form_frame, text="🔒 Senha:", 
                font=('Arial', 10, 'bold'), fg='#333', bg='white').pack(anchor='w', pady=(0,2))
        
        self.password_entry = tk.Entry(
            form_frame, font=('Arial', 11), show="*", relief='solid', bd=1
        )
        self.password_entry.pack(fill='x', pady=(0,10), ipady=8)
        
        # Campos extras para cadastro (inicialmente ocultos)
        self.extra_frame = tk.Frame(form_frame, bg='white')
        
        # Nome completo
        tk.Label(self.extra_frame, text="📝 Nome completo:", 
                font=('Arial', 10, 'bold'), fg='#333', bg='white').pack(anchor='w', pady=(10,2))
        
        self.nome_entry = tk.Entry(
            self.extra_frame, font=('Arial', 11), relief='solid', bd=1
        )
        self.nome_entry.pack(fill='x', pady=(0,10), ipady=8)
        
        # Email
        tk.Label(self.extra_frame, text="📧 E-mail:", 
                font=('Arial', 10, 'bold'), fg='#333', bg='white').pack(anchor='w', pady=(0,2))
        
        self.email_entry = tk.Entry(
            self.extra_frame, font=('Arial', 11), relief='solid', bd=1
        )
        self.email_entry.pack(fill='x', pady=(0,10), ipady=8)
    
    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        # Botão principal
        self.main_button = tk.Button(
            button_frame, text="🚀 ENTRAR",
            font=('Arial', 12, 'bold'),
            bg='#FF6B9D', fg='white',
            relief='flat', pady=12,
            command=self.handle_main_action,
            cursor='hand2'
        )
        self.main_button.pack(fill='x', pady=(0,15))
        
        # Link para alternar modo
        self.toggle_link = tk.Label(
            button_frame, text="Não tem conta? Cadastre-se aqui! 🌟",
            font=('Arial', 10, 'underline'),
            fg='#4D96FF', bg='white',
            cursor='hand2'
        )
        self.toggle_link.pack()
        self.toggle_link.bind("<Button-1>", self.toggle_mode)
    
    def toggle_mode(self, event=None):
        """Alterna entre login e cadastro"""
        self.is_login_mode = not self.is_login_mode
        
        if self.is_login_mode:
            # Modo Login
            self.title_label.config(text="🌟 ENTRAR 🌟")
            self.subtitle_label.config(text="Juntos fazemos a diferença! 💝")
            self.main_button.config(text="🚀 ENTRAR")
            self.toggle_link.config(text="Não tem conta? Cadastre-se aqui! 🌟")
            self.extra_frame.pack_forget()
        else:
            # Modo Cadastro
            self.title_label.config(text="🎪 CADASTRAR 🎪")
            self.subtitle_label.config(text="Venha fazer parte desta família! 🌈")
            self.main_button.config(text="✨ CADASTRAR")
            self.toggle_link.config(text="Já tem conta? Entre aqui! 🏠")
            self.extra_frame.pack(fill='x')
        
        # Limpar campos
        self.clear_fields()
    
    def clear_fields(self):
        """Limpa todos os campos"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, 'nome_entry'):
            self.nome_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        self.status_label.config(text="")
    
    def handle_main_action(self):
        """Processa login ou cadastro"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_message("Preencha usuário e senha! 📝", "error")
            return
        
        if self.is_login_mode:
            self.login(username, password)
        else:
            self.register(username, password)
    
    def login(self, username, password):
        """Processa login"""
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, nome_completo FROM usuarios 
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                user_id, username, nome_completo = user
                self.show_message("Login realizado com sucesso! 🎉", "success")
                self.show_welcome_screen(username, nome_completo or username)
            else:
                self.show_message("Usuário ou senha incorretos! 😔", "error")
                
        except sqlite3.Error as e:
            self.show_message(f"Erro no banco: {e}", "error")
    
    def register(self, username, password):
        """Processa cadastro"""
        try:
            if len(password) < 4:
                self.show_message("Senha deve ter pelo menos 4 caracteres! 🔒", "error")
                return
            
            nome_completo = self.nome_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if not nome_completo:
                self.show_message("Preencha seu nome completo! 📝", "error")
                return
            
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO usuarios (username, password, nome_completo, email)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, nome_completo, email))
            
            self.conn.commit()
            self.show_message("Conta criada com sucesso! 🎉", "success")
            
            # Limpar e voltar ao login
            self.clear_fields()
            self.toggle_mode()
            
        except sqlite3.IntegrityError:
            self.show_message("Nome de usuário já existe! 😅", "error")
        except sqlite3.Error as e:
            self.show_message(f"Erro ao criar conta: {e}", "error")
    
    def hash_password(self, password):
        """Hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_message(self, message, msg_type):
        """Exibe mensagem colorida"""
        colors = {
            'success': '#6BCF7F',
            'error': '#FF6B9D',
            'info': '#4D96FF'
        }
        
        self.status_label.config(
            text=message,
            fg=colors.get(msg_type, '#666')
        )
        
        # Limpar após 3 segundos
        self.root.after(3000, lambda: self.status_label.config(text=""))
    
    def show_welcome_screen(self, username, nome_completo):
        """Tela de boas-vindas"""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Bem-vindo!")
        welcome_window.geometry("350x400")
        welcome_window.configure(bg='#FFD93D')
        welcome_window.resizable(False, False)
        
        # Centralizar
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        
        x = self.root.winfo_x() + 25
        y = self.root.winfo_y() + 100
        welcome_window.geometry(f"350x400+{x}+{y}")
        
        # Container
        container = tk.Frame(welcome_window, bg='white', relief='raised', bd=2)
        container.pack(expand=True, fill='both', padx=15, pady=15)
        
        # Confetes
        tk.Label(container, text="🎉🎊🌟✨💝", 
                font=('Arial', 14), fg='#FF6B9D', bg='white').pack(pady=10)
        
        # Ícone
        tk.Label(container, text="🌟", 
                font=('Arial', 40), fg='#FFD93D', bg='white').pack(pady=10)
        
        # Título
        tk.Label(container, text="BEM-VINDO!", 
                font=('Comic Sans MS', 18, 'bold'), 
                fg='#FF6B9D', bg='white').pack()
        
        # Nome
        tk.Label(container, text=f"Olá, {nome_completo}! 👋", 
                font=('Arial', 12, 'bold'), 
                fg='#4D96FF', bg='white').pack(pady=10)
        
        # Mensagem
        tk.Label(container, 
                text="🌟 Você faz parte de algo especial!\n💝 Obrigado por fazer a diferença!", 
                font=('Arial', 10), fg='#666', bg='white',
                justify='center').pack(pady=20)
        
        # Botão continuar
        tk.Button(container, text="🚀 Continuar",
                 font=('Arial', 11, 'bold'),
                 bg='#6BCF7F', fg='white',
                 relief='flat', pady=8,
                 command=lambda: self.continue_to_main(welcome_window)).pack(pady=20, padx=50, fill='x')
    
    def continue_to_main(self, welcome_window):
        """Fecha todas as janelas e abre o main.py"""
        welcome_window.destroy()  # Fecha a janela de boas-vindas
        self.root.destroy()       # Fecha a janela principal de login
        subprocess.Popen(["python", "main.py"])  # Abre o arquivo main.py
    
    def run(self):
        """Executa a aplicação"""
        try:
            print("🎪 Sistema Criança Esperança iniciado!")
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro crítico: {e}")
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

# Executar aplicação
if __name__ == "__main__":
    app = CriancaEsperancaLogin()
    app.run()
