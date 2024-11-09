# Cofre de Senhas 🔒

Cofre de Senhas é uma simples aplicação WebGUI onde você pode gerar senhas automaticamente, em um banco de dados local e criptografado.<br/> Para ter acesso a todas suas senhas é necessário apenas lembrar de uma única chave de descriptogração!

## Como Utilizar? 🤔

É apenas inserir um usuário ao qual serão vinculadas as senhas, guardar sua chave em um lugar segura, inserir o nome da senha, por exemplo "YouTube", e clicar em "Gerar Senha!".

## Documentação 📄

A aplicação utiliza a biblioteca de Python "cryptography" para realizar as operações de criptografia e descriptografia, a biblioteca Flask para construir a WebGUI, e o banco de dados SQLite3 para persitência dos dados.

Além disso, a aplicação é estruturada baseada na arquitetura MVC, na pasta "model" estão os arquivos com as classes representados as tabelas do bando de dados, em "services" as funções que tratam de criptografia e conexão com o banco de dados, em "appController.py" as definições das rotas da aplicação e em "static" e "templates" os arquivos HTML e CSS das páginas da aplicação.

## Referências 🆙

Grandes agradecimentos:<br>
 <a href="https://www.geeksforgeeks.org/generating-strong-password-using-python/">Geeks for Geeks - Generating Strong Password using Python</a><br>
<a href="https://cryptography.io/en/latest/">pyca/cryptography library</a><br>
<a href="https://flask.palletsprojects.com/en/stable/">Flask</a>
