import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class CriancaEsperancaManager:
    def __init__(self, user_data):
        self.user_data = user_data  # Dados do usuário logado
        self.root = tk.Tk()
        self.root.title("Criança Esperança - Sistema de Gerenciamento")
        self.root.geometry("1200x800")
        self.root.configure(bg='#FFD93D')
        
        # Centralizar janela
        self.center_window()
        
        # Database
        self.init_database()
        
        # Variáveis
        self.current_section = "dashboard"
        
        # Interface
        self.create_main_interface()
        
        # Carregar dashboard inicial
        self.show_dashboard()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def init_database(self):
        """Inicializa tabelas do sistema de gerenciamento"""
        try:
            self.conn = sqlite3.connect("crianca_esperanca.db")
            cursor = self.conn.cursor()
            
            # Tabela de projetos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projetos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    data_inicio DATE,
                    data_fim DATE,
                    status TEXT DEFAULT 'Ativo',
                    responsavel TEXT,
                    orcamento REAL DEFAULT 0,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de voluntários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS voluntarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT,
                    telefone TEXT,
                    area_interesse TEXT,
                    disponibilidade TEXT,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de beneficiários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS beneficiarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER,
                    responsavel TEXT,
                    telefone_responsavel TEXT,
                    endereco TEXT,
                    situacao TEXT,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de atividades
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS atividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    projeto_id INTEGER,
                    data_atividade DATE,
                    local TEXT,
                    participantes INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'Planejada',
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (projeto_id) REFERENCES projetos (id)
                )
            ''')
            
            self.conn.commit()
            print("✅ Banco de gerenciamento inicializado!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro no banco: {e}")
    
    def create_main_interface(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header()
        
        # Menu lateral
        self.create_sidebar()
        
        # Área de conteúdo
        self.content_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=1)
        self.content_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#FF6B9D', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Logo e título
        logo_frame = tk.Frame(header_frame, bg='#FF6B9D')
        logo_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(logo_frame, text="🎪", font=('Arial', 24), 
                bg='#FF6B9D', fg='white').pack(side='left')
        
        tk.Label(logo_frame, text="CRIANÇA ESPERANÇA", 
                font=('Comic Sans MS', 18, 'bold'),
                bg='#FF6B9D', fg='white').pack(side='left', padx=(10, 0))
        
        # Info do usuário
        user_frame = tk.Frame(header_frame, bg='#FF6B9D')
        user_frame.pack(side='right', padx=20, pady=10)
        
        tk.Label(user_frame, text=f"👤 {self.user_data.get('nome', 'Usuário')}", 
                font=('Arial', 12, 'bold'),
                bg='#FF6B9D', fg='white').pack(anchor='e')
        
        tk.Label(user_frame, text=f"📅 {datetime.now().strftime('%d/%m/%Y')}", 
                font=('Arial', 10),
                bg='#FF6B9D', fg='white').pack(anchor='e')
    
    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.main_frame, bg='#4D96FF', width=200)
        sidebar_frame.pack(side='left', fill='y')
        sidebar_frame.pack_propagate(False)
        
        # Título do menu
        tk.Label(sidebar_frame, text="🌟 MENU PRINCIPAL", 
                font=('Arial', 12, 'bold'),
                bg='#4D96FF', fg='white').pack(pady=20)
        
        # Botões do menu
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📋 Projetos", "projetos"),
            ("👥 Voluntários", "voluntarios"),
            ("👶 Beneficiários", "beneficiarios"),
            ("🎯 Atividades", "atividades"),
        ]
        
        self.menu_buttons = {}
        for text, section in menu_items:
            btn = tk.Button(sidebar_frame, text=text,
                           font=('Arial', 11, 'bold'),
                           bg='white', fg='#4D96FF',
                           relief='flat', pady=10,
                           command=lambda s=section: self.show_section(s))
            btn.pack(fill='x', padx=10, pady=5)
            self.menu_buttons[section] = btn
        
        # Botão sair
        tk.Button(sidebar_frame, text="🚪 Sair",
                 font=('Arial', 11, 'bold'),
                 bg='#FF6B9D', fg='white',
                 relief='flat', pady=10,
                 command=self.logout).pack(side='bottom', fill='x', padx=10, pady=10)
    
    def show_section(self, section):
        """Mostra seção selecionada com destaque visual"""
        self.current_section = section
        
        # Resetar cores dos botões
        for btn_section, btn in self.menu_buttons.items():
            if btn_section == section:
                btn.configure(bg='#FFD93D', fg='#333')
            else:
                btn.configure(bg='white', fg='#4D96FF')
        
        # Limpar conteúdo atual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar seção correspondente
        if section == "dashboard":
            self.show_dashboard()
        elif section == "projetos":
            self.show_projetos()
        elif section == "voluntarios":
            self.show_voluntarios()
        elif section == "beneficiarios":
            self.show_beneficiarios()
        elif section == "atividades":
            self.show_atividades()
    
    def show_dashboard(self):
        """Dashboard principal com melhorias visuais"""
        # Título
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(title_frame, text="📊 DASHBOARD", 
                font=('Comic Sans MS', 20, 'bold'),
                fg='#FF6B9D', bg='white').pack(anchor='w')
        
        tk.Label(title_frame, text="Visão geral do sistema", 
                font=('Arial', 12),
                fg='#666', bg='white').pack(anchor='w')
        
        # Cards de estatísticas
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Obter estatísticas
        stats = self.get_dashboard_stats()
        
        # Criar cards com hover effect
        cards_data = [
            ("🎯 Projetos Ativos", stats['projetos'], "#4D96FF"),
            ("👥 Voluntários", stats['voluntarios'], "#6BCF7F"),
            ("👶 Beneficiários", stats['beneficiarios'], "#FF6B9D"),
            ("📅 Atividades", stats['atividades'], "#FFD93D")
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = tk.Frame(stats_frame, bg=color, relief='raised', bd=2, cursor='hand2')
            card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Efeito hover
            def on_enter(event, card=card, color=color):
                card.configure(relief='ridge', bd=3)
            
            def on_leave(event, card=card, color=color):
                card.configure(relief='raised', bd=2)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            tk.Label(card, text=str(value), 
                    font=('Arial', 24, 'bold'),
                    bg=color, fg='white').pack(pady=10)
            
            tk.Label(card, text=title, 
                    font=('Arial', 10, 'bold'),
                    bg=color, fg='white').pack(pady=(0, 10))
        
        # Atividades recentes com melhoria visual
        recent_frame = tk.Frame(self.content_frame, bg='white')
        recent_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(recent_frame, text="📋 Atividades Recentes", 
                font=('Arial', 14, 'bold'),
                fg='#333', bg='white').pack(anchor='w', pady=(0, 10))
        
        # Lista de atividades recentes
        self.create_recent_activities_list(recent_frame)
    
    def get_dashboard_stats(self):
        """Obtém estatísticas para o dashboard"""
        try:
            cursor = self.conn.cursor()
            
            # Contar projetos ativos
            cursor.execute("SELECT COUNT(*) FROM projetos WHERE status = 'Ativo'")
            projetos = cursor.fetchone()[0]
            
            # Contar voluntários
            cursor.execute("SELECT COUNT(*) FROM voluntarios")
            voluntarios = cursor.fetchone()[0]
            
            # Contar beneficiários
            cursor.execute("SELECT COUNT(*) FROM beneficiarios")
            beneficiarios = cursor.fetchone()[0]
            
            # Contar atividades
            cursor.execute("SELECT COUNT(*) FROM atividades")
            atividades = cursor.fetchone()[0]
            
            return {
                'projetos': projetos,
                'voluntarios': voluntarios,
                'beneficiarios': beneficiarios,
                'atividades': atividades
            }
            
        except sqlite3.Error:
            return {'projetos': 0, 'voluntarios': 0, 'beneficiarios': 0, 'atividades': 0}
    
    def create_recent_activities_list(self, parent):
        """Cria lista de atividades recentes com melhorias visuais"""
        list_frame = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        list_frame.pack(fill='both', expand=True)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT titulo, data_atividade, status 
                FROM atividades 
                ORDER BY data_criacao DESC 
                LIMIT 5
            ''')
            
            activities = cursor.fetchall()
            
            if not activities:
                empty_frame = tk.Frame(list_frame, bg='#f8f9fa')
                empty_frame.pack(expand=True, fill='both')
                
                tk.Label(empty_frame, text="📝", font=('Arial', 40), 
                        fg='#ccc', bg='#f8f9fa').pack(pady=(50, 10))
                
                tk.Label(empty_frame, text="Nenhuma atividade cadastrada ainda", 
                        font=('Arial', 12),
                        fg='#666', bg='#f8f9fa').pack()
            else:
                for i, (titulo, data_atividade, status) in enumerate(activities):
                    item_frame = tk.Frame(list_frame, bg='white', relief='flat', bd=1)
                    item_frame.pack(fill='x', padx=10, pady=5)
                    
                    # Efeito hover nas atividades
                    def on_enter_item(event, frame=item_frame):
                        frame.configure(bg='#f0f8ff', relief='solid')
                    
                    def on_leave_item(event, frame=item_frame):
                        frame.configure(bg='white', relief='flat')
                    
                    item_frame.bind("<Enter>", on_enter_item)
                    item_frame.bind("<Leave>", on_leave_item)
                    
                    # Status color indicator
                    status_colors = {
                        'Planejada': '#FFD93D',
                        'Em Andamento': '#4D96FF',
                        'Realizada': '#6BCF7F',
                        'Cancelada': '#FF6B9D'
                    }
                    
                    status_frame = tk.Frame(item_frame, bg=status_colors.get(status, '#ccc'), width=5)
                    status_frame.pack(side='left', fill='y')
                    
                    content_frame = tk.Frame(item_frame, bg='white')
                    content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=8)
                    
                    tk.Label(content_frame, text=f"📅 {titulo}", 
                            font=('Arial', 11, 'bold'),
                            fg='#333', bg='white').pack(anchor='w')
                    
                    tk.Label(content_frame, text=f"Data: {data_atividade or 'Não definida'} • Status: {status}", 
                            font=('Arial', 9),
                            fg='#666', bg='white').pack(anchor='w')
                    
        except sqlite3.Error as e:
            tk.Label(list_frame, text=f"Erro ao carregar atividades: {e}", 
                    fg='red', bg='#f8f9fa').pack(pady=50)
    
    def show_projetos(self):
        """Seção de gerenciamento de projetos"""
        self.create_crud_section("Projetos", "projetos", [
            ("Nome", "nome", "text", 150),
            ("Descrição", "descricao", "text", 200),
            ("Data Início", "data_inicio", "date", 100),
            ("Data Fim", "data_fim", "date", 100),
            ("Status", "status", "combo", 80, ["Ativo", "Pausado", "Concluído"]),
            ("Responsável", "responsavel", "text", 120),
            ("Orçamento", "orcamento", "number", 100)
        ])
    
    def show_voluntarios(self):
        """Seção de gerenciamento de voluntários"""
        self.create_crud_section("Voluntários", "voluntarios", [
            ("Nome", "nome", "text", 150),
            ("Email", "email", "text", 200),
            ("Telefone", "telefone", "text", 120),
            ("Área de Interesse", "area_interesse", "text", 150),
            ("Disponibilidade", "disponibilidade", "text", 150)
        ])
    
    def show_beneficiarios(self):
        """Seção de gerenciamento de beneficiários"""
        self.create_crud_section("Beneficiários", "beneficiarios", [
            ("Nome", "nome", "text", 150),
            ("Idade", "idade", "number", 80),
            ("Responsável", "responsavel", "text", 150),
            ("Telefone Responsável", "telefone_responsavel", "text", 140),
            ("Endereço", "endereco", "text", 200),
            ("Situação", "situacao", "text", 120)
        ])
    
    def show_atividades(self):
        """Seção de gerenciamento de atividades"""
        self.create_crud_section("Atividades", "atividades", [
            ("Título", "titulo", "text", 150),
            ("Descrição", "descricao", "text", 200),
            ("Data da Atividade", "data_atividade", "date", 120),
            ("Local", "local", "text", 150),
            ("Participantes", "participantes", "number", 100),
            ("Status", "status", "combo", 120, ["Planejada", "Em Andamento", "Realizada", "Cancelada"])
        ])
    
    def create_crud_section(self, title, table_name, fields):
        """Cria seção CRUD genérica com melhorias"""
        # Título com barra de pesquisa
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(side='left', fill='y')
        
        tk.Label(title_frame, text=f"📋 {title.upper()}", 
                font=('Arial', 20, 'bold'),
                fg='#FF6B9D', bg='white').pack(anchor='w')
        
        # Contador de registros
        count = self.get_record_count(table_name)
        tk.Label(title_frame, text=f"{count} registro(s) encontrado(s)", 
                font=('Arial', 10),
                fg='#666', bg='white').pack(anchor='w')
        
        # Botões de ação no topo
        btn_top_frame = tk.Frame(header_frame, bg='white')
        btn_top_frame.pack(side='right', fill='y')
        
        tk.Button(btn_top_frame, text=f"➕ Adicionar {title[:-1]}", 
                 font=('Arial', 10, 'bold'),
                 bg='#6BCF7F', fg='white', cursor='hand2',
                 command=lambda: self.open_add_dialog(table_name, fields)).pack(side='right', padx=5)
        
        # Barra de pesquisa simples
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Pesquisar:", 
                font=('Arial', 10, 'bold'),
                bg='white', fg='#333').pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=('Arial', 10), width=30)
        search_entry.pack(side='left', padx=(5, 10))
        
        tk.Button(search_frame, text="Buscar",
                 font=('Arial', 9), bg='#4D96FF', fg='white',
                 command=lambda: self.search_records(table_name, fields)).pack(side='left')
        
        # Frame para tabela com scrollbar
        table_frame = tk.Frame(self.content_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Criar tabela com estilo melhorado
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=25)
        style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'))
        
        columns = [field[1] for field in fields]
        self.current_tree = ttk.Treeview(table_frame, columns=columns, show='headings', 
                                        height=12, style="Custom.Treeview")
        
        # Configurar colunas com larguras específicas
        for field in fields:
            field_name = field[1]
            field_label = field[0]
            field_width = field[3] if len(field) > 3 else 120
            
            self.current_tree.heading(field_name, text=field_label)
            self.current_tree.column(field_name, width=field_width, minwidth=80)
        
        # Frame para scrollbars
        scrollbar_v = ttk.Scrollbar(table_frame, orient='vertical', command=self.current_tree.yview)
        scrollbar_h = ttk.Scrollbar(table_frame, orient='horizontal', command=self.current_tree.xview)
        
        self.current_tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Posicionar elementos
        self.current_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar redimensionamento
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Carregar dados
        self.load_table_data(self.current_tree, table_name, fields)
        
        # Botões de ação com melhor organização
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text="✏️ Editar", 
                 bg='#4D96FF', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2', padx=15, pady=5,
                 command=lambda: self.edit_selected(self.current_tree, table_name, fields)).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ Excluir", 
                 bg='#FF6B9D', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2', padx=15, pady=5,
                 command=lambda: self.delete_selected(self.current_tree, table_name)).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", 
                 bg='#FFD93D', fg='black', font=('Arial', 10, 'bold'),
                 cursor='hand2', padx=15, pady=5,
                 command=lambda: self.load_table_data(self.current_tree, table_name, fields)).pack(side='left', padx=5)
        
        # Informações de seleção
        self.selection_label = tk.Label(btn_frame, text="Nenhum item selecionado", 
                                       font=('Arial', 9), fg='#666', bg='white')
        self.selection_label.pack(side='right', padx=10)
        
        # Bind para atualizar seleção
        self.current_tree.bind('<<TreeviewSelect>>', self.on_selection_change)
    
    def get_record_count(self, table_name):
        """Obtém contagem de registros"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0
    
    def on_selection_change(self, event):
        """Atualiza label de seleção"""
        if hasattr(self, 'selection_label') and hasattr(self, 'current_tree'):
            selection = self.current_tree.selection()
            if selection:
                self.selection_label.config(text=f"1 item selecionado")
            else:
                self.selection_label.config(text="Nenhum item selecionado")
    
    def search_records(self, table_name, fields):
        """Busca registros (implementação básica)"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_table_data(self.current_tree, table_name, fields)
            return
        
        try:
            # Limpar tabela
            for item in self.current_tree.get_children():
                self.current_tree.delete(item)
            
            cursor = self.conn.cursor()
            columns = [field[1] for field in fields]
            
            # Busca simples no primeiro campo de texto
            text_fields = [field[1] for field in fields if field[2] == 'text']
            if text_fields:
                search_field = text_fields[0]  # Primeiro campo de texto
                cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name} WHERE {search_field} LIKE ?", 
                              (f'%{search_term}%',))
                
                for row in cursor.fetchall():
                    display_values = row[1:]
                    self.current_tree.insert('', 'end', values=display_values, tags=(row[0],))
                    
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro na pesquisa: {e}")
    
    def load_table_data(self, tree, table_name, fields):
        """Carrega dados na tabela"""
        try:
            # Limpar tabela
            for item in tree.get_children():
                tree.delete(item)
            
            cursor = self.conn.cursor()
            columns = [field[1] for field in fields]
            cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name}")
            
            # Cores alternadas para as linhas
            for i, row in enumerate(cursor.fetchall()):
                display_values = row[1:]
                tags = (row[0], 'evenrow' if i % 2 == 0 else 'oddrow')
                tree.insert('', 'end', values=display_values, tags=tags)
            
            # Configurar cores das linhas
            tree.tag_configure('evenrow', background='#f8f9fa')
            tree.tag_configure('oddrow', background='white')
                
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def open_add_dialog(self, table_name, fields):
        """Abre diálogo para adicionar registro"""
        self.open_record_dialog(table_name, fields, "Adicionar", None)
    
    def open_record_dialog(self, table_name, fields, mode, record_data=None):
        """Diálogo unificado para adicionar/editar registros"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{mode} {table_name[:-1].title()}")
        dialog.geometry("500x700")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (700 // 2)
        dialog.geometry(f"500x700+{x}+{y}")
        
        # Header do diálogo
        header_frame = tk.Frame(dialog, bg='#FF6B9D', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        icon = "✏️" if mode == "Editar" else "➕"
        tk.Label(header_frame, text=f"{icon} {mode} {table_name[:-1].title()}", 
                font=('Arial', 16, 'bold'), fg='white',
                bg='#FF6B9D').pack(expand=True)
        
        # Frame principal com scroll
        main_frame = tk.Frame(dialog, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Campos do formulário
        entries = {}
        for i, field_info in enumerate(fields):
            field_label = field_info[0]
            field_name = field_info[1]
            field_type = field_info[2]
            
            # Frame para cada campo
            field_frame = tk.Frame(scrollable_frame, bg='white')
            field_frame.pack(fill='x', pady=10)
            
            # Label
            tk.Label(field_frame, text=f"{field_label}:", 
                    font=('Arial', 11, 'bold'),
                    bg='white', fg='#333').pack(anchor='w', pady=(0, 5))
            
            # Campo de entrada
            if field_type == "combo":
                options = field_info[4] if len(field_info) > 4 else []
                var = tk.StringVar()
                combo = ttk.Combobox(field_frame, textvariable=var, values=options, 
                                   font=('Arial', 11), state='readonly', width=50)
                combo.pack(fill='x', pady=(0, 5))
                entries[field_name] = var
                
                # Definir valor se editando
                if record_data and field_name in record_data:
                    var.set(record_data[field_name])
                    
            elif field_type in ["text", "number", "date"]:
                entry = tk.Entry(field_frame, font=('Arial', 11), relief='solid', bd=1, width=50)
                entry.pack(fill='x', pady=(0, 5))
                entries[field_name] = entry
                
                # Placeholder para campos de data
                if field_type == "date":
                    placeholder = "DD/MM/AAAA"
                    if not record_data or not record_data.get(field_name):
                        entry.insert(0, placeholder)
                        entry.config(fg='gray')
                    
                    def on_focus_in(event, entry=entry, placeholder=placeholder):
                        if entry.get() == placeholder:
                            entry.delete(0, tk.END)
                            entry.config(fg='black')
                    
                    def on_focus_out(event, entry=entry, placeholder=placeholder):
                        if entry.get() == "":
                            entry.insert(0, placeholder)
                            entry.config(fg='gray')
                    
                    entry.bind("<FocusIn>", on_focus_in)
                    entry.bind("<FocusOut>", on_focus_out)
                
                # Definir valor se editando
                if record_data and field_name in record_data and record_data[field_name]:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(record_data[field_name]))
                    entry.config(fg='black')
        
        # Rodapé com botões
        footer_frame = tk.Frame(dialog, bg='#f8f9fa')
        footer_frame.pack(fill='x', side='bottom')
        
        btn_frame = tk.Frame(footer_frame, bg='#f8f9fa')
        btn_frame.pack(pady=15)
        
        # Botão salvar
        save_text = "💾 Atualizar" if mode == "Editar" else "💾 Salvar"
        tk.Button(btn_frame, text=save_text,
                 bg='#6BCF7F', fg='white', font=('Arial', 11, 'bold'),
                 pady=8, padx=20, cursor='hand2',
                 command=lambda: self.save_record(dialog, table_name, fields, entries, record_data)).pack(side='right', padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar",
                 bg='#FF6B9D', fg='white', font=('Arial', 11, 'bold'),
                 pady=8, padx=20, cursor='hand2',
                 command=dialog.destroy).pack(side='right')
        
        # Foco no primeiro campo
        first_entry = list(entries.values())[0]
        if hasattr(first_entry, 'focus'):
            first_entry.focus()
    
    def save_record(self, dialog, table_name, fields, entries, record_data=None):
        """Salva ou atualiza registro no banco"""
        try:
            values = []
            columns = []
            
            # Validação básica
            required_fields = []
            for field_info in fields:
                field_name = field_info[1]
                field_label = field_info[0]
                widget = entries[field_name]
                
                if isinstance(widget, tk.StringVar):
                    value = widget.get().strip()
                else:
                    value = widget.get().strip()
                    # Limpar placeholder
                    if value == "DD/MM/AAAA":
                        value = ""
                
                # Verificar campos obrigatórios (nome/titulo)
                if field_name in ['nome', 'titulo'] and not value:
                    required_fields.append(field_label)
                
                values.append(value if value else None)
                columns.append(field_name)
            
            # Verificar se há campos obrigatórios vazios
            if required_fields:
                messagebox.showwarning("Campos Obrigatórios", 
                                     f"Os seguintes campos são obrigatórios:\n• {chr(10).join(required_fields)}")
                return
            
            cursor = self.conn.cursor()
            
            if record_data:  # Editando
                # UPDATE
                set_clause = ', '.join([f"{col} = ?" for col in columns])
                cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", 
                              values + [record_data['id']])
                success_msg = "Registro atualizado com sucesso! ✅"
            else:  # Adicionando
                # INSERT
                placeholders = ', '.join(['?' for _ in values])
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
                success_msg = "Registro salvo com sucesso! 🎉"
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", success_msg)
            dialog.destroy()
            
            # Recarregar seção atual
            self.show_section(self.current_section)
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
    
    def edit_selected(self, tree, table_name, fields):
        """Edita registro selecionado - FUNÇÃO IMPLEMENTADA"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para editar!")
            return
        
        try:
            # Obter ID do registro usando as tags
            item_tags = tree.item(selection[0])['tags']
            if not item_tags:
                messagebox.showerror("Erro", "Não foi possível identificar o registro!")
                return
            
            record_id = item_tags[0]
            
            # Buscar dados completos do registro
            cursor = self.conn.cursor()
            columns = [field[1] for field in fields]
            cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name} WHERE id = ?", (record_id,))
            
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Erro", "Registro não encontrado!")
                return
            
            # Preparar dados para o diálogo
            record_data = {'id': row[0]}
            for i, field_name in enumerate(columns):
                record_data[field_name] = row[i + 1]
            
            # Abrir diálogo de edição
            self.open_record_dialog(table_name, fields, "Editar", record_data)
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar registro: {e}")
    
    def delete_selected(self, tree, table_name):
        """Exclui registro selecionado com confirmação melhorada"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para excluir!")
            return
        
        # Confirmação com mais detalhes
        item_values = tree.item(selection[0])['values']
        first_value = item_values[0] if item_values else "este registro"
        
        result = messagebox.askyesnocancel(
            "Confirmar Exclusão", 
            f"⚠️ Tem certeza que deseja excluir '{first_value}'?\n\n"
            "Esta ação não pode ser desfeita!",
            icon='warning'
        )
        
        if result:
            try:
                # Obter ID do registro usando as tags
                item_tags = tree.item(selection[0])['tags']
                if item_tags:
                    record_id = item_tags[0]
                    
                    cursor = self.conn.cursor()
                    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
                    self.conn.commit()
                    
                    messagebox.showinfo("Sucesso", "Registro excluído com sucesso! 🗑️")
                    self.show_section(self.current_section)
                else:
                    messagebox.showerror("Erro", "Não foi possível identificar o registro!")
                    
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def logout(self):
        """Sair do sistema com confirmação"""
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema? 🚪"):
            try:
                self.conn.close()
            except:
                pass
            self.root.destroy()
    
    def run(self):
        """Executa o sistema de gerenciamento"""
        try:
            print("🎪 Sistema de Gerenciamento Criança Esperança iniciado!")
            
            # Configurar evento de fechamento
            self.root.protocol("WM_DELETE_WINDOW", self.logout)
            
            # Definir ícone da janela (se disponível)
            try:
                self.root.iconbitmap('icon.ico')  # Opcional
            except:
                pass
            
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro crítico: {e}")
        finally:
            if hasattr(self, 'conn'):
                try:
                    self.conn.close()
                except:
                    pass

# Função para integrar com o sistema de login
def iniciar_gerenciamento(user_data):
    """Inicia o sistema de gerenciamento após login"""
    try:
        manager = CriancaEsperancaManager(user_data)
        manager.run()
    except Exception as e:
        print(f"Erro ao iniciar sistema: {e}")
        messagebox.showerror("Erro", f"Erro ao iniciar sistema: {e}")

# Exemplo de uso (para teste independente)
if __name__ == "__main__":
    # Dados de exemplo do usuário
    user_data_exemplo = {
        'id': 1,
        'username': 'admin',
        'nome': 'Administrador do Sistema'
    }
    
    print("🎪 Iniciando Sistema Criança Esperança...")
    iniciar_gerenciamento(user_data_exemplo)
