
# Estrutura da pasta `src/`

> Esta pasta contém o núcleo da aplicação Bricks-Agent, responsável pela interface, lógica de negócio, integração com Databricks e configuração do agente inteligente.

## Descrição dos arquivos

- **app.py**  
	Interface principal em Streamlit. Permite ao usuário descrever a aplicação desejada, envia a requisição para a chain RAG e exibe as recomendações de materiais. Gerencia o histórico do chat e inicializa a lógica de recomendação.

- **main.py**  
	Implementa toda a lógica de backend: define a chain RAG, integra com busca vetorial (Vector Search) e LLM do Databricks, formata o contexto dos materiais e carrega o template do prompt. É o "cérebro" do agente.

- **settings.py**  
	Centraliza o carregamento das variáveis de ambiente do projeto (.env), facilitando o acesso seguro a endpoints, tokens e configurações do Databricks e MLflow.

- **prompt_template.txt**  
	Template do prompt utilizado pelo LLM. Define o formato, tom e regras para as respostas do agente, garantindo consistência e foco comercial nas recomendações.

- **__init__.py**  
	Arquivo de inicialização do pacote Python. Permite que a pasta seja importada como módulo, mesmo estando vazio.

## Fluxo resumido

1. O usuário interage via `app.py` (Streamlit).
2. O texto é processado e enviado para a chain definida em `main.py`.
3. A chain utiliza busca vetorial e LLM do Databricks, com contexto formatado pelo template em `prompt_template.txt`.
4. As configurações e segredos são acessados via `settings.py`.
5. O resultado é exibido ao usuário na interface.

---
Para detalhes sobre a arquitetura geral, consulte o README principal do projeto.
