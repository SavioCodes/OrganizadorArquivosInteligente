#!/usr/bin/env python3
"""
📁 Organizador de Arquivos Inteligente
=====================================
Automação em Python para organizar arquivos por tipo e data.
Autor: SavioCodes - https://github.com/SavioCodes
Licença: MIT
"""

import os
import shutil
import datetime
from pathlib import Path
import logging
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import json


class FileOrganizer:
    """Classe principal para organização inteligente de arquivos."""
    
    def __init__(self):
        """Inicializa o organizador com configurações padrão."""
        self.file_categories = {
            'documentos': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', 
                          '.xlsx', '.ppt', '.pptx', '.csv', '.ods', '.odp'],
            'imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', 
                       '.webp', '.ico', '.raw', '.psd'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
                      '.m4v', '.3gp', '.mpg', '.mpeg'],
            'audios': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', 
                      '.opus', '.aiff'],
            'compactados': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', 
                           '.tar.gz', '.tar.bz2'],
            'executaveis': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.appimage'],
            'codigo': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', 
                      '.h', '.json', '.xml', '.sql', '.sh', '.bat'],
            'outros': []  # Arquivos que não se encaixam em nenhuma categoria
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Configura o sistema de logging."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('organizador_log.txt', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_file_category(self, file_path: Path) -> str:
        """
        Determina a categoria de um arquivo baseado em sua extensão.
        
        Args:
            file_path (Path): Caminho do arquivo
            
        Returns:
            str: Categoria do arquivo
        """
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return 'outros'
    
    def get_file_date_folder(self, file_path: Path) -> str:
        """
        Obtém a pasta de data baseada na modificação do arquivo.
        
        Args:
            file_path (Path): Caminho do arquivo
            
        Returns:
            str: Pasta no formato 'YYYY/MM'
        """
        try:
            # Usa a data de modificação do arquivo
            timestamp = file_path.stat().st_mtime
            date_obj = datetime.datetime.fromtimestamp(timestamp)
            return f"{date_obj.year}/{date_obj.month:02d}"
        except Exception as e:
            self.logger.error(f"Erro ao obter data do arquivo {file_path}: {e}")
            # Fallback para data atual
            now = datetime.datetime.now()
            return f"{now.year}/{now.month:02d}"
    
    def create_unique_filename(self, destination: Path) -> Path:
        """
        Cria um nome único para evitar sobrescrita.
        
        Args:
            destination (Path): Caminho de destino desejado
            
        Returns:
            Path: Caminho único para o arquivo
        """
        if not destination.exists():
            return destination
        
        # Gera nomes únicos adicionando sufixo numérico
        counter = 1
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def organize_files(self, source_dir: str, destination_dir: str, 
                      progress_callback=None) -> Dict[str, int]:
        """
        Organiza arquivos da pasta origem para a pasta destino.
        
        Args:
            source_dir (str): Diretório de origem
            destination_dir (str): Diretório de destino
            progress_callback: Função callback para atualizar progresso
            
        Returns:
            Dict[str, int]: Estatísticas da organização
        """
        source_path = Path(source_dir)
        destination_path = Path(destination_dir)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Diretório de origem não encontrado: {source_dir}")
        
        # Cria diretório de destino se não existir
        destination_path.mkdir(parents=True, exist_ok=True)
        
        # Estatísticas
        stats = {
            'total_files': 0,
            'organized_files': 0,
            'errors': 0,
            'categories': {}
        }
        
        # Lista todos os arquivos na pasta origem
        files_to_process = []
        for item in source_path.rglob('*'):
            if item.is_file():
                files_to_process.append(item)
        
        stats['total_files'] = len(files_to_process)
        self.logger.info(f"Iniciando organização de {stats['total_files']} arquivos...")
        
        for i, file_path in enumerate(files_to_process):
            try:
                # Atualiza progresso
                if progress_callback:
                    progress = (i + 1) / stats['total_files'] * 100
                    progress_callback(progress, f"Processando: {file_path.name}")
                
                # Determina categoria e data
                category = self.get_file_category(file_path)
                date_folder = self.get_file_date_folder(file_path)
                
                # Cria estrutura de pastas: destino/categoria/ano/mês/
                target_dir = destination_path / category / date_folder
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Define caminho final do arquivo
                target_file = target_dir / file_path.name
                target_file = self.create_unique_filename(target_file)
                
                # Move o arquivo
                shutil.move(str(file_path), str(target_file))
                
                # Atualiza estatísticas
                stats['organized_files'] += 1
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
                self.logger.info(f"Arquivo movido: {file_path.name} → {category}/{date_folder}")
                
            except Exception as e:
                stats['errors'] += 1
                self.logger.error(f"Erro ao processar {file_path}: {e}")
        
        # Log final das estatísticas
        self.logger.info("="*50)
        self.logger.info("RESUMO DA ORGANIZAÇÃO")
        self.logger.info("="*50)
        self.logger.info(f"Total de arquivos: {stats['total_files']}")
        self.logger.info(f"Arquivos organizados: {stats['organized_files']}")
        self.logger.info(f"Erros: {stats['errors']}")
        self.logger.info("\nArquivos por categoria:")
        for category, count in stats['categories'].items():
            self.logger.info(f"  {category}: {count}")
        
        return stats


class FileOrganizerGUI:
    """Interface gráfica para o Organizador de Arquivos."""
    
    def __init__(self):
        """Inicializa a interface gráfica."""
        self.organizer = FileOrganizer()
        self.setup_gui()
    
    def setup_gui(self):
        """Configura a interface gráfica."""
        self.root = tk.Tk()
        self.root.title("📁 Organizador de Arquivos Inteligente")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="📁 Organizador de Arquivos Inteligente", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Pasta de origem
        ttk.Label(main_frame, text="Pasta de origem:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        source_entry = ttk.Entry(main_frame, textvariable=self.source_var, width=50)
        source_entry.grid(row=1, column=1, padx=(10, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Escolher", 
                  command=self.select_source_folder).grid(row=1, column=2, pady=5)
        
        # Pasta de destino
        ttk.Label(main_frame, text="Pasta de destino:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        dest_entry = ttk.Entry(main_frame, textvariable=self.dest_var, width=50)
        dest_entry.grid(row=2, column=1, padx=(10, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Escolher", 
                  command=self.select_dest_folder).grid(row=2, column=2, pady=5)
        
        # Botão de organizar
        self.organize_btn = ttk.Button(main_frame, text="🚀 Organizar Arquivos", 
                                      command=self.start_organization, style='Accent.TButton')
        self.organize_btn.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Label de status
        self.status_var = tk.StringVar(value="Pronto para organizar arquivos")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Área de resultado
        ttk.Label(main_frame, text="Resultado:", font=('Arial', 12, 'bold')).grid(
            row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        # Text widget para mostrar resultados
        self.result_text = tk.Text(main_frame, height=10, width=70, wrap=tk.WORD)
        self.result_text.grid(row=7, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para o texto
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=7, column=3, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansão
        main_frame.rowconfigure(7, weight=1)
        
        # Valores padrão
        self.set_default_folders()
    
    def set_default_folders(self):
        """Define pastas padrão baseadas no sistema operacional."""
        home = Path.home()
        
        # Pasta de origem padrão (Downloads)
        downloads_folder = home / "Downloads"
        if downloads_folder.exists():
            self.source_var.set(str(downloads_folder))
        
        # Pasta de destino padrão
        organized_folder = home / "ArquivosOrganizados"
        self.dest_var.set(str(organized_folder))
    
    def select_source_folder(self):
        """Abre diálogo para seleção da pasta de origem."""
        folder = filedialog.askdirectory(title="Selecione a pasta de origem")
        if folder:
            self.source_var.set(folder)
    
    def select_dest_folder(self):
        """Abre diálogo para seleção da pasta de destino."""
        folder = filedialog.askdirectory(title="Selecione a pasta de destino")
        if folder:
            self.dest_var.set(folder)
    
    def update_progress(self, progress, status):
        """Atualiza a barra de progresso e status."""
        self.progress_var.set(progress)
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def start_organization(self):
        """Inicia o processo de organização em thread separada."""
        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()
        
        if not source or not dest:
            messagebox.showerror("Erro", "Por favor, selecione as pastas de origem e destino.")
            return
        
        if not os.path.exists(source):
            messagebox.showerror("Erro", "Pasta de origem não existe.")
            return
        
        # Confirma operação
        if not messagebox.askyesno("Confirmar", 
                                  f"Organizar arquivos de:\n{source}\n\nPara:\n{dest}\n\nContinuar?"):
            return
        
        # Desabilita botão e limpa resultado
        self.organize_btn.configure(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # Inicia thread de organização
        thread = threading.Thread(target=self.organize_files_thread, args=(source, dest))
        thread.daemon = True
        thread.start()
    
    def organize_files_thread(self, source, dest):
        """Thread para organização de arquivos."""
        try:
            # Executa organização
            stats = self.organizer.organize_files(source, dest, self.update_progress)
            
            # Mostra resultado na interface
            self.show_results(stats)
            
            # Mostra mensagem de sucesso
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", 
                                                           f"Organização concluída!\n"
                                                           f"{stats['organized_files']} arquivos organizados."))
            
        except Exception as e:
            # Mostra erro
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante organização: {e}"))
        
        finally:
            # Reabilita botão
            self.root.after(0, lambda: self.organize_btn.configure(state='normal'))
            self.root.after(0, lambda: self.status_var.set("Organização concluída"))
    
    def show_results(self, stats):
        """Mostra os resultados na área de texto."""
        result_text = f"""📊 RELATÓRIO DE ORGANIZAÇÃO
{'='*50}

📁 Total de arquivos processados: {stats['total_files']}
✅ Arquivos organizados com sucesso: {stats['organized_files']}
❌ Erros encontrados: {stats['errors']}

📂 ARQUIVOS POR CATEGORIA:
"""
        
        for category, count in stats['categories'].items():
            emoji_map = {
                'documentos': '📄',
                'imagens': '🖼️',
                'videos': '🎬',
                'audios': '🎵',
                'compactados': '📦',
                'executaveis': '⚙️',
                'codigo': '💻',
                'outros': '📋'
            }
            emoji = emoji_map.get(category, '📋')
            result_text += f"  {emoji} {category.title()}: {count} arquivo(s)\n"
        
        result_text += f"\n📝 Log detalhado salvo em: organizador_log.txt"
        
        # Atualiza interface na thread principal
        self.root.after(0, lambda: self.result_text.insert(tk.END, result_text))
    
    def run(self):
        """Executa a interface gráfica."""
        self.root.mainloop()


def main():
    """Função principal - pode ser executada via linha de comando ou GUI."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Modo linha de comando
        print("📁 Organizador de Arquivos Inteligente - Modo CLI")
        print("=" * 50)
        
        organizer = FileOrganizer()
        
        # Solicita pastas
        source = input("Digite o caminho da pasta de origem (Enter para Downloads): ").strip()
        if not source:
            source = str(Path.home() / "Downloads")
        
        dest = input("Digite o caminho da pasta de destino (Enter para ArquivosOrganizados): ").strip()
        if not dest:
            dest = str(Path.home() / "ArquivosOrganizados")
        
        print(f"\nOrganizando arquivos de: {source}")
        print(f"Para: {dest}")
        print("\nProcessando...")
        
        try:
            stats = organizer.organize_files(source, dest)
            print("\n✅ Organização concluída com sucesso!")
            print(f"📁 {stats['organized_files']} de {stats['total_files']} arquivos organizados")
            if stats['errors'] > 0:
                print(f"❌ {stats['errors']} erro(s) encontrado(s) - verifique o log")
        
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    else:
        # Modo interface gráfica
        try:
            app = FileOrganizerGUI()
            app.run()
        except ImportError:
            print("Tkinter não disponível. Execute com --cli para modo linha de comando.")
            print("Exemplo: python organizer.py --cli")


if __name__ == "__main__":
    main()
