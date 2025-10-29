# Guia de Contribuição

Obrigado por considerar contribuir para o Jukebox Retro! 🎵

## Como Contribuir

### Reportar Bugs

Se você encontrou um bug, por favor abra uma issue incluindo:

1. **Descrição do problema**: Explique o que aconteceu
2. **Passos para reproduzir**: Como reproduzir o bug
3. **Comportamento esperado**: O que deveria acontecer
4. **Sistema operacional**: Windows/Linux e versão
5. **Versão do Python**: Qual versão você está usando
6. **Logs de erro**: Se disponível

### Sugerir Novos Recursos

Para sugerir novos recursos, abra uma issue com:

1. **Descrição do recurso**: O que você gostaria de ver
2. **Caso de uso**: Por que este recurso seria útil
3. **Alternativas consideradas**: Outras soluções que você pensou

### Enviar Pull Requests

1. **Fork o repositório**
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```

3. **Faça suas alterações** seguindo o estilo do código:
   - Use PEP 8 para estilo Python
   - Adicione comentários quando necessário
   - Mantenha o estilo retro da interface

4. **Teste suas alterações**:
   ```bash
   python3 test_jukebox.py
   python3 jukebox_retro.py
   ```

5. **Commit suas alterações**:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

6. **Push para sua branch**:
   ```bash
   git push origin feature/minha-feature
   ```

7. **Abra um Pull Request** descrevendo suas alterações

## Estilo de Código

- Siga o PEP 8 para código Python
- Use nomes descritivos para variáveis e funções
- Adicione docstrings para classes e funções públicas
- Mantenha as linhas com no máximo 100 caracteres quando possível

## Convenções de Commit

Use mensagens de commit claras e descritivas:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `style:` - Formatação, ponto e vírgula faltando, etc
- `refactor:` - Refatoração de código
- `test:` - Adição de testes
- `chore:` - Tarefas de manutenção

Exemplos:
```
feat: adiciona suporte para arquivos M4A
fix: corrige bug no carregamento de playlist
docs: atualiza guia de instalação para Ubuntu 24.04
```

## Desenvolvimento Local

### Configurar Ambiente

```bash
# Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox-Retro.git
cd Jukebox-Retro

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python jukebox_retro.py

# Execute os testes
python test_jukebox.py
```

### Estrutura do Projeto

```
Jukebox-Retro/
├── jukebox_retro.py      # Aplicação principal
├── jukebox_retro.spec    # Configuração PyInstaller
├── requirements.txt      # Dependências Python
├── test_jukebox.py       # Testes unitários
├── build_linux.sh        # Script de build Linux
├── build_windows.bat     # Script de build Windows
├── README.md             # Documentação principal
├── INSTALL.md            # Guia de instalação
├── CHANGELOG.md          # Histórico de mudanças
└── CONTRIBUTING.md       # Este arquivo
```

## Áreas que Precisam de Ajuda

Algumas áreas onde contribuições seriam muito bem-vindas:

1. **Atalhos de teclado**: Adicionar suporte para atalhos (Space para play/pause, etc)
2. **Visualizador**: Adicionar visualizador de áudio estilo retro
3. **Temas**: Permitir escolha de esquemas de cor diferentes
4. **Equalizer**: Adicionar equalizer de áudio
5. **Letras**: Mostrar letras das músicas
6. **Busca**: Adicionar busca na playlist
7. **Shuffle/Repeat**: Modos de reprodução aleatória e repetição
8. **Ícone**: Criar um ícone personalizado para a aplicação
9. **Testes**: Adicionar mais testes unitários e de integração
10. **Documentação**: Traduzir documentação para outros idiomas

## Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas graciosamente
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## Perguntas?

Se você tem dúvidas, sinta-se à vontade para:

- Abrir uma issue de discussão
- Entrar em contato através do GitHub

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT.

---

Obrigado por contribuir! 🎉
