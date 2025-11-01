# 🧠 Tutorial: Comandos SQL usados no CRUD
# 🟩 1. INSERT — Inserir dados (Create)

Função: adiciona novos registros (linhas) em uma tabela.

Sintaxe básica:
```
INSERT INTO nome_tabela (coluna1, coluna2, coluna3)
VALUES (valor1, valor2, valor3);
```

Exemplo real:
```
INSERT INTO vendas (nome_produto, valor)
VALUES ('chocolate', 15);
```

👉 Adiciona um novo produto chamado “chocolate” com valor 15 na tabela vendas.

Em Python (seguro com placeholders):
```
comando = "INSERT INTO vendas (nome_produto, valor) VALUES (%s, %s)"
cursor.execute(comando, (nome_produto, valor))
```
# 🟦 2. SELECT — Consultar dados (Read)

Função: busca informações existentes no banco.

Sintaxe básica:
```
SELECT colunas FROM nome_tabela;
```

Exemplo real:
```
SELECT * FROM vendas;
```

👉 O * seleciona todas as colunas da tabela vendas.

Você pode filtrar dados com WHERE:
```
SELECT * FROM vendas WHERE nome_produto = 'chocolate';
```

Em Python:
```
comando = "SELECT * FROM vendas WHERE nome_produto = %s"
cursor.execute(comando, (nome,))
resultado = cursor.fetchall()
```
# 🟨 3. UPDATE — Atualizar dados (Update)

Função: altera valores de colunas em linhas já existentes.

Sintaxe básica:
```
UPDATE nome_tabela
SET coluna1 = novo_valor
WHERE condição;
```

Exemplo real:
```
UPDATE vendas SET valor = 20 WHERE nome_produto = 'chocolate';
```

👉 Atualiza o valor do produto “chocolate” para 20.

Em Python:
```
comando = "UPDATE vendas SET valor = %s WHERE nome_produto = %s"
cursor.execute(comando, (novo_valor, nome))
```

⚠️ Atenção: sempre use WHERE no UPDATE.
Sem ele, todas as linhas da tabela serão alteradas!

# 🟥 4. DELETE — Excluir dados (Delete)

Função: remove registros do banco.

Sintaxe básica:
```
DELETE FROM nome_tabela WHERE condição;
```

Exemplo real:
```
DELETE FROM vendas WHERE nome_produto = 'chocolate';
```

👉 Remove todas as linhas da tabela vendas cujo produto se chama “chocolate”.

Em Python:
```
comando = "DELETE FROM vendas WHERE nome_produto = %s"
cursor.execute(comando, (nome,))
```

⚠️ Sem o WHERE, o comando apagaria toda a tabela.

# 🧾 Resumo rápido
| Operação   | SQL                                     | O que faz      | Exemplo                                             |
| ---------- | --------------------------------------- | -------------- | --------------------------------------------------- |
| **CREATE** | `INSERT INTO tabela (...) VALUES (...)` | Insere dados   | `INSERT INTO vendas (...)`                          |
| **READ**   | `SELECT ... FROM tabela`                | Lê dados       | `SELECT * FROM vendas`                              |
| **UPDATE** | `UPDATE tabela SET ... WHERE ...`       | Atualiza dados | `UPDATE vendas SET valor=20`                        |
| **DELETE** | `DELETE FROM tabela WHERE ...`          | Apaga dados    | `DELETE FROM vendas WHERE nome_produto='chocolate'` |
