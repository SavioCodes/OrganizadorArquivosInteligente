# 🤝 Guia de Contribuição - Organizador de Arquivos Inteligente 2025

Obrigado por considerar contribuir para o **Organizador de Arquivos Inteligente 2025**! Este documento fornece diretrizes para contribuições efetivas e colaboração produtiva.

## 🎯 Como Contribuir

### 🐛 Reportando Bugs
1. **Verifique** se o bug já foi reportado nas [Issues](https://github.com/SavioCodes/OrganizadorArquivosInteligente/issues)
2. **Use** o template de bug report
3. **Inclua** informações detalhadas:
   - Versão do Python e SO
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Logs relevantes

### 💡 Sugerindo Melhorias
1. **Abra** uma issue com o template de feature request
2. **Descreva** claramente a funcionalidade desejada
3. **Explique** o caso de uso e benefícios
4. **Considere** a compatibilidade com versões existentes

### 🔧 Contribuindo com Código

#### Configuração do Ambiente
```bash
# 1. Fork e clone o repositório
git clone https://github.com/SEU_USERNAME/OrganizadorArquivosInteligente.git
cd OrganizadorArquivosInteligente

# 2. Crie ambiente virtual
python -m venv dev-env
source dev-env/bin/activate  # Linux/macOS
# ou dev-env\Scripts\activate  # Windows

# 3. Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# 4. Configure pre-commit hooks (opcional)
pre-commit install
```

#### Fluxo de Desenvolvimento
1. **Crie** uma branch para sua feature:
   ```bash
   git checkout -b feature/minha-nova-feature
   ```

2. **Desenvolva** seguindo os padrões do projeto

3. **Teste** suas alterações:
   ```bash
   # Testes unitários
   pytest
   
   # Cobertura de código
   pytest --cov=organizer --cov-report=html
   
   # Qualidade de código
   flake8 organizer.py
   mypy organizer.py
   black --check organizer.py
   ```

4. **Commit** com mensagens descritivas:
   ```bash
   git commit -m "feat: adiciona detecção de arquivos de vídeo 4K"
   ```

5. **Push** e abra um Pull Request

## 📋 Padrões de Código

### 🐍 Estilo Python
- **PEP 8** como base
- **Black** para formatação automática
- **Type hints** obrigatórios para funções públicas
- **Docstrings** no formato Google Style

### 📝 Convenções de Commit
Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição

feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: tarefas de manutenção
```

### 🧪 Testes
- **Cobertura mínima**: 80%
- **Testes unitários** para todas as funções públicas
- **Testes de integração** para fluxos principais
- **Mocks** para operações de I/O

Exemplo de teste:
```python
def test_get_file_category():
    organizer = SmartFileOrganizer()
    file_info = FileInfo(
        path=Path("test.pdf"),
        extension=".pdf",
        mime_type="application/pdf"
    )
    
    category = organizer.get_file_category(file_info)
    assert category == "documentos"
```

## 🏗️ Arquitetura do Projeto

### 📁 Estrutura de Arquivos
```
OrganizadorArquivosInteligente/
├── organizer.py              # Código principal
├── tests/                    # Testes
│   ├── test_organizer.py
│   └── test_gui.py
├── docs/                     # Documentação
├── examples/                 # Exemplos de uso
├── configs/                  # Configurações exemplo
└── scripts/                  # Scripts utilitários
```

### 🔧 Componentes Principais
- **SmartFileOrganizer**: Core do sistema
- **ModernFileOrganizerGUI**: Interface gráfica
- **FileInfo**: Metadados de arquivo
- **OrganizationStats**: Estatísticas

## 🎨 Diretrizes de Design

### 🖥️ Interface Gráfica
- **Consistência** visual em todos os elementos
- **Acessibilidade** (contraste, tamanhos)
- **Responsividade** para diferentes resoluções
- **Feedback** visual para todas as ações

### 📊 Experiência do Usuário
- **Simplicidade** na interface principal
- **Opções avançadas** em seções separadas
- **Mensagens claras** de erro e sucesso
- **Progresso visível** para operações longas

## 🚀 Tipos de Contribuição

### 🔥 Prioridade Alta
- 🐛 Correções de bugs críticos
- 🔒 Melhorias de segurança
- ⚡ Otimizações de performance
- 📱 Compatibilidade com novos sistemas

### 🌟 Funcionalidades Desejadas
- 🌐 Interface web com FastAPI
- 🤖 IA para categorização por conteúdo
- ☁️ Integração com cloud storage
- 📱 App mobile
- 🔍 Busca semântica
- 📊 Dashboard de analytics

### 📚 Documentação
- 📖 Tutoriais e guias
- 🎥 Vídeos explicativos
- 🌍 Traduções
- 📋 Exemplos de uso

## ✅ Checklist para Pull Requests

Antes de submeter um PR, verifique:

- [ ] **Código** segue os padrões do projeto
- [ ] **Testes** passam e cobertura mantida
- [ ] **Documentação** atualizada se necessário
- [ ] **Changelog** atualizado para mudanças significativas
- [ ] **Commits** seguem convenção estabelecida
- [ ] **Branch** está atualizada com main
- [ ] **Descrição** clara do que foi alterado

## 🏷️ Labels das Issues

| Label | Descrição |
|-------|-----------|
| `bug` | Algo não está funcionando |
| `enhancement` | Nova funcionalidade ou melhoria |
| `documentation` | Melhorias na documentação |
| `good first issue` | Boa para iniciantes |
| `help wanted` | Ajuda extra é bem-vinda |
| `priority: high` | Alta prioridade |
| `priority: low` | Baixa prioridade |

## 🎖️ Reconhecimento

Contribuidores são reconhecidos:
- 📝 **README**: Lista de contribuidores
- 🏆 **Releases**: Créditos nas notas de versão
- 🌟 **GitHub**: Destaque no perfil do projeto

## 📞 Comunicação

### 💬 Canais de Comunicação
- **Issues**: Discussões técnicas
- **Discussions**: Ideias e perguntas gerais
- **Email**: contato@saviocodes.com (questões privadas)

### 🕐 Tempo de Resposta
- **Issues**: 24-48 horas
- **Pull Requests**: 2-5 dias úteis
- **Discussões**: 1-3 dias

## 📜 Código de Conduta

### 🤝 Nossos Valores
- **Respeito** mútuo e inclusividade
- **Colaboração** construtiva
- **Aprendizado** contínuo
- **Qualidade** em tudo que fazemos

### 🚫 Comportamentos Inaceitáveis
- Linguagem ofensiva ou discriminatória
- Assédio de qualquer forma
- Spam ou autopromoção excessiva
- Violação de privacidade

## 🎓 Recursos para Novos Contribuidores

### 📚 Documentação Útil
- [Python Style Guide](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Type Hints](https://docs.python.org/3/library/typing.html)

### 🛠️ Ferramentas Recomendadas
- **IDE**: VS Code, PyCharm
- **Git GUI**: GitKraken, SourceTree
- **Terminal**: Windows Terminal, iTerm2

## 🙏 Agradecimentos

Agradecemos a todos que contribuem para tornar este projeto melhor! Cada contribuição, por menor que seja, faz diferença.

---

**Dúvidas?** Não hesite em abrir uma [Discussion](https://github.com/SavioCodes/OrganizadorArquivosInteligente/discussions) ou entrar em contato!

*Desenvolvido com ❤️ pela comunidade*
