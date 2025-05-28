# 🤖 Robotic Enterprise Framework (REFramework) em Python com BotCity

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![BotCity Framework](https://img.shields.io/badge/BotCity_Framework-Python-green?logo=robot-framework&logoColor=white)](https://www.botcity.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ---

## 📝 Visão Geral do Projeto

Este projeto consiste em uma implementação da arquitetura **Robotic Enterprise Framework (REFramework)** utilizando o poderoso **BotCity Framework** em Python. Nosso objetivo é oferecer uma base robusta e escalável para o desenvolvimento de robôs de automação transacionais, incorporando fases de inicialização, obtenção e processamento de dados, e finalização, além de um tratamento de exceções e logging detalhado.

**✨ Propósito:** O propósito deste projeto é **transpor anos de experiência e os padrões consolidados do UiPath REFramework para o ecossistema Python**, utilizando as capacidades do BotCity Framework. Busca-se criar uma fundação sólida e familiar para automações corporativas em Python, replicando a resiliência e a estrutura que garantem a robustez em ambientes de produção.

---

## 🚀 Primeiros Passos

Siga as instruções abaixo para configurar e executar a arquitetura base em seu ambiente local.

### ⚙️ Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

* **Python 3.11:** A versão do Python recomendada e utilizada no desenvolvimento.
* **Google Chrome:** O navegador web essencial para a execução das automações web.
* **Chromedriver:** **Crucial!** O driver do Chrome deve corresponder **exatamente à versão do seu Google Chrome**.

### 🛠️ Configuração do Ambiente

1.  **Clonagem do Repositório (se usando Git):**
    ```bash
    git clone [https://github.com/seu-usuario/REPyBot.git](https://github.com/seu-usuario/REPyBot.git)
    cd REPyBot
    ```
    *Se não estiver usando Git, navegue diretamente até a pasta onde salvou o projeto.*

2.  **Criação e Ativação do Ambiente Virtual (`.venv`):**
    Recomendamos fortemente o uso de um ambiente virtual para gerenciar as dependências do projeto de forma isolada.
    ```bash
    python3.11 -m venv .venv
    source ./.venv/bin/activate
    ```

3.  **Instalação das Dependências do Projeto:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Chromedriver:**
    * 📥 Baixe o `chromedriver` correspondente à sua versão do Google Chrome em: [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/) (Para Chrome versões 115+).
    * 📦 Após o download, extraia o arquivo `.zip`.
    * ➡️ Mova o executável `chromedriver` para um diretório centralizado em seu sistema, por exemplo, `~/drivers/`.
        ```bash
        mkdir -p ~/drivers/
        mv /caminho/do/seu/download/chromedriver ~/drivers/
        ```
    * 🔒 Conceda permissão de execução ao driver:
        ```bash
        chmod +x ~/drivers/chromedriver
        ```

5.  **Ajuste do Arquivo de Configuração (`config/config.yaml`):**
    Abra o arquivo `config/config.yaml` e personalize as variáveis conforme o seu ambiente e as necessidades específicas do robô.
    ```yaml
    # config/config.yaml
    app_settings:
      url_google: "[https://www.google.com](https://www.google.com)" # Exemplo: URL inicial de navegação
      driver_path: "/home/claudio-sousa/drivers/chromedriver" # ⚠️ AJUSTE ESTE CAMINHO PARA O SEU CHROMEDRIVER
    # ... outras configurações (credenciais, tempos de espera, etc.)
    ```
    **É fundamental que o `driver_path` aponte para o local exato do seu executável `chromedriver`.**

---

## 🏃‍♀️ Como Executar a Arquitetura Base

Com o ambiente configurado e ativado, execute a estrutura base do REFramework:

```bash
# Verifique se o ambiente virtual está ativo
source ./.venv/bin/activate

# Inicie a arquitetura
python main.py