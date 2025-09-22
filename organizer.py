#!/usr/bin/env python3
"""
📁 Organizador de Arquivos Inteligente 2025
==========================================
Sistema avançado de automação para organização inteligente de arquivos.
Versão: 2.0.0 | Ano: 2025
Autor: SavioCodes - https://github.com/SavioCodes
Licença: MIT
"""

import os
import shutil
import datetime
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional, Callable
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import json
import hashlib
import mimetypes
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import concurrent.futures
from collections import defaultdict


class OrganizationMode(Enum):
    """Modos de organização disponíveis."""
    BY_TYPE_AND_DATE = "tipo_e_data"
    BY_TYPE_ONLY = "apenas_tipo"
    BY_DATE_ONLY = "apenas_data"
    BY_SIZE = "por_tamanho"


@dataclass
class FileInfo:
    """Informações detalhadas de um arquivo."""
    path: Path
    size: int
    created_date: datetime.datetime
    modified_date: datetime.datetime
    extension: str
    mime_type: str
    hash_md5: Optional[str] = None
    category: Optional[str] = None


@dataclass
class OrganizationStats:
    """Estatísticas da organização."""
    total_files: int = 0
    organized_files: int = 0
    skipped_files: int = 0
    errors: int = 0
    duplicates_found: int = 0
    total_size: int = 0
    categories: Dict[str, int] = None
    processing_time: float = 0.0
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = defaultdict(int)


class SmartFileOrganizer:
    """
    Organizador de arquivos inteligente com recursos avançados.
    Versão 2025 com melhorias em performance, segurança e usabilidade.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializa o organizador com configurações avançadas.
        
        Args:
            config_file: Arquivo de configuração personalizada (JSON)
        """
        self.version = "2.0.0"
        self.year = 2025
        
        # Configurações padrão expandidas para 2025
        self.file_categories = {
            'documentos': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', 
                              '.xlsx', '.ppt', '.pptx', '.csv', '.ods', '.odp', '.pages',
                              '.numbers', '.key', '.epub', '.mobi'],
                'icon': '📄',
                'description': 'Documentos e planilhas'
            },
            'imagens': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', 
                              '.webp', '.ico', '.raw', '.psd', '.ai', '.sketch', '.fig',
                              '.heic', '.heif', '.avif', '.jxl'],
                'icon': '🖼️',
                'description': 'Imagens e gráficos'
            },
            'videos': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
                              '.m4v', '.3gp', '.mpg', '.mpeg', '.ogv', '.f4v', '.asf',
                              '.m2ts', '.mts', '.vob'],
                'icon': '🎬',
                'description': 'Vídeos e filmes'
            },
            'audios': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', 
                              '.opus', '.aiff', '.alac', '.ape', '.dsd', '.pcm'],
                'icon': '🎵',
                'description': 'Áudios e música'
            },
            'compactados': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', 
                              '.tar.gz', '.tar.bz2', '.tar.xz', '.lzma', '.zst'],
                'icon': '📦',
                'description': 'Arquivos compactados'
            },
            'executaveis': {
                'extensions': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.appimage',
                              '.snap', '.flatpak', '.app', '.run'],
                'icon': '⚙️',
                'description': 'Programas executáveis'
            },
            'codigo': {
                'extensions': ['.py', '.js', '.ts', '.html', '.css', '.php', '.java', '.cpp', 
                              '.c', '.h', '.json', '.xml', '.sql', '.sh', '.bat', '.ps1',
                              '.go', '.rs', '.swift', '.kt', '.dart', '.vue', '.jsx', '.tsx'],
                'icon': '💻',
                'description': 'Código fonte'
            },
            'fontes': {
                'extensions': ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon', '.pfb', '.pfm'],
                'icon': '🔤',
                'description': 'Arquivos de fonte'
            },
            'ebooks': {
                'extensions': ['.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lit', '.pdb'],
                'icon': '📚',
                'description': 'Livros eletrônicos'
            },
            'outros': {
                'extensions': [],
                'icon': '📋',
                'description': 'Outros arquivos'
            }
        }
        
        self.organization_mode = OrganizationMode.BY_TYPE_AND_DATE
        self.duplicate_handling = "rename"  # "rename", "skip", "replace"
        self.max_workers = min(32, (os.cpu_count() or 1) + 4)
        
        # Carrega configurações personalizadas se fornecidas
        if config_file and Path(config_file).exists():
            self.load_config(config_file)
        
        self.setup_logging()
        self.logger.info(f"🚀 Organizador de Arquivos Inteligente {self.version} ({self.year}) iniciado")
    
    def setup_logging(self):
        """Configura sistema de logging avançado."""
        log_format = '%(asctime)s | %(levelname)8s | %(message)s'
        
        # Cria pasta de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Nome do arquivo de log com timestamp
        log_filename = f"organizador_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = log_dir / log_filename
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Mantém apenas os 10 logs mais recentes
        self.cleanup_old_logs(log_dir, keep_count=10)
    
    def cleanup_old_logs(self, log_dir: Path, keep_count: int = 10):
        """Remove logs antigos mantendo apenas os mais recentes."""
        try:
            log_files = sorted(log_dir.glob("organizador_*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
            for old_log in log_files[keep_count:]:
                old_log.unlink()
                self.logger.debug(f"Log antigo removido: {old_log.name}")
        except Exception as e:
            self.logger.warning(f"Erro ao limpar logs antigos: {e}")
    
    def load_config(self, config_file: str):
        """Carrega configurações personalizadas de arquivo JSON."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 'file_categories' in config:
                self.file_categories.update(config['file_categories'])
            
            if 'organization_mode' in config:
                self.organization_mode = OrganizationMode(config['organization_mode'])
            
            if 'duplicate_handling' in config:
                self.duplicate_handling = config['duplicate_handling']
            
            self.logger.info(f"Configurações carregadas de: {config_file}")
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
    
    def save_config(self, config_file: str):
        """Salva configurações atuais em arquivo JSON."""
        try:
            config = {
                'version': self.version,
                'file_categories': self.file_categories,
                'organization_mode': self.organization_mode.value,
                'duplicate_handling': self.duplicate_handling,
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configurações salvas em: {config_file}")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
    
    def get_file_info(self, file_path: Path) -> FileInfo:
        """
        Extrai informações detalhadas de um arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            FileInfo: Informações completas do arquivo
        """
        try:
            stat = file_path.stat()
            
            # Datas de criação e modificação
            created_date = datetime.datetime.fromtimestamp(stat.st_ctime)
            modified_date = datetime.datetime.fromtimestamp(stat.st_mtime)
            
            # MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = "application/octet-stream"
            
            return FileInfo(
                path=file_path,
                size=stat.st_size,
                created_date=created_date,
                modified_date=modified_date,
                extension=file_path.suffix.lower(),
                mime_type=mime_type
            )
        
        except Exception as e:
            self.logger.error(f"Erro ao obter informações do arquivo {file_path}: {e}")
            raise
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calcula hash MD5 do arquivo para detecção de duplicatas.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            str: Hash MD5 do arquivo
        """
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Lê em chunks para arquivos grandes
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        
        except Exception as e:
            self.logger.error(f"Erro ao calcular hash do arquivo {file_path}: {e}")
            return ""
    
    def get_file_category(self, file_info: FileInfo) -> str:
        """
        Determina a categoria de um arquivo baseado em extensão e MIME type.
        
        Args:
            file_info: Informações do arquivo
            
        Returns:
            str: Categoria do arquivo
        """
        extension = file_info.extension
        mime_type = file_info.mime_type
        
        # Verifica por extensão primeiro
        for category, info in self.file_categories.items():
            if extension in info['extensions']:
                return category
        
        # Fallback por MIME type
        if mime_type.startswith('image/'):
            return 'imagens'
        elif mime_type.startswith('video/'):
            return 'videos'
        elif mime_type.startswith('audio/'):
            return 'audios'
        elif mime_type.startswith('text/'):
            return 'documentos'
        
        return 'outros'
    
    def get_organization_path(self, file_info: FileInfo, base_dest: Path) -> Path:
        """
        Determina o caminho de destino baseado no modo de organização.
        
        Args:
            file_info: Informações do arquivo
            base_dest: Diretório base de destino
            
        Returns:
            Path: Caminho completo de destino
        """
        category = self.get_file_category(file_info)
        
        if self.organization_mode == OrganizationMode.BY_TYPE_AND_DATE:
            date_folder = f"{file_info.modified_date.year}/{file_info.modified_date.month:02d}"
            return base_dest / category / date_folder
        
        elif self.organization_mode == OrganizationMode.BY_TYPE_ONLY:
            return base_dest / category
        
        elif self.organization_mode == OrganizationMode.BY_DATE_ONLY:
            date_folder = f"{file_info.modified_date.year}/{file_info.modified_date.month:02d}"
            return base_dest / date_folder
        
        elif self.organization_mode == OrganizationMode.BY_SIZE:
            if file_info.size < 1024 * 1024:  # < 1MB
                size_category = "pequenos"
            elif file_info.size < 100 * 1024 * 1024:  # < 100MB
                size_category = "medios"
            else:
                size_category = "grandes"
            return base_dest / size_category / category
        
        return base_dest / category
    
    def create_unique_filename(self, destination: Path) -> Path:
        """
        Cria nome único para evitar sobrescrita com estratégia inteligente.
        
        Args:
            destination: Caminho de destino desejado
            
        Returns:
            Path: Caminho único para o arquivo
        """
        if not destination.exists():
            return destination
        
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        
        # Estratégia: nome_arquivo (1), nome_arquivo (2), etc.
        counter = 1
        while True:
            new_name = f"{stem} ({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
            
            # Proteção contra loop infinito
            if counter > 9999:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{stem}_{timestamp}{suffix}"
                return parent / new_name
    
    def process_single_file(self, file_info: FileInfo, destination_dir: Path, 
                           duplicate_hashes: Dict[str, Path]) -> Tuple[bool, str]:
        """
        Processa um único arquivo com tratamento avançado de duplicatas.
        
        Args:
            file_info: Informações do arquivo
            destination_dir: Diretório de destino
            duplicate_hashes: Dicionário de hashes para detecção de duplicatas
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            # Calcula hash para detecção de duplicatas
            if self.duplicate_handling != "skip":
                file_hash = self.calculate_file_hash(file_info.path)
                file_info.hash_md5 = file_hash
                
                if file_hash in duplicate_hashes:
                    if self.duplicate_handling == "skip":
                        return False, f"Duplicata ignorada: {file_info.path.name}"
                    elif self.duplicate_handling == "replace":
                        # Remove arquivo duplicado anterior
                        duplicate_hashes[file_hash].unlink()
            
            # Determina pasta de destino
            target_dir = self.get_organization_path(file_info, destination_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Define arquivo de destino
            target_file = target_dir / file_info.path.name
            
            # Cria nome único se necessário
            if target_file.exists():
                target_file = self.create_unique_filename(target_file)
            
            # Move o arquivo
            shutil.move(str(file_info.path), str(target_file))
            
            # Atualiza registro de duplicatas
            if file_info.hash_md5:
                duplicate_hashes[file_info.hash_md5] = target_file
            
            category = self.get_file_category(file_info)
            relative_path = target_file.relative_to(destination_dir)
            
            return True, f"✅ {file_info.path.name} → {relative_path}"
        
        except Exception as e:
            return False, f"❌ Erro ao processar {file_info.path.name}: {e}"
    
    def organize_files(self, source_dir: str, destination_dir: str, 
                      progress_callback: Optional[Callable] = None,
                      include_subdirs: bool = True) -> OrganizationStats:
        """
        Organiza arquivos com processamento paralelo e recursos avançados.
        
        Args:
            source_dir: Diretório de origem
            destination_dir: Diretório de destino
            progress_callback: Função callback para progresso
            include_subdirs: Incluir subdiretórios na busca
            
        Returns:
            OrganizationStats: Estatísticas detalhadas da operação
        """
        start_time = datetime.datetime.now()
        source_path = Path(source_dir)
        destination_path = Path(destination_dir)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Diretório de origem não encontrado: {source_dir}")
        
        destination_path.mkdir(parents=True, exist_ok=True)
        
        # Inicializa estatísticas
        stats = OrganizationStats()
        duplicate_hashes = {}
        
        self.logger.info(f"🔍 Escaneando arquivos em: {source_path}")
        
        # Coleta todos os arquivos
        files_to_process = []
        pattern = "**/*" if include_subdirs else "*"
        
        for item in source_path.glob(pattern):
            if item.is_file():
                try:
                    file_info = self.get_file_info(item)
                    files_to_process.append(file_info)
                    stats.total_size += file_info.size
                except Exception as e:
                    self.logger.error(f"Erro ao processar {item}: {e}")
                    stats.errors += 1
        
        stats.total_files = len(files_to_process)
        self.logger.info(f"📊 Encontrados {stats.total_files} arquivos ({self.format_size(stats.total_size)})")
        
        if stats.total_files == 0:
            return stats
        
        # Processamento paralelo com ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submete todas as tarefas
            future_to_file = {
                executor.submit(self.process_single_file, file_info, destination_path, duplicate_hashes): file_info
                for file_info in files_to_process
            }
            
            # Processa resultados conforme completam
            for i, future in enumerate(concurrent.futures.as_completed(future_to_file)):
                file_info = future_to_file[future]
                
                try:
                    success, message = future.result()
                    
                    if success:
                        stats.organized_files += 1
                        category = self.get_file_category(file_info)
                        stats.categories[category] += 1
                        self.logger.info(message)
                    else:
                        if "Duplicata" in message:
                            stats.duplicates_found += 1
                        else:
                            stats.errors += 1
                        stats.skipped_files += 1
                        self.logger.warning(message)
                
                except Exception as e:
                    stats.errors += 1
                    self.logger.error(f"❌ Erro no processamento: {e}")
                
                # Atualiza progresso
                if progress_callback:
                    progress = (i + 1) / stats.total_files * 100
                    progress_callback(progress, f"Processando: {file_info.path.name}")
        
        # Calcula tempo de processamento
        end_time = datetime.datetime.now()
        stats.processing_time = (end_time - start_time).total_seconds()
        
        # Log final das estatísticas
        self.log_final_stats(stats)
        
        # Salva relatório detalhado
        self.save_detailed_report(stats, source_dir, destination_dir)
        
        return stats
    
    def format_size(self, size_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def log_final_stats(self, stats: OrganizationStats):
        """Registra estatísticas finais no log."""
        self.logger.info("=" * 60)
        self.logger.info("📊 RELATÓRIO FINAL DE ORGANIZAÇÃO")
        self.logger.info("=" * 60)
        self.logger.info(f"📁 Total de arquivos processados: {stats.total_files}")
        self.logger.info(f"✅ Arquivos organizados: {stats.organized_files}")
        self.logger.info(f"⏭️  Arquivos ignorados: {stats.skipped_files}")
        self.logger.info(f"🔄 Duplicatas encontradas: {stats.duplicates_found}")
        self.logger.info(f"❌ Erros: {stats.errors}")
        self.logger.info(f"💾 Tamanho total processado: {self.format_size(stats.total_size)}")
        self.logger.info(f"⏱️  Tempo de processamento: {stats.processing_time:.2f}s")
        
        if stats.categories:
            self.logger.info("\n📂 ARQUIVOS POR CATEGORIA:")
            for category, count in sorted(stats.categories.items()):
                icon = self.file_categories.get(category, {}).get('icon', '📋')
                self.logger.info(f"  {icon} {category.title()}: {count} arquivo(s)")
    
    def save_detailed_report(self, stats: OrganizationStats, source_dir: str, destination_dir: str):
        """Salva relatório detalhado em JSON."""
        try:
            report_dir = Path("reports")
            report_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = report_dir / f"relatorio_organizacao_{timestamp}.json"
            
            report_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'version': self.version,
                'source_directory': source_dir,
                'destination_directory': destination_dir,
                'organization_mode': self.organization_mode.value,
                'statistics': asdict(stats),
                'configuration': {
                    'duplicate_handling': self.duplicate_handling,
                    'max_workers': self.max_workers,
                    'categories_count': len(self.file_categories)
                }
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"📄 Relatório detalhado salvo: {report_file}")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar relatório: {e}")


class ModernFileOrganizerGUI:
    """Interface gráfica moderna e intuitiva para o Organizador 2025."""
    
    def __init__(self):
        """Inicializa a interface gráfica moderna."""
        self.organizer = SmartFileOrganizer()
        self.setup_modern_gui()
    
    def setup_modern_gui(self):
        """Configura interface gráfica com design moderno."""
        self.root = tk.Tk()
        self.root.title(f"📁 Organizador de Arquivos Inteligente {self.organizer.version} ({self.organizer.year})")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configuração de tema moderno
        style = ttk.Style()
        available_themes = style.theme_names()
        modern_theme = 'vista' if 'vista' in available_themes else 'clam'
        style.theme_use(modern_theme)
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'))
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Modern.TButton', padding=(10, 5))
        
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Cabeçalho moderno
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(header_frame, 
                               text=f"📁 Organizador de Arquivos Inteligente {self.organizer.year}",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        version_label = ttk.Label(header_frame, 
                                 text=f"Versão {self.organizer.version} | SavioCodes",
                                 style='Subtitle.TLabel')
        version_label.grid(row=1, column=0, sticky=tk.W)
        
        # Seção de configuração de pastas
        folder_frame = ttk.LabelFrame(main_frame, text="📂 Configuração de Pastas", padding="15")
        folder_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        folder_frame.columnconfigure(1, weight=1)
        
        # Pasta de origem
        ttk.Label(folder_frame, text="Pasta de origem:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        source_entry = ttk.Entry(folder_frame, textvariable=self.source_var, width=60)
        source_entry.grid(row=0, column=1, padx=(10, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(folder_frame, text="📁 Escolher", 
                  command=self.select_source_folder).grid(row=0, column=2, pady=5)
        
        # Pasta de destino
        ttk.Label(folder_frame, text="Pasta de destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        dest_entry = ttk.Entry(folder_frame, textvariable=self.dest_var, width=60)
        dest_entry.grid(row=1, column=1, padx=(10, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(folder_frame, text="📁 Escolher", 
                  command=self.select_dest_folder).grid(row=1, column=2, pady=5)
        
        # Seção de opções avançadas
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Opções Avançadas", padding="15")
        options_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Modo de organização
        ttk.Label(options_frame, text="Modo de organização:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value=self.organizer.organization_mode.value)
        mode_combo = ttk.Combobox(options_frame, textvariable=self.mode_var, width=25, state="readonly")
        mode_combo['values'] = [mode.value for mode in OrganizationMode]
        mode_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Tratamento de duplicatas
        ttk.Label(options_frame, text="Duplicatas:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.duplicate_var = tk.StringVar(value=self.organizer.duplicate_handling)
        duplicate_combo = ttk.Combobox(options_frame, textvariable=self.duplicate_var, width=15, state="readonly")
        duplicate_combo['values'] = ["rename", "skip", "replace"]
        duplicate_combo.grid(row=0, column=3, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Incluir subdiretórios
        self.include_subdirs_var = tk.BooleanVar(value=True)
        subdirs_check = ttk.Checkbutton(options_frame, text="Incluir subdiretórios", 
                                       variable=self.include_subdirs_var)
        subdirs_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        self.organize_btn = ttk.Button(action_frame, text="🚀 Organizar Arquivos", 
                                      command=self.start_organization, 
                                      style='Modern.TButton')
        self.organize_btn.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(action_frame, text="💾 Salvar Configuração", 
                  command=self.save_config).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(action_frame, text="📁 Carregar Configuração", 
                  command=self.load_config).grid(row=0, column=2)
        
        # Seção de progresso
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progresso", padding="15")
        progress_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=500)
        self.progress_bar.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Status
        self.status_var = tk.StringVar(value="✅ Pronto para organizar arquivos")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="📋 Resultados", padding="15")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget com scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(text_frame, height=12, width=80, wrap=tk.WORD, 
                                  font=('Consolas', 9))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansão da área de resultados
        main_frame.rowconfigure(5, weight=1)
        
        # Define valores padrão
        self.set_default_folders()
    
    def set_default_folders(self):
        """Define pastas padrão inteligentes baseadas no sistema."""
        home = Path.home()
        
        # Pasta de origem padrão (Downloads)
        downloads_folder = home / "Downloads"
        if downloads_folder.exists():
            self.source_var.set(str(downloads_folder))
        else:
            self.source_var.set(str(home))
        
        # Pasta de destino padrão
        organized_folder = home / "ArquivosOrganizados2025"
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
    
    def save_config(self):
        """Salva configuração atual."""
        config_file = filedialog.asksaveasfilename(
            title="Salvar Configuração",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if config_file:
            self.update_organizer_config()
            self.organizer.save_config(config_file)
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
    
    def load_config(self):
        """Carrega configuração de arquivo."""
        config_file = filedialog.askopenfilename(
            title="Carregar Configuração",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if config_file:
            self.organizer.load_config(config_file)
            self.update_gui_from_config()
            messagebox.showinfo("Sucesso", "Configuração carregada com sucesso!")
    
    def update_organizer_config(self):
        """Atualiza configurações do organizador baseado na GUI."""
        self.organizer.organization_mode = OrganizationMode(self.mode_var.get())
        self.organizer.duplicate_handling = self.duplicate_var.get()
    
    def update_gui_from_config(self):
        """Atualiza GUI baseado nas configurações do organizador."""
        self.mode_var.set(self.organizer.organization_mode.value)
        self.duplicate_var.set(self.organizer.duplicate_handling)
    
    def update_progress(self, progress: float, status: str):
        """Atualiza progresso e status."""
        self.progress_var.set(progress)
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def start_organization(self):
        """Inicia processo de organização."""
        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()
        
        if not source or not dest:
            messagebox.showerror("Erro", "Por favor, selecione as pastas de origem e destino.")
            return
        
        if not os.path.exists(source):
            messagebox.showerror("Erro", "Pasta de origem não existe.")
            return
        
        if source == dest:
            messagebox.showerror("Erro", "As pastas de origem e destino não podem ser iguais.")
            return
        
        # Confirmação com informações detalhadas
        file_count = len(list(Path(source).rglob('*') if self.include_subdirs_var.get() 
                              else Path(source).glob('*')))
        
        confirm_msg = (f"🔍 Organizar arquivos:\n\n"
                      f"📂 Origem: {source}\n"
                      f"📁 Destino: {dest}\n"
                      f"📊 Arquivos encontrados: ~{file_count}\n"
                      f"⚙️ Modo: {self.mode_var.get()}\n"
                      f"🔄 Duplicatas: {self.duplicate_var.get()}\n\n"
                      f"Continuar?")
        
        if not messagebox.askyesno("Confirmar Organização", confirm_msg):
            return
        
        # Prepara interface para processamento
        self.organize_btn.configure(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_var.set("🚀 Iniciando organização...")
        
        # Atualiza configurações
        self.update_organizer_config()
        
        # Inicia thread de organização
        thread = threading.Thread(target=self.organize_files_thread, 
                                 args=(source, dest, self.include_subdirs_var.get()))
        thread.daemon = True
        thread.start()
    
    def organize_files_thread(self, source: str, dest: str, include_subdirs: bool):
        """Thread para organização de arquivos."""
        try:
            # Executa organização
            stats = self.organizer.organize_files(source, dest, self.update_progress, include_subdirs)
            
            # Mostra resultado
            self.show_results(stats)
            
            # Mensagem de sucesso
            success_msg = (f"✅ Organização concluída!\n\n"
                          f"📁 {stats.organized_files} de {stats.total_files} arquivos organizados\n"
                          f"⏱️ Tempo: {stats.processing_time:.2f}s\n"
                          f"💾 Tamanho: {self.organizer.format_size(stats.total_size)}")
            
            if stats.errors > 0:
                success_msg += f"\n⚠️ {stats.errors} erro(s) encontrado(s)"
            
            self.root.after(0, lambda: messagebox.showinfo("Organização Concluída", success_msg))
        
        except Exception as e:
            error_msg = f"❌ Erro durante organização:\n\n{str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Erro", error_msg))
        
        finally:
            # Reabilita interface
            self.root.after(0, lambda: self.organize_btn.configure(state='normal'))
            self.root.after(0, lambda: self.status_var.set("✅ Organização concluída"))
    
    def show_results(self, stats: OrganizationStats):
        """Mostra resultados detalhados na interface."""
        result_text = f"""🎉 RELATÓRIO DE ORGANIZAÇÃO - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
{'='*70}

📊 ESTATÍSTICAS GERAIS:
  📁 Total de arquivos: {stats.total_files}
  ✅ Organizados com sucesso: {stats.organized_files}
  ⏭️  Arquivos ignorados: {stats.skipped_files}
  🔄 Duplicatas encontradas: {stats.duplicates_found}
  ❌ Erros: {stats.errors}
  💾 Tamanho total: {self.organizer.format_size(stats.total_size)}
  ⏱️  Tempo de processamento: {stats.processing_time:.2f} segundos

📂 ARQUIVOS POR CATEGORIA:
"""
        
        if stats.categories:
            for category, count in sorted(stats.categories.items()):
                icon = self.organizer.file_categories.get(category, {}).get('icon', '📋')
                description = self.organizer.file_categories.get(category, {}).get('description', category)
                percentage = (count / stats.organized_files * 100) if stats.organized_files > 0 else 0
                result_text += f"  {icon} {description}: {count} arquivo(s) ({percentage:.1f}%)\n"
        
        result_text += f"\n📝 Logs detalhados salvos na pasta 'logs/'"
        result_text += f"\n📄 Relatório JSON salvo na pasta 'reports/'"
        
        # Atualiza interface na thread principal
        self.root.after(0, lambda: self.result_text.insert(tk.END, result_text))
    
    def run(self):
        """Executa a interface gráfica."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def main():
    """Função principal com suporte a argumentos de linha de comando."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"📁 Organizador de Arquivos Inteligente 2025 v2.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python organizer.py                           # Interface gráfica
  python organizer.py --cli                     # Modo linha de comando
  python organizer.py --cli --source ~/Downloads --dest ~/Organized
  python organizer.py --config config.json     # Usar configuração personalizada
        """
    )
    
    parser.add_argument('--cli', action='store_true', 
                       help='Executar em modo linha de comando')
    parser.add_argument('--source', type=str, 
                       help='Pasta de origem')
    parser.add_argument('--dest', type=str, 
                       help='Pasta de destino')
    parser.add_argument('--config', type=str, 
                       help='Arquivo de configuração JSON')
    parser.add_argument('--mode', type=str, 
                       choices=[mode.value for mode in OrganizationMode],
                       help='Modo de organização')
    parser.add_argument('--duplicates', type=str, 
                       choices=['rename', 'skip', 'replace'],
                       help='Como tratar duplicatas')
    parser.add_argument('--no-subdirs', action='store_true',
                       help='Não incluir subdiretórios')
    
    args = parser.parse_args()
    
    if args.cli:
        # Modo linha de comando
        print(f"📁 Organizador de Arquivos Inteligente 2025 v2.0.0")
        print("=" * 60)
        
        organizer = SmartFileOrganizer(args.config)
        
        # Configura organizador baseado nos argumentos
        if args.mode:
            organizer.organization_mode = OrganizationMode(args.mode)
        if args.duplicates:
            organizer.duplicate_handling = args.duplicates
        
        # Solicita ou usa pastas fornecidas
        source = args.source or input("📂 Pasta de origem (Enter para Downloads): ").strip()
        if not source:
            source = str(Path.home() / "Downloads")
        
        dest = args.dest or input("📁 Pasta de destino (Enter para ArquivosOrganizados2025): ").strip()
        if not dest:
            dest = str(Path.home() / "ArquivosOrganizados2025")
        
        include_subdirs = not args.no_subdirs
        
        print(f"\n🔍 Organizando arquivos:")
        print(f"  📂 Origem: {source}")
        print(f"  📁 Destino: {dest}")
        print(f"  ⚙️ Modo: {organizer.organization_mode.value}")
        print(f"  🔄 Duplicatas: {organizer.duplicate_handling}")
        print(f"  📁 Subdiretórios: {'Sim' if include_subdirs else 'Não'}")
        print("\n🚀 Processando...")
        
        try:
            def progress_callback(progress, status):
                print(f"\r⏳ {progress:.1f}% - {status}", end="", flush=True)
            
            stats = organizer.organize_files(source, dest, progress_callback, include_subdirs)
            
            print(f"\n\n✅ Organização concluída!")
            print(f"📊 {stats.organized_files} de {stats.total_files} arquivos organizados")
            print(f"⏱️ Tempo: {stats.processing_time:.2f}s")
            print(f"💾 Tamanho: {organizer.format_size(stats.total_size)}")
            
            if stats.errors > 0:
                print(f"⚠️ {stats.errors} erro(s) - verifique os logs")
        
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            sys.exit(1)
    
    else:
        # Modo interface gráfica
        try:
            app = ModernFileOrganizerGUI()
            if args.config:
                app.organizer.load_config(args.config)
                app.update_gui_from_config()
            app.run()
        except ImportError:
            print("❌ Tkinter não disponível.")
            print("💡 Execute com --cli para modo linha de comando.")
            print("📖 Exemplo: python organizer.py --cli")
        except Exception as e:
            print(f"❌ Erro ao iniciar interface gráfica: {e}")
            print("💡 Tente executar em modo CLI: python organizer.py --cli")


if __name__ == "__main__":
    main()
