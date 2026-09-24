# PetGrid Hub API

API REST para gestão de produtos e controle de estoque de pet shops, desenvolvida em **Python**, **Flask** e **SQLite**.

Ela controla o estoque atual em relação ao estoque mínimo, custo de aquisição, preço de venda, lote e datas de entrada e validade, classificando cada produto como `ok`, `a_vencer` (próximos 30 dias), `vencido` ou `sem_validade`.

O frontend do projeto está em outro repositório: [petgrid-hub-frontend](https://github.com/maradantaspereira-eng/petgrid-hub-frontend).

## Tecnologias

- Python 3 e Flask
- Flask-OpenAPI3 (documentação Swagger/OpenAPI) e Pydantic (validação)
- Flask-SQLAlchemy e SQLite
- Flask-CORS

## Como executar

1. Crie o ambiente virtual:
   - **Linux/macOS:** `python3 -m venv env`
   - **Windows:** `python -m venv env`

2. Ative o ambiente virtual:
   - **Linux/macOS:** `source env/bin/activate`
   - **Windows:** `env\Scripts\activate`

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a API:

   ```bash
   flask run --host 0.0.0.0 --port 5001 --reload
   ```

> **Windows:** use o Prompt de Comando (cmd). No PowerShell, se a ativação do ambiente for bloqueada, rode antes `Set-ExecutionPolicy -Scope Process Bypass`. Se o comando `python` não for encontrado, use `py -m venv env`. Se o firewall perguntar sobre o acesso do Python à rede, é possível permitir ou usar `--host 127.0.0.1` no comando de execução.

As dependências estão com versões fixas no `requirements.txt` (Flask 3.1.3, Flask-Cors 6.0.5, Flask-SQLAlchemy 3.1.1, flask-openapi3 4.3.2 e pydantic 2.13.5) para que a instalação seja reproduzível.

A API estará disponível em `http://localhost:5001` e a documentação interativa (Swagger) em `http://localhost:5001/openapi/swagger`.

O banco `database.db` e as 6 categorias iniciais (Rações, Petiscos, Higiene, Brinquedos, Medicamentos e Acessórios) são criados automaticamente na primeira execução.

## Rotas

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| GET | `/categorias` | Lista as categorias | 200 |
| GET | `/produtos` | Lista os produtos, com nome da categoria e status de validade | 200 |
| GET | `/produtos/{id}` | Busca um produto pelo ID | 200, 404 |
| POST | `/produtos` | Cadastra um produto | 201, 404, 422 |
| PUT | `/produtos/{id}` | Atualiza parcialmente um produto | 200, 400, 404, 422 |
| DELETE | `/produtos/{id}` | Remove um produto | 200, 404 |
| GET | `/resumo` | Indicadores do estoque calculados no servidor | 200 |

## Validações

- `nome` e `categoria_id` são obrigatórios; a categoria precisa existir (404 caso contrário).
- Estoques, custo e preço não podem ser negativos (422).
- As datas devem estar no formato `AAAA-MM-DD` e a validade não pode ser anterior à entrada (422 no cadastro, 400 na atualização).

## Estrutura

```
app.py          # rotas e documentação OpenAPI
database/       # configuração do SQLite/SQLAlchemy
model/          # tabelas Produto e Categoria (relacionamento 1:N)
schemas/        # schemas Pydantic de requisição e resposta
logger.py       # log de operações em log/app.log
```
