## Como utilizar esta seção para gerar os dados ficticios do projeto?

#### Caso não queira utilizar os dados ja disponiveis na pasta, basta seguir o guia abaixo para gerar sua base;

- Primeiro de tudo se atente em estar com o ambinete ativo para gerar os dados, caso ainda não tenha iniciado o mesmo:
```
uv sync 
```

- Após ativar o ambiente, abra a pasta onde o gerador se encontra e rode os comandos com o uv:
```
cd data
uv run data_generator.py

```

#### Feito isso, seus dados estarão disponiveis na mesma pasta. Agora fica pendente só de enviar eles para o Databricks.