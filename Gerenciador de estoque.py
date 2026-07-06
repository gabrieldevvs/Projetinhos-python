#!/usr/bin/env python
# coding: utf-8

# ### Gerenciador de Estoque e Validade

# ### voce deve:
# cadastrar produtos (nome, quantidade, validade e lote)
# controlar quantidade
# Atualizar estoque (adicionar quantidade, remover quantidade)
# buscar produtos(nome, lote)
# alertar produtos vencidos(produtos vencidos)
# 
# dica:antes criar a conexão com o banco de dados onde irá ser armazenado as informações.

# In[3]:


#importando a biblioteca
import pyodbc #importando a biblioteca pyodbc
print(pyodbc.drivers()) #buscando pelo banco SQLite3 ODBC Driver   


# In[4]:


#criar conexão com o banco de dados
conexao_banco = ("Driver={SQLite3 ODBC Driver};"
                 "Server=localhost;"
                 "Database=gerenciador.sqlite"
                )
conexao = pyodbc.connect(conexao_banco)
cursor = conexao.cursor()
print('conexao bem sucedida')


# In[24]:


cursor.execute("""
CREATE TABLE estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    quantidade INTEGER,
    validade TEXT,
    lote TEXT
)
""")
conexao.commit()


# In[5]:


#função para verificar produto vencido
from datetime import datetime
def verificar_validade(valido):
    data_validade = datetime.strptime(valido, '%m/%Y')
    hoje = datetime.now()
    if (data_validade.year, data_validade.month) < (hoje.year, hoje.month):
        return 'Produto vencido'
    else:
        return 'Produto dentro da validade'

#menu de opções 
while True:
    menu = input('Bem vindo ao gerenciador de estoque.Digite:\n 1-para cadastrar\n 2-para deletar\n 3-para atualizar estoque\n 4-consultar produto\n 5-sair')
#saindo do menu e encerrando o programa
    if menu == '5':
        break
     #cadastrando produtos
    elif menu == '1':
        if menu.isdigit():
            cadastro_produtos = input('digite o nome do produto')
            if cadastro_produtos.isalpha():
                cadastro_qtde = input('digite a quantidade de produtos')
                if cadastro_qtde.isdigit():
                    for i in range(int(cadastro_qtde)):
                        cadastro_validade = input('digite a data de validade do produto (MM/AAAA)')
                        resultado = verificar_validade(cadastro_validade)
                        print(resultado)
                        if len(cadastro_validade) == 7 and '/' in cadastro_validade:
                            cadastro_lote = input('digite o lote do produto de 5 numeros')
                            if len(cadastro_lote) == 5:
                                cursor.execute("""
                                INSERT INTO estoque(produto, quantidade, validade, lote)
                                VALUES (?, ?, ?, ?)
                                """,(
                                    cadastro_produtos,
                                    cadastro_qtde,
                                    cadastro_validade,
                                    cadastro_lote
                                ))
                                conexao.commit()
                                print('produto cadastrado com sucesso')

                            else:('lote inválido')
                        else:('data de validade inválida')
                else:('quantidade inválida')
            else:('nome inválido')

#apagar um produto
    elif menu == '2':
        if menu.isdigit():  
            produtos = input('digite o nome do produto que deseja excluir')
            cursor.execute("""
            SELECT * FROM estoque
            WHERE Produto = ?
            """,(produtos,))
            resultado = cursor.fetchone()
            if resultado != None:
                cursor.execute("""
                DELETE FROM estoque
                WHERE Produto = ?
                """,(produtos,))
                cursor.commit()
                print('produto excluido com sucesso')
            else:
                print('o produto não existe')
#atualizando produto no banco
    elif menu == '3':
        if menu.isdigit():
            atualizar_produto =  input('digite o produto')
            cursor.execute("""
            SELECT produto, quantidade
            FROM estoque
            WHERE produto = ?
            """, (atualizar_produto,))
            resultado = cursor.fetchone()
            if resultado:
                print("\nProduto encontrado:")
                print(f"Produto: {resultado[0]}")
                print(f"Quantidade: {resultado[1]}")
                alterar = input("\nDeseja alterar? (Sim/Nao): ")
                if alterar == 'sim':
                    novo_produto = input('nome do novo produto')
                    nova_quantidade = input('digite a nova quantidade')
                    cursor.execute("""
                    UPDATE estoque
                    SET produto = ?, quantidade =?
                    WHERE produto = ?
                    """,(novo_produto, nova_quantidade, atualizar_produto))
                    conexao.commit()
                    print('produto atualizado com sucesso')
                else:
                    print("alteração cancelada")  
                    break
#busca o produto no banco
    elif menu == "4":
        if menu.isdigit():
            buscar_produto = input('Qual e o nome do produto ?')
            cursor.execute("""
            SELECT produto, validade
            FROM estoque
            WHERE produto = ?
            """, (buscar_produto,))
            resultado = cursor.fetchone()
            if resultado:
                status = verificar_validade(resultado[1])
                print(f"Produto: {resultado[0]}")
                print(f"Validade: {resultado[1]}")
                print(status)
            else:
                print('o produto nao existe')             
    else: 
        print('produto não encontrado')


# In[7]:


cursor.close()
conexao.close()


# In[22]:





# In[ ]:




