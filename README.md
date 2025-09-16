# 📌 Projeto API REST com FastAPI - TechBlog

Este projeto é uma API REST para o TechBlog desenvolvida em **Python 3** utilizando o framework **FastAPI**.  
A aplicação foi construída com foco em simplicidade, escalabilidade e boas práticas de desenvolvimento.

---

## 🚀 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** → Framework moderno, rápido e intuitivo para criação de APIs em Python.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** → ORM (Object Relational Mapper) para manipulação do banco de dados de forma mais produtiva e segura.
- **[SQLite](https://www.sqlite.org/)** → Banco de dados leve, simples de configurar e ideal para desenvolvimento e testes.
- **[Alembic](https://alembic.sqlalchemy.org/)** → Ferramenta para versionamento do banco de dados, facilitando o controle de migrações.
- **[bcrypt](https://pypi.org/project/bcrypt/)** → Biblioteca utilizada para criptografia segura de senhas.
- **[python-jose](https://python-jose.readthedocs.io/)** → Responsável pela geração e validação de tokens JWT para autenticação.
- **[Pydantic](https://docs.pydantic.dev/)** → Utilizado para validação de dados e definição de schemas de forma simples e robusta.

---

## 🛠️ Como Rodar a Aplicação

1. Clone este repositório:
   ```bash
   git clone tech-blog-backend
   cd tech-blog-backend
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute as migrações do banco de dados:
   ```bash
   alembic upgrade head
   ```

4. Inicie a aplicação:
   ```bash
   uvicorn src.server:app --reload --reload-dir=src
   ```

---

## 🔑 Usuários para Teste

A aplicação já conta com dois usuários pré-cadastrados para testes:

- **Administrador**  
  📧 `admin@email.com`  
  🔑 `admin123`

- **Usuário Comum**  
  📧 `user@email.com`  
  🔑 `user123`

---

## 📖 Documentação

A documentação interativa da API está disponível em:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)