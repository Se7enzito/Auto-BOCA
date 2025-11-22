# BOCA Automático | Estudo

Sistema para resolver de maneira automática exercícios que forem colocados no **BOCA** da Universidade Federal de São João Del Rei (**UFSJ**). Para entender como utilizar o sistema acesse o arquivo: COMO_USAR.md

---

# Objetivos do Projeto

Este projeto tem como objetivos:

* Trabalhar conceitos de IA e LLMs Generativas
* Procurar maneiras de melhorar o sistema do BOCA da Universidade Federal de São João Del Rei (UFSJ)
* Trabalhar conceitos de automação

---

# Funcionalidades do Projeto

- Enviar atividades no sistema BOCA da Universidade Federal de São João Del Rei (**UFSJ**), a partir do uso de LLMs que geram códigos nas linguagens: C; Python; C++; e enviam automáticamente para o sistema cada uma para sua respectiva atividade.

---

# Estrutura do Projeto

```
 project/				# Diretório do projeto
├── docs/				# Diretório com todos os documentos de atividades
├── respostas/				# Diretório com todos os códigos que são utilizados para respostas
├── main.py				# Código principal do aplicativo, código de uso geral para gerar relatórios e pesquisas
├── LICENSE				# Licença do projeto
├── SECUTIRY.md				# Instruções para relatar vunerabilidades no código
├── .gitignore				# Arquivos ignorados pelo github
├── requirements.txt			# Requerimentos para o código rodar
├── COMO_USAR.md			# Ĩnstruções de como utilizar o sistema
└── README.md				# Este arquivo
```

---

# Pré-requesitos

* Python 3.8+
* Shutil
* Requests
* Urllib3
* Selenium
* Transformers

---

# Instalação

```
git clone https://github.com/Se7enzito/Auto-BOCA.git
cd Auto-BOCA
pip install -r requirements.txt
```

---

# Como executar localmente

```
python3 -m main
```

---

# Ideias futuras

- Finalizar a API de resolução das atividades
- Melhorar a estrutura de dados utilizada para resolução dos problemas
- Conectar a API do BOCA com o Telegram, fazendo com que seja possível utilizar o sistema por telefone
