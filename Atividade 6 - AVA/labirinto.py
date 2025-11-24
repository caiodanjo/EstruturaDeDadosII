import tkinter as tk
from tkinter import messagebox
from collections import deque

# --- Configurações da Grade e Cores ---
class Configuracoes:
    # Tamanho da grade (colunas x linhas)
    COLUNAS = 30
    LINHAS = 20
    # Tamanho de cada célula em pixels
    TAMANHO_CELULA = 25
    # Tempo de atraso para a animação do BFS em milissegundos
    TEMPO_ANIMACAO_MS = 50

    # Paleta de Cores
    CORES = {
        'Parede': "#1E3A5F",    # Azul Escuro
        'Caminho': "#FFFFFF",   # Branco
        'Inicio': "#4CAF50",    # Verde
        'Fim': "#F44336",       # Vermelho
        'Fronteira': "#AED6F1", # Azul Claro (Na Fila)
        'Visitado': "#D6EAF8",  # Azul Pálido (Já Visitado)
        'Caminho Final': "#FFD700", # Dourado
    }
    
    # Mapeamento de Ferramenta para Caractere e Cor
    FERRAMENTAS = {
        'Parede': {'char': '#', 'cor': CORES['Parede'], 'label': 'Parede (#)'},
        'Caminho': {'char': ' ', 'cor': CORES['Caminho'], 'label': 'Caminho ( )'},
        'Inicio': {'char': 'S', 'cor': CORES['Inicio'], 'label': 'Início (S)'},
        'Fim': {'char': 'E', 'cor': CORES['Fim'], 'label': 'Fim (E)'},
    }

class MazeEditorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Solucionador de Labirintos (BFS)")
        
        # Variáveis de Estado da Aplicação
        self.modo_edicao = True
        self.inicio_pos = None
        self.fim_pos = None
        self.job_after = None   # ID para a função agendada do Tkinter (animação)

        # Variáveis do Algoritmo BFS
        self.fila = deque()
        self.visitados = set()
        self.predecessores = {} # predecessor[(l, c)] = (l_origem, c_origem)

        # Inicializa o modelo de dados (matriz 2D)
        self.labirinto = [[' ' for _ in range(Configuracoes.COLUNAS)] for _ in range(Configuracoes.LINHAS)]
        # Inicializa o armazenamento das IDs dos objetos do Canvas
        self.grid_cells = [[None for _ in range(Configuracoes.COLUNAS)] for _ in range(Configuracoes.LINHAS)]

        # Variável para o Radiobutton da ferramenta de edição
        self.tool_var = tk.StringVar(value='Caminho') # Caminho como ferramenta padrão

        self._configurar_gui()
        self.desenhar_grid_inicial()
        self.bind_eventos()

    def _configurar_gui(self):
        # Frame principal que divide Canvas e Controles
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # --- Canvas para o Labirinto (Grid) ---
        self.canvas = tk.Canvas(main_frame, 
                                width=Configuracoes.COLUNAS * Configuracoes.TAMANHO_CELULA, 
                                height=Configuracoes.LINHAS * Configuracoes.TAMANHO_CELULA, 
                                bg=Configuracoes.CORES['Caminho'], 
                                bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10)

        # --- Frame para os Controles (Toolbox) ---
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Título
        tk.Label(control_frame, text="Modo Edição", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Radiobuttons para Seleção de Ferramenta
        self.radio_buttons = []
        for tool_name, tool_data in Configuracoes.FERRAMENTAS.items():
            rb = tk.Radiobutton(control_frame, 
                                text=tool_data['label'], 
                                variable=self.tool_var, 
                                value=tool_name, 
                                anchor='w')
            rb.pack(fill='x', padx=5, pady=2)
            self.radio_buttons.append(rb)

        # Separador
        tk.Frame(control_frame, height=2, bg="gray").pack(fill='x', pady=10)
        
        # Botões de Ação
        self.btn_iniciar = tk.Button(control_frame, text="Iniciar Busca (BFS)", command=self.iniciar_busca, bg='#4CAF50', fg='white')
        self.btn_iniciar.pack(fill='x', padx=5, pady=5)
        
        self.btn_resetar = tk.Button(control_frame, text="Resetar Busca", command=self.resetar_busca, bg='#FFA500', fg='white')
        self.btn_resetar.pack(fill='x', padx=5, pady=5)

        self.btn_limpar = tk.Button(control_frame, text="Limpar Labirinto", command=self.limpar_labirinto, bg='#F44336', fg='white')
        self.btn_limpar.pack(fill='x', padx=5, pady=5)
        
        # Status
        tk.Label(control_frame, text="Status:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.status_label = tk.Label(control_frame, text="Pronto para Edição", fg="blue")
        self.status_label.pack()

    def desenhar_grid_inicial(self):
        """Desenha todos os retângulos no Canvas e armazena suas IDs."""
        for r in range(Configuracoes.LINHAS):
            for c in range(Configuracoes.COLUNAS):
                x1 = c * Configuracoes.TAMANHO_CELULA
                y1 = r * Configuracoes.TAMANHO_CELULA
                x2 = x1 + Configuracoes.TAMANHO_CELULA
                y2 = y1 + Configuracoes.TAMANHO_CELULA
                
                # Desenha o retângulo inicial (Caminho)
                cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                       fill=Configuracoes.CORES['Caminho'], 
                                                       outline="#CCCCCC") # Borda cinza clara
                self.grid_cells[r][c] = cell_id

    def bind_eventos(self):
        """Configura os manipuladores de eventos do mouse."""
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)

    def on_canvas_click(self, event):
        """Manipulador de clique (Button-1)."""
        if self.modo_edicao:
            col = event.x // Configuracoes.TAMANHO_CELULA
            row = event.y // Configuracoes.TAMANHO_CELULA
            self.editar_celula(row, col)

    def on_canvas_drag(self, event):
        """Manipulador de arrasto (B1-Motion)."""
        if self.modo_edicao:
            col = event.x // Configuracoes.TAMANHO_CELULA
            row = event.y // Configuracoes.TAMANHO_CELULA
            # Verifica se a posição é válida dentro da grade
            if 0 <= row < Configuracoes.LINHAS and 0 <= col < Configuracoes.COLUNAS:
                self.editar_celula(row, col)

    def editar_celula(self, row, col):
        """Atualiza a célula no modelo de dados e visualmente."""
        tool_name = self.tool_var.get()
        tool_data = Configuracoes.FERRAMENTAS.get(tool_name)
        
        if not tool_data:
            return

        novo_char = tool_data['char']
        
        # Se a célula atual é a mesma que queremos desenhar, não faz nada
        if self.labirinto[row][col] == novo_char and novo_char not in ('S', 'E'):
            return

        # 1. Lidar com a regra de 'S' e 'E' únicos
        if novo_char == 'S':
            if self.inicio_pos and self.inicio_pos != (row, col):
                # Limpa o 'S' antigo
                r_old, c_old = self.inicio_pos
                self._atualizar_celula_visual(r_old, c_old, ' ', Configuracoes.CORES['Caminho'])
                self.labirinto[r_old][c_old] = ' '
            self.inicio_pos = (row, col)
        elif novo_char == 'E':
            if self.fim_pos and self.fim_pos != (row, col):
                # Limpa o 'E' antigo
                r_old, c_old = self.fim_pos
                self._atualizar_celula_visual(r_old, c_old, ' ', Configuracoes.CORES['Caminho'])
                self.labirinto[r_old][c_old] = ' '
            self.fim_pos = (row, col)
        
        # Se estamos apagando um 'S' ou 'E' (colocando 'Caminho'), atualiza a posição armazenada E limpa o texto
        elif self.labirinto[row][col] == 'S':
            self.inicio_pos = None
            self._limpar_texto_celula(row, col) # CORREÇÃO: Limpar o texto ao apagar 'S'
        elif self.labirinto[row][col] == 'E':
            self.fim_pos = None
            self._limpar_texto_celula(row, col) # CORREÇÃO: Limpar o texto ao apagar 'E'

        # 2. Atualizar o modelo de dados e a visualização
        self.labirinto[row][col] = novo_char
        self._atualizar_celula_visual(row, col, novo_char, tool_data['cor'])
        
    def _limpar_texto_celula(self, row, col):
        """Remove o objeto de texto ('S' ou 'E') da célula no Canvas."""
        # Deleta qualquer objeto no canvas que tenha a tag específica de texto
        self.canvas.delete(f"text_{row}_{col}")
        
    def _atualizar_celula_visual(self, row, col, char, cor):
        """Atualiza a cor da célula no Canvas."""
        cell_id = self.grid_cells[row][col]
        self.canvas.itemconfig(cell_id, fill=cor)
        
        # 1. Remove texto antigo (sempre removemos antes de desenhar novo)
        self._limpar_texto_celula(row, col)
        
        # 2. Adicionar texto para 'S' e 'E', se aplicável
        if char in ('S', 'E'):
            # Calcula o centro da célula para posicionar o texto
            center_x = col * Configuracoes.TAMANHO_CELULA + Configuracoes.TAMANHO_CELULA / 2
            center_y = row * Configuracoes.TAMANHO_CELULA + Configuracoes.TAMANHO_CELULA / 2
            
            # Adiciona novo texto com uma tag única
            text_id = self.canvas.create_text(center_x, center_y, text=char, fill='black', font=('Arial', 10, 'bold'), tags=f"text_{row}_{col}")
            # Garante que o texto está acima do retângulo
            self.canvas.tag_raise(text_id)

    # --- Lógica de Busca BFS ---

    def iniciar_busca(self):
        """Prepara o estado e inicia a animação do BFS."""
        if not self.inicio_pos or not self.fim_pos:
            messagebox.showerror("Erro", "O labirinto deve ter um ponto de Início (S) e um de Fim (E)!")
            return

        # Desabilita o modo de edição e controles
        self.modo_edicao = False
        self._set_controles_edicao(False)
        self.status_label.config(text="Simulação BFS em progresso...", fg="orange")
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_resetar.config(state=tk.NORMAL)

        # Garante que os resultados de uma busca anterior sejam limpos
        self.resetar_busca(apenas_logica=True)
        
        # Inicializa BFS com a posição de início
        self.fila.append(self.inicio_pos)
        self.visitados.add(self.inicio_pos)
        # O predecessor de 'S' pode ser None, mas o set 'visitados' já o contém.

        # Inicia a animação agendando o primeiro passo
        self.job_after = self.root.after(Configuracoes.TEMPO_ANIMACAO_MS, self.processar_passo_bfs)

    def processar_passo_bfs(self):
        """Executa um único passo do algoritmo BFS e agenda o próximo."""
        self.job_after = None # Limpa o job ID antes de iniciar um novo

        if not self.fila:
            self.status_label.config(text="Caminho não encontrado!", fg="red")
            self._set_controles_edicao(True)
            self.btn_iniciar.config(state=tk.NORMAL)
            return

        # 1. Retira o item atual da fila
        r, c = self.fila.popleft()
        
        # Se for o 'E', paramos a busca
        if (r, c) == self.fim_pos:
            self.status_label.config(text="Caminho encontrado!", fg="green")
            self.reconstruir_caminho()
            self._set_controles_edicao(True)
            self.btn_iniciar.config(state=tk.NORMAL)
            return

        # 2. Pinta a célula atual como 'Visitada', a menos que seja 'S'
        if (r, c) != self.inicio_pos:
            self.canvas.itemconfig(self.grid_cells[r][c], fill=Configuracoes.CORES['Visitado'])

        # 3. Explora os vizinhos (cima, baixo, esquerda, direita)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in movimentos:
            nr, nc = r + dr, c + dc
            vizinho_pos = (nr, nc)
            
            # 4. Verifica se o vizinho é válido e não visitado
            if (0 <= nr < Configuracoes.LINHAS and 
                0 <= nc < Configuracoes.COLUNAS and 
                self.labirinto[nr][nc] != Configuracoes.FERRAMENTAS['Parede']['char'] and 
                vizinho_pos not in self.visitados):

                # Marca como visitado e salva o predecessor
                self.visitados.add(vizinho_pos)
                self.predecessores[vizinho_pos] = (r, c)
                
                # Adiciona à fila e pinta como 'Fronteira' (a menos que seja 'E')
                self.fila.append(vizinho_pos)
                if vizinho_pos != self.fim_pos:
                    self.canvas.itemconfig(self.grid_cells[nr][nc], fill=Configuracoes.CORES['Fronteira'])
                    
        # 5. Agenda o próximo passo
        self.job_after = self.root.after(Configuracoes.TEMPO_ANIMACAO_MS, self.processar_passo_bfs)

    def reconstruir_caminho(self):
        """Rastreia e colore o caminho mais curto encontrado de E até S."""
        caminho_cor = Configuracoes.CORES['Caminho Final']
        
        # Inicia no 'E'
        passo_atual = self.fim_pos
        
        # Rastreia de volta usando o dicionário de predecessores
        while passo_atual and passo_atual != self.inicio_pos:
            r, c = passo_atual
            
            # Pinta apenas se não for o 'E' (já está vermelho)
            if passo_atual != self.fim_pos:
                self.canvas.itemconfig(self.grid_cells[r][c], fill=caminho_cor)
            
            # Move para o predecessor
            passo_atual = self.predecessores.get(passo_atual)

    def resetar_busca(self, apenas_logica=False):
        """Para a animação e limpa as cores de simulação, mantendo o labirinto."""
        # 1. Cancela a animação, se estiver rodando
        if self.job_after:
            self.root.after_cancel(self.job_after)
            self.job_after = None

        # 2. Limpa o estado lógico do BFS
        self.fila.clear()
        self.visitados.clear()
        self.predecessores.clear()
        
        if apenas_logica:
            return

        # 3. Restaura as cores originais da grade (mantendo 'Parede', 'S', 'E')
        for r in range(Configuracoes.LINHAS):
            for c in range(Configuracoes.COLUNAS):
                char = self.labirinto[r][c]
                cell_id = self.grid_cells[r][c]
                cor = Configuracoes.FERRAMENTAS.get(char, {}).get('cor', Configuracoes.CORES['Caminho'])
                
                # Verifica se a célula tem um estado de busca (visitado, fronteira, final)
                is_search_state = cor in [Configuracoes.CORES['Visitado'], Configuracoes.CORES['Fronteira'], Configuracoes.CORES['Caminho Final']]
                
                if is_search_state or char in (' ', '#'):
                    # Recalcula a cor base
                    if char == '#':
                        cor = Configuracoes.CORES['Parede']
                    elif char == 'S':
                        cor = Configuracoes.CORES['Inicio']
                    elif char == 'E':
                        cor = Configuracoes.CORES['Fim']
                    else: # ' '
                        cor = Configuracoes.CORES['Caminho']

                    self.canvas.itemconfig(cell_id, fill=cor)

        # 4. Restaura o modo de edição e controles
        self.status_label.config(text="Pronto para Edição", fg="blue")
        self._set_controles_edicao(True)
        self.btn_iniciar.config(state=tk.NORMAL)

    def limpar_labirinto(self):
        """Limpa toda a grade para o estado 'Caminho'."""
        self.resetar_busca() # Limpa o estado da busca primeiro
        
        # Limpa o modelo de dados e as posições de 'S' e 'E'
        self.labirinto = [[' ' for _ in range(Configuracoes.COLUNAS)] for _ in range(Configuracoes.LINHAS)]
        self.inicio_pos = None
        self.fim_pos = None

        # Limpa a visualização
        for r in range(Configuracoes.LINHAS):
            for c in range(Configuracoes.COLUNAS):
                cell_id = self.grid_cells[r][c]
                self.canvas.itemconfig(cell_id, fill=Configuracoes.CORES['Caminho'])
                
                # CORREÇÃO: Remove o objeto de texto 'S' ou 'E' da célula
                self._limpar_texto_celula(r, c)

        self.status_label.config(text="Labirinto Limpo. Pronto para desenhar.", fg="black")

    def _set_controles_edicao(self, enabled):
        """Habilita/desabilita controles de edição."""
        self.modo_edicao = enabled
        state = tk.NORMAL if enabled else tk.DISABLED
        
        for rb in self.radio_buttons:
            rb.config(state=state)
        
        self.btn_limpar.config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeEditorGUI(root)
    # Garante que a aplicação feche corretamente se houver um after() rodando
    def on_closing():
        if app.job_after:
            root.after_cancel(app.job_after)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
