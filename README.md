# 🚀 Sistema de Atendimento ServPub   

**Cadastre, gerencie e documente serviços municipais com facilidade e eficiência!**  

---

## ✨ Funcionalidades:

✅ **Cadastro Inteligente**  
- Valida CPF automaticamente  
- Armazena dados completos (endereço, contato e mais)  
- Edição rápida e prática  

📄 **Gerador de Documentos Profissional**  
- Cria ordens de serviço em PDF *com um clique*  
- Números de protocolo automáticos e sequenciais  

📊 **Relatórios Poderosos**  
- Exporta dados para Excel em segundos  
- Organiza informações para análise  

🔍 **Busca Rápida**  
- Encontre qualquer cidadão pelo CPF em instantes  

---

## ⚡ Como Começar  

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/seu-usuario/servpub.git
   cd servpub
   ```

2. **Prepare o ambiente**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. **Iniciar!** 🚀  
   ```bash
   python main.py
   ```

   Acesse no navegador: `http://localhost:8080`  

---

## 🎮 Manual Rápido  

### 🔎 Buscar um Cidadão  
1. Digite o CPF (pode ser com ou sem pontuação)  
2. Clique em **"Buscar CPF"**  
3. Pronto! Cadastro encontrado ou opção para cadastrar novo  

### ✏️ Cadastrar Novo  
1. CPF não encontrado? Sem problemas!  
2. Clique em **"Cadastrar novo"**  
3. Preencha os dados e salve  

### 📤 Exportar Relatórios  
1. Clique em **"Salvar na Planilha"** para Excel  
2. **"Abrir Planilha"** visualiza o arquivo gerado  

### 🖨️ Gerar Ordem de Serviço  
1. Localize o cadastro  
2. Clique em **"Visualizar PDF"**  
3. Imprima ou salve o documento profissional  

---

## 🛠️ Arquivos Importantes  

| Arquivo          | Função                          |
|------------------|---------------------------------|
| `main.py`        | Cérebro do sistema (lógica principal) |
| `interface.py`   | Interface simples e funcional |
| `dados.json`     | Banco de dados |
| `atendimentos.xls` | Relatórios em Excel |
| `protocolo.txt`  | Contador de protocolos |

---

## 💡 Dicas Pro  

🔸 **Backup é vida!** Mantenha cópias do `dados.json`  
🔸 **Personalize facilmente** os campos em `interface.py`  
🔸 **Quer um PDF diferente?** Edite a classe `PDF` no `main.py`  

---

## 🤝 Quer Contribuir?  

1. Faça um fork 🍴  
2. Crie sua branch (`git checkout -b feature/sua-ideia-incrivel`)  
3. Commit suas mudanças (`git commit -m 'Adiciona feature X'`)  
4. Push (`git push origin feature/sua-ideia-incrivel`)  
5. Abra um Pull Request  

---

## 📜 Licença  

MIT - Use, modifique e compartilhe à vontade!  
