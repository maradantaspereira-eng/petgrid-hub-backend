# PetGrid Hub API

API REST para gestão de produtos e estoque de um pet shop.

## Como executar

1. Crie o ambiente virtual:
```bash
python3 -m venv env
```

2. Ative o ambiente:
```bash
source env/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a API:
```bash
flask run --host 0.0.0.0 --port 5001 --reload
```

A API estará disponível em `http://localhost:5001`.

O Swagger estará em `http://localhost:5001/openapi/swagger`.
