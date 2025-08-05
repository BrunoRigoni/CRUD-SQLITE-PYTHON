import sqlite3
import config
from datetime import datetime
import os
import csv
import pandas as pd


def limpar_terminal():
    """Limpa o terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def garantir_pastas_existem():
    """Garante que as pastas relatorios e inventario existem"""
    pastas = ['relatorios', 'inventario',
              'inventario/download_base', 'inventario/upload_base']
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta '{pasta}' criada com sucesso!")


def menu_produtos(connect, user_email):
    """Menu de gerenciamento de produtos"""
    while True:
        print("\n" + "="*50)
        print(f"GERENCIAMENTO DE PRODUTOS - {user_email}")
        print("="*50)
        print("1. Listar produtos")
        print("2. Adicionar produto")
        print("3. Editar produto")
        print("4. Remover produto")
        print("5. Buscar produto")
        print("6. Gerar relatório Excel")
        print("7. Gerar planilha base para importação")
        print("8. Importar produtos da pasta upload_base")
        print("9. Voltar ao menu principal")
        print("-"*50)

        try:
            opcao = int(input("Digite a opção desejada: "))

            if opcao == 1:
                listar_produtos(connect, user_email)
            elif opcao == 2:
                adicionar_produto(connect, user_email)
            elif opcao == 3:
                editar_produto(connect, user_email)
            elif opcao == 4:
                remover_produto(connect, user_email)
            elif opcao == 5:
                buscar_produto(connect, user_email)
            elif opcao == 6:
                gerar_relatorio_produtos_excel(connect, user_email)
            elif opcao == 7:
                gerar_planilha_base_produtos(connect, user_email)
            elif opcao == 8:
                importar_produtos_upload_base(connect, user_email)
            elif opcao == 9:
                break
            else:
                print("Opção inválida!")

        except ValueError:
            print("Erro: Digite apenas números!")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def listar_produtos(connect, user_email):
    """Lista todos os produtos cadastrados do usuário"""
    print("\n" + "-"*80)
    print(f"LISTA DE PRODUTOS - {user_email}")
    print("-"*80)
    print(f"{'ID':<5} {'NOME':<30} {'PREÇO':<10} {'QTD':<5} {'CATEGORIA':<15} {'DATA CADASTRO':<20}")
    print("-"*80)

    cursor = connect.execute('''
        SELECT id, nome, preco, quantidade, categoria, data_cadastro
        FROM produtos
        WHERE usuario_email = ?
        ORDER BY nome
    ''', (user_email,))

    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto cadastrado!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    for produto in produtos:
        data_formatada = produto[5][:10] if produto[5] else "N/A"
        print(
            f"{produto[0]:<5} {produto[1]:<30} R$ {produto[2]:<8.2f} {produto[3]:<5} {produto[4]:<15} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def adicionar_produto(connect, user_email):
    """Adiciona um novo produto"""
    print("\n" + "-"*50)
    print("ADICIONAR PRODUTO")
    print("-"*50)

    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Nome é obrigatório!")
        return

    try:
        preco = float(input("Preço: R$ "))
        if preco <= 0:
            print("Preço deve ser maior que zero!")
            return
    except ValueError:
        print("Preço inválido!")
        return

    try:
        quantidade = int(input("Quantidade em estoque: "))
        if quantidade < 0:
            print("Quantidade não pode ser negativa!")
            return
    except ValueError:
        print("Quantidade inválida!")
        return

    categoria = input("Categoria (opcional): ").strip()

    try:
        connect.execute('''
            INSERT INTO produtos (nome, preco, quantidade, categoria, usuario_email)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, preco, quantidade, categoria, user_email))
        connect.commit()
        print("Produto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")


def editar_produto(connect, user_email):
    """Edita um produto existente"""
    print("\n" + "-"*50)
    print("EDITAR PRODUTO")
    print("-"*50)

    produto_id_input = input("Digite o ID do produto: ").strip()
    if not produto_id_input:
        print("ID é obrigatório!")
        return

    try:
        produto_id = int(produto_id_input)
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o produto existe e pertence ao usuário
    cursor = connect.execute(
        'SELECT * FROM produtos WHERE id = ? AND usuario_email = ?', (produto_id, user_email))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado ou não pertence a você!")
        return

    print(f"\nEditando produto: {produto[1]}")
    print("Deixe em branco (pressione Enter) para manter o valor atual")

    nome = input(f"Nome atual ({produto[1]}): ").strip()
    if not nome:
        nome = produto[1]

    preco_input = input(f"Preço atual (R$ {produto[2]}): ").strip()
    if not preco_input:
        preco = produto[2]
    else:
        try:
            preco = float(preco_input)
            if preco <= 0:
                print("Preço deve ser maior que zero!")
                return
        except ValueError:
            print("Preço inválido!")
            return

    qtd_input = input(f"Quantidade atual ({produto[3]}): ").strip()
    if not qtd_input:
        quantidade = produto[3]
    else:
        try:
            quantidade = int(qtd_input)
            if quantidade < 0:
                print("Quantidade não pode ser negativa!")
                return
        except ValueError:
            print("Quantidade inválida!")
            return

    categoria = input(f"Categoria atual ({produto[4] or 'N/A'}): ").strip()
    if not categoria:
        categoria = produto[4]

    try:
        connect.execute('''
            UPDATE produtos
            SET nome = ?, preco = ?, quantidade = ?, categoria = ?
            WHERE id = ? AND usuario_email = ?
        ''', (nome, preco, quantidade, categoria, produto_id, user_email))
        connect.commit()
        print("Produto atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")


def remover_produto(connect, user_email):
    """Remove um produto"""
    print("\n" + "-"*50)
    print("REMOVER PRODUTO")
    print("-"*50)

    try:
        produto_id = int(input("Digite o ID do produto: "))
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o produto existe e pertence ao usuário
    cursor = connect.execute(
        'SELECT nome FROM produtos WHERE id = ? AND usuario_email = ?', (produto_id, user_email))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado ou não pertence a você!")
        return

    confirmacao = input(
        f"Tem certeza que deseja remover '{produto[0]}'? (s/n): ").strip().lower()

    if confirmacao in ['s', 'sim']:
        try:
            connect.execute(
                'DELETE FROM produtos WHERE id = ? AND usuario_email = ?', (produto_id, user_email))
            connect.commit()
            print("Produto removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
    else:
        print("Operação cancelada.")


def buscar_produto(connect, user_email):
    """Busca produtos por nome ou categoria"""
    print("\n" + "-"*50)
    print("BUSCAR PRODUTO")
    print("-"*50)
    print("1. Buscar por nome")
    print("2. Buscar por categoria")

    try:
        opcao = int(input("Digite a opção: "))
    except ValueError:
        print("Opção inválida!")
        return

    if opcao == 1:
        termo = input("Digite o nome do produto: ").strip()
        if not termo:
            print("Termo de busca é obrigatório!")
            return

        cursor = connect.execute('''
            SELECT id, nome, preco, quantidade, categoria, data_cadastro
            FROM produtos
            WHERE nome LIKE ? AND usuario_email = ?
            ORDER BY nome
        ''', (f'%{termo}%', user_email))

    elif opcao == 2:
        categoria = input("Digite a categoria: ").strip()
        if not categoria:
            print("Categoria é obrigatória!")
            return

        cursor = connect.execute('''
            SELECT id, nome, preco, quantidade, categoria, data_cadastro
            FROM produtos
            WHERE categoria LIKE ? AND usuario_email = ?
            ORDER BY nome
        ''', (f'%{categoria}%', user_email))

    else:
        print("Opção inválida!")
        return

    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto encontrado!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    print("\n" + "-"*80)
    print("RESULTADOS DA BUSCA")
    print("-"*80)
    print(f"{'ID':<5} {'NOME':<30} {'PREÇO':<10} {'QTD':<5} {'CATEGORIA':<15} {'DATA CADASTRO':<20}")
    print("-"*80)

    for produto in produtos:
        data_formatada = produto[5][:10] if produto[5] else "N/A"
        print(
            f"{produto[0]:<5} {produto[1]:<30} R$ {produto[2]:<8.2f} {produto[3]:<5} {produto[4]:<15} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def gerar_relatorio_produtos_excel(connect, user_email):
    """Gera relatório de produtos em Excel"""
    print("\n" + "-"*50)
    print("GERAR RELATÓRIO DE PRODUTOS - EXCEL")
    print("-"*50)

    try:
        # Garantir que a pasta relatorios existe
        garantir_pastas_existem()

        # Buscar todos os produtos do usuário
        cursor = connect.execute('''
            SELECT id, nome, preco, quantidade, categoria, data_cadastro
            FROM produtos
            WHERE usuario_email = ?
            ORDER BY nome
        ''', (user_email,))

        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto encontrado para gerar relatório!")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        # Criar DataFrame
        df = pd.DataFrame(produtos, columns=[
                          'ID', 'Nome', 'Preço', 'Quantidade', 'Categoria', 'Data Cadastro'])

        # Formatar preços
        df['Preço'] = df['Preço'].apply(lambda x: f"R$ {x:.2f}")

        # Formatar datas
        df['Data Cadastro'] = df['Data Cadastro'].apply(
            lambda x: x[:10] if x else "N/A")

        # Nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorios/relatorio_produtos_{user_email.replace('@', '_').replace('.', '_')}_{timestamp}.xlsx"

        # Criar writer do Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Planilha principal
            df.to_excel(writer, sheet_name='Produtos', index=False)

            # Obter a planilha para formatação
            worksheet = writer.sheets['Produtos']

            # Ajustar largura das colunas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"\n✅ Relatório gerado com sucesso!")
        print(f"📁 Arquivo: {filename}")
        print(f"📊 Total de produtos: {len(produtos)}")

        # Estatísticas adicionais
        total_valor_estoque = sum(produto[2] * produto[3]
                                  for produto in produtos)
        produtos_baixo_estoque = sum(
            1 for produto in produtos if produto[3] <= 10)

        print(f"💰 Valor total em estoque: R$ {total_valor_estoque:.2f}")
        print(
            f"⚠️  Produtos com baixo estoque (≤10): {produtos_baixo_estoque}")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except ImportError:
        print("❌ Erro: Biblioteca 'openpyxl' não encontrada!")
        print("💡 Para instalar: pip install openpyxl")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def menu_clientes(connect, user_email):
    """Menu de gerenciamento de clientes"""
    while True:
        print("\n" + "="*50)
        print(f"GERENCIAMENTO DE CLIENTES - {user_email}")
        print("="*50)
        print("1. Listar clientes")
        print("2. Adicionar cliente")
        print("3. Editar cliente")
        print("4. Remover cliente")
        print("5. Buscar cliente")
        print("6. Voltar ao menu principal")
        print("-"*50)

        try:
            opcao = int(input("Digite a opção desejada: "))

            if opcao == 1:
                listar_clientes(connect, user_email)
            elif opcao == 2:
                adicionar_cliente(connect, user_email)
            elif opcao == 3:
                editar_cliente(connect, user_email)
            elif opcao == 4:
                remover_cliente(connect, user_email)
            elif opcao == 5:
                buscar_cliente(connect, user_email)
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

        except ValueError:
            print("Erro: Digite apenas números!")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def listar_clientes(connect, user_email):
    """Lista todos os clientes cadastrados do usuário"""
    print("\n" + "-"*80)
    print(f"LISTA DE CLIENTES - {user_email}")
    print("-"*80)
    print(f"{'ID':<5} {'NOME':<30} {'EMAIL':<25} {'TELEFONE':<15} {'DATA CADASTRO':<20}")
    print("-"*80)

    cursor = connect.execute('''
        SELECT id, nome, email, telefone, data_cadastro
        FROM clientes
        WHERE usuario_email = ?
        ORDER BY nome
    ''', (user_email,))

    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente cadastrado!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    for cliente in clientes:
        data_formatada = cliente[4][:10] if cliente[4] else "N/A"
        email = cliente[2] or "N/A"
        telefone = cliente[3] or "N/A"
        print(
            f"{cliente[0]:<5} {cliente[1]:<30} {email:<25} {telefone:<15} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def adicionar_cliente(connect, user_email):
    """Adiciona um novo cliente"""
    print("\n" + "-"*50)
    print("ADICIONAR CLIENTE")
    print("-"*50)

    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome é obrigatório!")
        return

    email = input("Email (opcional): ").strip()
    telefone = input("Telefone (opcional): ").strip()
    endereco = input("Endereço (opcional): ").strip()

    try:
        connect.execute('''
            INSERT INTO clientes (nome, email, telefone, endereco, usuario_email)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, telefone, endereco, user_email))
        connect.commit()
        print("Cliente adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")


def editar_cliente(connect, user_email):
    """Edita um cliente existente"""
    print("\n" + "-"*50)
    print("EDITAR CLIENTE")
    print("-"*50)

    cliente_id_input = input("Digite o ID do cliente: ").strip()
    if not cliente_id_input:
        print("ID é obrigatório!")
        return

    try:
        cliente_id = int(cliente_id_input)
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o cliente existe e pertence ao usuário
    cursor = connect.execute(
        'SELECT * FROM clientes WHERE id = ? AND usuario_email = ?', (cliente_id, user_email))
    cliente = cursor.fetchone()

    if not cliente:
        print("Cliente não encontrado ou não pertence a você!")
        return

    print(f"\nEditando cliente: {cliente[1]}")
    print("Deixe em branco (pressione Enter) para manter o valor atual")

    nome = input(f"Nome atual ({cliente[1]}): ").strip()
    if not nome:
        nome = cliente[1]

    email = input(f"Email atual ({cliente[2] or 'N/A'}): ").strip()
    if not email:
        email = cliente[2]

    telefone = input(f"Telefone atual ({cliente[3] or 'N/A'}): ").strip()
    if not telefone:
        telefone = cliente[3]

    endereco = input(f"Endereço atual ({cliente[4] or 'N/A'}): ").strip()
    if not endereco:
        endereco = cliente[4]

    try:
        connect.execute('''
            UPDATE clientes
            SET nome = ?, email = ?, telefone = ?, endereco = ?
            WHERE id = ? AND usuario_email = ?
        ''', (nome, email, telefone, endereco, cliente_id, user_email))
        connect.commit()
        print("Cliente atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")


def remover_cliente(connect, user_email):
    """Remove um cliente"""
    print("\n" + "-"*50)
    print("REMOVER CLIENTE")
    print("-"*50)

    try:
        cliente_id = int(input("Digite o ID do cliente: "))
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o cliente existe e pertence ao usuário
    cursor = connect.execute(
        'SELECT nome FROM clientes WHERE id = ? AND usuario_email = ?', (cliente_id, user_email))
    cliente = cursor.fetchone()

    if not cliente:
        print("Cliente não encontrado ou não pertence a você!")
        return

    confirmacao = input(
        f"Tem certeza que deseja remover '{cliente[0]}'? (s/n): ").strip().lower()

    if confirmacao in ['s', 'sim']:
        try:
            connect.execute(
                'DELETE FROM clientes WHERE id = ? AND usuario_email = ?', (cliente_id, user_email))
            connect.commit()
            print("Cliente removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
    else:
        print("Operação cancelada.")


def buscar_cliente(connect, user_email):
    """Busca clientes por nome ou email"""
    print("\n" + "-"*50)
    print("BUSCAR CLIENTE")
    print("-"*50)
    print("1. Buscar por nome")
    print("2. Buscar por email")

    try:
        opcao = int(input("Digite a opção: "))
    except ValueError:
        print("Opção inválida!")
        return

    if opcao == 1:
        termo = input("Digite o nome do cliente: ").strip()
        if not termo:
            print("Termo de busca é obrigatório!")
            return

        cursor = connect.execute('''
            SELECT id, nome, email, telefone, data_cadastro
            FROM clientes
            WHERE nome LIKE ? AND usuario_email = ?
            ORDER BY nome
        ''', (f'%{termo}%', user_email))

    elif opcao == 2:
        email = input("Digite o email: ").strip()
        if not email:
            print("Email é obrigatório!")
            return

        cursor = connect.execute('''
            SELECT id, nome, email, telefone, data_cadastro
            FROM clientes
            WHERE email LIKE ? AND usuario_email = ?
            ORDER BY nome
        ''', (f'%{email}%', user_email))

    else:
        print("Opção inválida!")
        return

    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente encontrado!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    print("\n" + "-"*80)
    print("RESULTADOS DA BUSCA")
    print("-"*80)
    print(f"{'ID':<5} {'NOME':<30} {'EMAIL':<25} {'TELEFONE':<15} {'DATA CADASTRO':<20}")
    print("-"*80)

    for cliente in clientes:
        data_formatada = cliente[4][:10] if cliente[4] else "N/A"
        email = cliente[2] or "N/A"
        telefone = cliente[3] or "N/A"
        print(
            f"{cliente[0]:<5} {cliente[1]:<30} {email:<25} {telefone:<15} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def menu_vendas(connect, user_email):
    """Menu de gerenciamento de vendas"""
    while True:
        print("\n" + "="*50)
        print(f"GERENCIAMENTO DE VENDAS - {user_email}")
        print("="*50)
        print("1. Nova venda")
        print("2. Listar vendas")
        print("3. Buscar venda")
        print("4. Relatório de vendas")
        print("5. Gerar relatório Excel")
        print("6. Voltar ao menu principal")
        print("-"*50)

        try:
            opcao = int(input("Digite a opção desejada: "))

            if opcao == 1:
                nova_venda(connect, user_email)
            elif opcao == 2:
                listar_vendas(connect, user_email)
            elif opcao == 3:
                buscar_venda(connect, user_email)
            elif opcao == 4:
                relatorio_vendas(connect, user_email)
            elif opcao == 5:
                gerar_relatorio_vendas_excel(connect, user_email)
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

        except ValueError:
            print("Erro: Digite apenas números!")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def nova_venda(connect, user_email):
    """Registra uma nova venda"""
    print("\n" + "-"*50)
    print("NOVA VENDA")
    print("-"*50)

    # Listar clientes do usuário
    print("Clientes disponíveis:")
    cursor = connect.execute(
        'SELECT id, nome FROM clientes WHERE usuario_email = ? ORDER BY nome', (user_email,))
    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente cadastrado! Cadastre um cliente primeiro.")
        return

    for cliente in clientes:
        print(f"{cliente[0]} - {cliente[1]}")

    try:
        cliente_id = int(input("\nDigite o ID do cliente: "))
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o cliente existe e pertence ao usuário
    cursor = connect.execute(
        'SELECT nome FROM clientes WHERE id = ? AND usuario_email = ?', (cliente_id, user_email))
    cliente = cursor.fetchone()

    if not cliente:
        print("Cliente não encontrado ou não pertence a você!")
        return

    # Listar produtos do usuário
    print(f"\nProdutos disponíveis para {cliente[0]}:")
    cursor = connect.execute(
        'SELECT id, nome, preco, quantidade FROM produtos WHERE quantidade > 0 AND usuario_email = ? ORDER BY nome', (user_email,))
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto em estoque!")
        return

    for produto in produtos:
        print(
            f"{produto[0]} - {produto[1]} - R$ {produto[2]:.2f} - Estoque: {produto[3]}")

    try:
        produto_id = int(input("\nDigite o ID do produto: "))
    except ValueError:
        print("ID inválido!")
        return

    # Verificar se o produto existe, tem estoque e pertence ao usuário
    cursor = connect.execute(
        'SELECT nome, preco, quantidade FROM produtos WHERE id = ? AND usuario_email = ?', (produto_id, user_email))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado ou não pertence a você!")
        return

    if produto[2] <= 0:
        print("Produto sem estoque!")
        return

    try:
        quantidade = int(input(f"Quantidade (máximo {produto[2]}): "))
        if quantidade <= 0:
            print("Quantidade deve ser maior que zero!")
            return
        if quantidade > produto[2]:
            print("Quantidade maior que o estoque disponível!")
            return
    except ValueError:
        print("Quantidade inválida!")
        return

    total = produto[1] * quantidade

    print(f"\nResumo da venda:")
    print(f"Cliente: {cliente[0]}")
    print(f"Produto: {produto[0]}")
    print(f"Quantidade: {quantidade}")
    print(f"Preço unitário: R$ {produto[1]:.2f}")
    print(f"Total: R$ {total:.2f}")

    confirmacao = input("\nConfirmar venda? (s/n): ").strip().lower()

    if confirmacao in ['s', 'sim']:
        try:
            # Registrar a venda
            connect.execute('''
                INSERT INTO vendas (cliente_id, produto_id, quantidade, preco_unitario, total, usuario_email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cliente_id, produto_id, quantidade, produto[1], total, user_email))

            # Atualizar estoque
            nova_quantidade = produto[2] - quantidade
            connect.execute('UPDATE produtos SET quantidade = ? WHERE id = ? AND usuario_email = ?',
                            (nova_quantidade, produto_id, user_email))

            connect.commit()
            print("Venda registrada com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar venda: {e}")
    else:
        print("Venda cancelada.")


def listar_vendas(connect, user_email):
    """Lista todas as vendas do usuário"""
    print("\n" + "-"*100)
    print(f"LISTA DE VENDAS - {user_email}")
    print("-"*100)
    print(f"{'ID':<5} {'CLIENTE':<25} {'PRODUTO':<25} {'QTD':<5} {'PREÇO UN.':<10} {'TOTAL':<10} {'DATA':<20}")
    print("-"*100)

    cursor = connect.execute('''
        SELECT v.id, c.nome, p.nome, v.quantidade, v.preco_unitario, v.total, v.data_venda
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN produtos p ON v.produto_id = p.id
        WHERE v.usuario_email = ?
        ORDER BY v.data_venda DESC
    ''', (user_email,))

    vendas = cursor.fetchall()

    if not vendas:
        print("Nenhuma venda registrada!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    for venda in vendas:
        data_formatada = venda[6][:10] if venda[6] else "N/A"
        print(f"{venda[0]:<5} {venda[1]:<25} {venda[2]:<25} {venda[3]:<5} R$ {venda[4]:<8.2f} R$ {venda[5]:<8.2f} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def gerar_relatorio_vendas_excel(connect, user_email):
    """Gera relatório de vendas em Excel"""
    print("\n" + "-"*50)
    print("GERAR RELATÓRIO DE VENDAS - EXCEL")
    print("-"*50)

    try:
        # Garantir que a pasta relatorios existe
        garantir_pastas_existem()

        # Buscar todas as vendas do usuário
        cursor = connect.execute('''
            SELECT v.id, c.nome as cliente, p.nome as produto, v.quantidade,
                   v.preco_unitario, v.total, v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            WHERE v.usuario_email = ?
            ORDER BY v.data_venda DESC
        ''', (user_email,))

        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda encontrada para gerar relatório!")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        # Criar DataFrame
        df = pd.DataFrame(vendas, columns=[
                          'ID', 'Cliente', 'Produto', 'Quantidade', 'Preço Unitário', 'Total', 'Data Venda'])

        # Formatar preços
        df['Preço Unitário'] = df['Preço Unitário'].apply(
            lambda x: f"R$ {x:.2f}")
        df['Total'] = df['Total'].apply(lambda x: f"R$ {x:.2f}")

        # Formatar datas
        df['Data Venda'] = df['Data Venda'].apply(
            lambda x: x[:10] if x else "N/A")

        # Nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorios/relatorio_vendas_{user_email.replace('@', '_').replace('.', '_')}_{timestamp}.xlsx"

        # Criar writer do Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Planilha principal - Vendas
            df.to_excel(writer, sheet_name='Vendas', index=False)

            # Planilha de resumo
            resumo_data = {
                'Métrica': ['Total de Vendas', 'Valor Total', 'Ticket Médio', 'Data Primeira Venda', 'Data Última Venda'],
                'Valor': [
                    len(vendas),
                    f"R$ {sum(venda[5] for venda in vendas):.2f}",
                    f"R$ {sum(venda[5] for venda in vendas) / len(vendas):.2f}",
                    min(venda[6][:10]
                        for venda in vendas if venda[6]) if vendas else "N/A",
                    max(venda[6][:10]
                        for venda in vendas if venda[6]) if vendas else "N/A"
                ]
            }

            df_resumo = pd.DataFrame(resumo_data)
            df_resumo.to_excel(writer, sheet_name='Resumo', index=False)

            # Planilha de produtos mais vendidos
            produtos_vendidos = {}
            for venda in vendas:
                produto = venda[2]
                quantidade = venda[3]
                total = venda[5]

                if produto in produtos_vendidos:
                    produtos_vendidos[produto]['quantidade'] += quantidade
                    produtos_vendidos[produto]['total'] += total
                else:
                    produtos_vendidos[produto] = {
                        'quantidade': quantidade, 'total': total}

            if produtos_vendidos:
                produtos_data = []
                for produto, dados in sorted(produtos_vendidos.items(), key=lambda x: x[1]['quantidade'], reverse=True):
                    produtos_data.append(
                        [produto, dados['quantidade'], f"R$ {dados['total']:.2f}"])

                df_produtos = pd.DataFrame(produtos_data, columns=[
                                           'Produto', 'Quantidade Vendida', 'Valor Total'])
                df_produtos.to_excel(
                    writer, sheet_name='Produtos Mais Vendidos', index=False)

            # Formatação das planilhas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]

                # Ajustar largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"\n✅ Relatório gerado com sucesso!")
        print(f"📁 Arquivo: {filename}")
        print(f"📊 Total de vendas: {len(vendas)}")
        print(f"💰 Valor total: R$ {sum(venda[5] for venda in vendas):.2f}")
        print(
            f"📈 Ticket médio: R$ {sum(venda[5] for venda in vendas) / len(vendas):.2f}")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except ImportError:
        print("❌ Erro: Biblioteca 'openpyxl' não encontrada!")
        print("💡 Para instalar: pip install openpyxl")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def buscar_venda(connect, user_email):
    """Busca vendas por cliente ou data"""
    print("\n" + "-"*50)
    print("BUSCAR VENDA")
    print("-"*50)
    print("1. Buscar por cliente")
    print("2. Buscar por data")

    try:
        opcao = int(input("Digite a opção: "))
    except ValueError:
        print("Opção inválida!")
        return

    if opcao == 1:
        termo = input("Digite o nome do cliente: ").strip()
        if not termo:
            print("Termo de busca é obrigatório!")
            return

        cursor = connect.execute('''
            SELECT v.id, c.nome, p.nome, v.quantidade, v.preco_unitario, v.total, v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            WHERE c.nome LIKE ? AND v.usuario_email = ?
            ORDER BY v.data_venda DESC
        ''', (f'%{termo}%', user_email))

    elif opcao == 2:
        data = input("Digite a data (YYYY-MM-DD): ").strip()
        if not data:
            print("Data é obrigatória!")
            return

        cursor = connect.execute('''
            SELECT v.id, c.nome, p.nome, v.quantidade, v.preco_unitario, v.total, v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            WHERE DATE(v.data_venda) = ? AND v.usuario_email = ?
            ORDER BY v.data_venda DESC
        ''', (data, user_email))

    else:
        print("Opção inválida!")
        return

    vendas = cursor.fetchall()

    if not vendas:
        print("Nenhuma venda encontrada!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    print("\n" + "-"*100)
    print("RESULTADOS DA BUSCA")
    print("-"*100)
    print(f"{'ID':<5} {'CLIENTE':<25} {'PRODUTO':<25} {'QTD':<5} {'PREÇO UN.':<10} {'TOTAL':<10} {'DATA':<20}")
    print("-"*100)

    for venda in vendas:
        data_formatada = venda[6][:10] if venda[6] else "N/A"
        print(f"{venda[0]:<5} {venda[1]:<25} {venda[2]:<25} {venda[3]:<5} R$ {venda[4]:<8.2f} R$ {venda[5]:<8.2f} {data_formatada:<20}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def relatorio_vendas(connect, user_email):
    """Gera relatório de vendas do usuário"""
    print("\n" + "-"*50)
    print(f"RELATÓRIO DE VENDAS - {user_email}")
    print("-"*50)

    # Total de vendas do usuário
    cursor = connect.execute(
        'SELECT COUNT(*), SUM(total) FROM vendas WHERE usuario_email = ?', (user_email,))
    resultado = cursor.fetchone()
    total_vendas = resultado[0] or 0
    valor_total = resultado[1] or 0

    print(f"Total de vendas: {total_vendas}")
    print(f"Valor total: R$ {valor_total:.2f}")

    # Top 5 produtos mais vendidos do usuário
    print("\nTop 5 produtos mais vendidos:")
    cursor = connect.execute('''
        SELECT p.nome, SUM(v.quantidade) as total_vendido, SUM(v.total) as valor_total
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        WHERE v.usuario_email = ?
        GROUP BY p.id, p.nome
        ORDER BY total_vendido DESC
        LIMIT 5
    ''', (user_email,))

    produtos = cursor.fetchall()
    if produtos:
        print(f"{'PRODUTO':<25} {'QTD VENDIDA':<15} {'VALOR TOTAL':<15}")
        print("-"*55)
        for produto in produtos:
            print(f"{produto[0]:<25} {produto[1]:<15} R$ {produto[2]:<12.2f}")

    # Top 5 clientes do usuário
    print("\nTop 5 clientes:")
    cursor = connect.execute('''
        SELECT c.nome, COUNT(v.id) as total_compras, SUM(v.total) as valor_total
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.usuario_email = ?
        GROUP BY c.id, c.nome
        ORDER BY valor_total DESC
        LIMIT 5
    ''', (user_email,))

    clientes = cursor.fetchall()
    if clientes:
        print(f"{'CLIENTE':<25} {'COMPRAS':<10} {'VALOR TOTAL':<15}")
        print("-"*50)
        for cliente in clientes:
            print(f"{cliente[0]:<25} {cliente[1]:<10} R$ {cliente[2]:<12.2f}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def menu_analise_vendas(connect, user_email):
    """Menu de análise de vendas"""
    while True:
        print("\n" + "="*50)
        print(f"ANÁLISE DE VENDAS - {user_email}")
        print("="*50)
        print("1. Relatório geral")
        print("2. Vendas por período")
        print("3. Produtos em baixo estoque")
        print("4. Gerar relatório Excel completo")
        print("5. Voltar ao menu principal")
        print("-"*50)

        try:
            opcao = int(input("Digite a opção desejada: "))

            if opcao == 1:
                relatorio_vendas(connect, user_email)
            elif opcao == 2:
                vendas_por_periodo(connect, user_email)
            elif opcao == 3:
                produtos_baixo_estoque(connect, user_email)
            elif opcao == 4:
                gerar_relatorio_analise_vendas_excel(connect, user_email)
            elif opcao == 5:
                break
            else:
                print("Opção inválida!")

        except ValueError:
            print("Erro: Digite apenas números!")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def vendas_por_periodo(connect, user_email):
    """Analisa vendas por período"""
    print("\n" + "-"*50)
    print("VENDAS POR PERÍODO")
    print("-"*50)

    try:
        data_inicio = input("Data de início (YYYY-MM-DD): ").strip()
        data_fim = input("Data de fim (YYYY-MM-DD): ").strip()

        if not data_inicio or not data_fim:
            print("Datas são obrigatórias!")
            return

        cursor = connect.execute('''
            SELECT COUNT(*), SUM(total)
            FROM vendas
            WHERE DATE(data_venda) BETWEEN ? AND ? AND usuario_email = ?
        ''', (data_inicio, data_fim, user_email))

        resultado = cursor.fetchone()
        total_vendas = resultado[0] or 0
        valor_total = resultado[1] or 0

        print(f"\nPeríodo: {data_inicio} a {data_fim}")
        print(f"Total de vendas: {total_vendas}")
        print(f"Valor total: R$ {valor_total:.2f}")

        # Vendas por dia no período
        cursor = connect.execute('''
            SELECT DATE(data_venda) as data, COUNT(*), SUM(total)
            FROM vendas
            WHERE DATE(data_venda) BETWEEN ? AND ? AND usuario_email = ?
            GROUP BY DATE(data_venda)
            ORDER BY data
        ''', (data_inicio, data_fim, user_email))

        vendas_diarias = cursor.fetchall()
        if vendas_diarias:
            print(f"\nVendas por dia:")
            print(f"{'DATA':<15} {'VENDAS':<10} {'VALOR':<15}")
            print("-"*40)
            for venda in vendas_diarias:
                print(f"{venda[0]:<15} {venda[1]:<10} R$ {venda[2]:<12.2f}")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except Exception as e:
        print(f"Erro ao analisar vendas: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def produtos_baixo_estoque(connect, user_email):
    """Lista produtos com baixo estoque"""
    print("\n" + "-"*50)
    print("PRODUTOS EM BAIXO ESTOQUE")
    print("-"*50)

    try:
        limite = int(
            input("Digite o limite de estoque (padrão: 10): ") or "10")
    except ValueError:
        limite = 10

    cursor = connect.execute('''
        SELECT id, nome, preco, quantidade, categoria
        FROM produtos
        WHERE quantidade <= ? AND usuario_email = ?
        ORDER BY quantidade
    ''', (limite, user_email))

    produtos = cursor.fetchall()

    if not produtos:
        print(f"Nenhum produto com estoque menor ou igual a {limite}!")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
        return

    print(f"\nProdutos com estoque <= {limite}:")
    print(f"{'ID':<5} {'NOME':<30} {'PREÇO':<10} {'ESTOQUE':<10} {'CATEGORIA':<15}")
    print("-"*70)

    for produto in produtos:
        print(
            f"{produto[0]:<5} {produto[1]:<30} R$ {produto[2]:<8.2f} {produto[3]:<10} {produto[4]:<15}")

    input("\nPressione Enter para voltar ao menu...")
    limpar_terminal()


def gerar_relatorio_analise_vendas_excel(connect, user_email):
    """Gera relatório completo de análise de vendas em Excel"""
    print("\n" + "-"*50)
    print("GERAR RELATÓRIO DE ANÁLISE DE VENDAS - EXCEL")
    print("-"*50)

    try:
        # Garantir que a pasta relatorios existe
        garantir_pastas_existem()

        # Buscar dados para análise
        cursor = connect.execute('''
            SELECT v.id, c.nome as cliente, p.nome as produto, v.quantidade,
                   v.preco_unitario, v.total, v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            WHERE v.usuario_email = ?
            ORDER BY v.data_venda DESC
        ''', (user_email,))

        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda encontrada para gerar relatório!")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        # Nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorios/relatorio_analise_vendas_{user_email.replace('@', '_').replace('.', '_')}_{timestamp}.xlsx"

        # Criar writer do Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:

            # 1. Planilha de Vendas Detalhadas
            df_vendas = pd.DataFrame(vendas, columns=[
                                     'ID', 'Cliente', 'Produto', 'Quantidade', 'Preço Unitário', 'Total', 'Data Venda'])
            df_vendas['Preço Unitário'] = df_vendas['Preço Unitário'].apply(
                lambda x: f"R$ {x:.2f}")
            df_vendas['Total'] = df_vendas['Total'].apply(
                lambda x: f"R$ {x:.2f}")
            df_vendas['Data Venda'] = df_vendas['Data Venda'].apply(
                lambda x: x[:10] if x else "N/A")
            df_vendas.to_excel(
                writer, sheet_name='Vendas Detalhadas', index=False)

            # 2. Planilha de Resumo Geral
            total_vendas = len(vendas)
            valor_total = sum(venda[5] for venda in vendas)
            ticket_medio = valor_total / total_vendas if total_vendas > 0 else 0

            resumo_data = {
                'Métrica': [
                    'Total de Vendas',
                    'Valor Total',
                    'Ticket Médio',
                    'Data Primeira Venda',
                    'Data Última Venda',
                    'Total de Clientes Únicos',
                    'Total de Produtos Vendidos'
                ],
                'Valor': [
                    total_vendas,
                    f"R$ {valor_total:.2f}",
                    f"R$ {ticket_medio:.2f}",
                    min(venda[6][:10]
                        for venda in vendas if venda[6]) if vendas else "N/A",
                    max(venda[6][:10]
                        for venda in vendas if venda[6]) if vendas else "N/A",
                    len(set(venda[1] for venda in vendas)),
                    len(set(venda[2] for venda in vendas))
                ]
            }

            df_resumo = pd.DataFrame(resumo_data)
            df_resumo.to_excel(writer, sheet_name='Resumo Geral', index=False)

            # 3. Planilha de Produtos Mais Vendidos
            produtos_vendidos = {}
            for venda in vendas:
                produto = venda[2]
                quantidade = venda[3]
                total = venda[5]

                if produto in produtos_vendidos:
                    produtos_vendidos[produto]['quantidade'] += quantidade
                    produtos_vendidos[produto]['total'] += total
                    produtos_vendidos[produto]['vendas'] += 1
                else:
                    produtos_vendidos[produto] = {
                        'quantidade': quantidade, 'total': total, 'vendas': 1}

            if produtos_vendidos:
                produtos_data = []
                for produto, dados in sorted(produtos_vendidos.items(), key=lambda x: x[1]['quantidade'], reverse=True):
                    produtos_data.append([
                        produto,
                        dados['quantidade'],
                        dados['vendas'],
                        f"R$ {dados['total']:.2f}",
                        f"R$ {dados['total']/dados['quantidade']:.2f}"
                    ])

                df_produtos = pd.DataFrame(produtos_data, columns=[
                                           'Produto', 'Quantidade Vendida', 'Número de Vendas', 'Valor Total', 'Preço Médio'])
                df_produtos.to_excel(
                    writer, sheet_name='Produtos Mais Vendidos', index=False)

            # 4. Planilha de Clientes Mais Valiosos
            clientes_vendidos = {}
            for venda in vendas:
                cliente = venda[1]
                quantidade = venda[3]
                total = venda[5]

                if cliente in clientes_vendidos:
                    clientes_vendidos[cliente]['quantidade'] += quantidade
                    clientes_vendidos[cliente]['total'] += total
                    clientes_vendidos[cliente]['compras'] += 1
                else:
                    clientes_vendidos[cliente] = {
                        'quantidade': quantidade, 'total': total, 'compras': 1}

            if clientes_vendidos:
                clientes_data = []
                for cliente, dados in sorted(clientes_vendidos.items(), key=lambda x: x[1]['total'], reverse=True):
                    clientes_data.append([
                        cliente,
                        dados['compras'],
                        dados['quantidade'],
                        f"R$ {dados['total']:.2f}",
                        f"R$ {dados['total']/dados['compras']:.2f}"
                    ])

                df_clientes = pd.DataFrame(clientes_data, columns=[
                                           'Cliente', 'Número de Compras', 'Quantidade Total', 'Valor Total', 'Ticket Médio'])
                df_clientes.to_excel(
                    writer, sheet_name='Clientes Mais Valiosos', index=False)

            # 5. Planilha de Vendas por Período (últimos 12 meses)
            vendas_por_mes = {}
            for venda in vendas:
                if venda[6]:
                    mes_ano = venda[6][:7]  # YYYY-MM
                    total = venda[5]

                    if mes_ano in vendas_por_mes:
                        vendas_por_mes[mes_ano]['total'] += total
                        vendas_por_mes[mes_ano]['vendas'] += 1
                    else:
                        vendas_por_mes[mes_ano] = {'total': total, 'vendas': 1}

            if vendas_por_mes:
                periodos_data = []
                for mes_ano, dados in sorted(vendas_por_mes.items()):
                    periodos_data.append([
                        mes_ano,
                        dados['vendas'],
                        f"R$ {dados['total']:.2f}",
                        f"R$ {dados['total']/dados['vendas']:.2f}"
                    ])

                df_periodos = pd.DataFrame(periodos_data, columns=[
                                           'Mês/Ano', 'Número de Vendas', 'Valor Total', 'Ticket Médio'])
                df_periodos.to_excel(
                    writer, sheet_name='Vendas por Período', index=False)

            # Formatação das planilhas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]

                # Ajustar largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"\n✅ Relatório de análise gerado com sucesso!")
        print(f"📁 Arquivo: {filename}")
        print(f"📊 Total de vendas analisadas: {len(vendas)}")
        print(f"💰 Valor total: R$ {valor_total:.2f}")
        print(f"👥 Clientes únicos: {len(set(venda[1] for venda in vendas))}")
        print(f"📦 Produtos vendidos: {len(set(venda[2] for venda in vendas))}")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except ImportError:
        print("❌ Erro: Biblioteca 'openpyxl' não encontrada!")
        print("💡 Para instalar: pip install openpyxl")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def gerar_planilha_base_produtos(connect, user_email):
    """Gera uma planilha base para importação de produtos"""
    try:
        print("\n" + "="*60)
        print("GERAR PLANILHA BASE PARA IMPORTAÇÃO DE PRODUTOS")
        print("="*60)

        # Garantir que a pasta inventario existe
        garantir_pastas_existem()

        # Criar DataFrame com estrutura base
        dados_base = [
            ['', 'Nome do Produto', 0.00, 0, 'Categoria'],
            ['', 'Exemplo: Notebook', 2500.00, 10, 'Eletrônicos'],
            ['', 'Exemplo: Mouse', 50.00, 25, 'Acessórios'],
        ]

        df = pd.DataFrame(dados_base, columns=[
                          'ID', 'Nome', 'Preço', 'Quantidade', 'Categoria'])

        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inventario/download_base/planilha_base_produtos_{user_email.replace('@', '_').replace('.', '_')}_{timestamp}.xlsx"

        # Salvar arquivo Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Produtos', index=False)

            # Formatação da planilha
            worksheet = writer.sheets['Produtos']

            # Ajustar largura das colunas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"\n✅ Planilha base gerada com sucesso!")
        print(f"📁 Arquivo: {filename}")
        print("\n📋 INSTRUÇÕES:")
        print("1. Abra o arquivo Excel gerado")
        print("2. Preencha os dados dos produtos (ID deve ficar vazio)")
        print("3. Salve o arquivo")
        print("4. Use a opção 'Importar produtos de arquivo Excel' para carregar os dados")
        print("\n⚠️  IMPORTANTE:")
        print("- O campo 'ID' deve ficar vazio (será preenchido automaticamente)")
        print("- O campo 'Nome' é obrigatório")
        print("- O campo 'Preço' deve ser um número decimal (ex: 25.50)")
        print("- O campo 'Quantidade' deve ser um número inteiro")
        print("- O campo 'Categoria' é opcional")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except ImportError:
        print("❌ Erro: Biblioteca 'openpyxl' não encontrada!")
        print("💡 Para instalar: pip install openpyxl")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
    except Exception as e:
        print(f"❌ Erro ao gerar planilha base: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def importar_produtos_upload_base(connect, user_email):
    """Importa produtos da pasta upload_base com confirmação e limpeza automática"""
    try:
        print("\n" + "="*60)
        print("IMPORTAR PRODUTOS DA PASTA UPLOAD_BASE")
        print("="*60)

        # Garantir que a pasta upload_base existe
        garantir_pastas_existem()

        upload_path = "inventario/upload_base"

        # Verificar se existem arquivos Excel na pasta
        arquivos_excel = []
        for arquivo in os.listdir(upload_path):
            if arquivo.lower().endswith(('.xlsx', '.xls')) and not arquivo.startswith('~$'):
                arquivos_excel.append(arquivo)

        if not arquivos_excel:
            print("❌ Nenhum arquivo Excel encontrado na pasta upload_base!")
            print(f"📁 Pasta: {upload_path}")
            print("\n💡 Para importar produtos:")
            print("1. Coloque o arquivo Excel na pasta 'inventario/upload_base'")
            print("2. Execute esta opção novamente")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        print(f"📁 Arquivos encontrados na pasta upload_base:")
        for i, arquivo in enumerate(arquivos_excel, 1):
            print(f"  {i}. {arquivo}")

        # Selecionar arquivo
        try:
            escolha = int(
                input(f"\nEscolha o arquivo (1-{len(arquivos_excel)}) ou 0 para cancelar: "))
            if escolha == 0:
                print("Importação cancelada.")
                input("\nPressione Enter para voltar ao menu...")
                limpar_terminal()
                return
            if escolha < 1 or escolha > len(arquivos_excel):
                print("❌ Opção inválida!")
                input("\nPressione Enter para voltar ao menu...")
                limpar_terminal()
                return
        except ValueError:
            print("❌ Digite apenas números!")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        arquivo_selecionado = arquivos_excel[escolha - 1]
        caminho_completo = os.path.join(upload_path, arquivo_selecionado)

        print(f"\n📋 Arquivo selecionado: {arquivo_selecionado}")

        # Confirmar importação
        confirmacao = input(
            "\n⚠️  ATENÇÃO: Esta operação irá importar produtos e EXCLUIR o arquivo após a importação!\n\nConfirma a importação? (s/n): ").lower().strip()

        if confirmacao not in ['s', 'sim', 'y', 'yes']:
            print("Importação cancelada pelo usuário.")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        # Ler arquivo Excel
        df = pd.read_excel(caminho_completo, sheet_name=0)

        # Verificar colunas necessárias
        colunas_necessarias = ['Nome', 'Preço', 'Quantidade']
        colunas_faltando = [
            col for col in colunas_necessarias if col not in df.columns]

        if colunas_faltando:
            print(
                f"❌ Colunas obrigatórias não encontradas: {', '.join(colunas_faltando)}")
            print(f"📋 Colunas necessárias: {', '.join(colunas_necessarias)}")
            input("\nPressione Enter para voltar ao menu...")
            limpar_terminal()
            return

        # Processar importação
        produtos_importados = 0
        produtos_erro = 0
        erros = []

        print(f"\n🔄 Processando {len(df)} produtos...")

        for index, row in df.iterrows():
            try:
                # Extrair dados
                nome = str(row['Nome']).strip()
                preco = float(row['Preço'])
                quantidade = int(row['Quantidade'])
                categoria = str(row.get('Categoria', '')).strip()

                # Validações
                if not nome:
                    erros.append(f"Linha {index + 2}: Nome é obrigatório")
                    produtos_erro += 1
                    continue

                if preco < 0:
                    erros.append(
                        f"Linha {index + 2}: Preço não pode ser negativo")
                    produtos_erro += 1
                    continue

                if quantidade < 0:
                    erros.append(
                        f"Linha {index + 2}: Quantidade não pode ser negativa")
                    produtos_erro += 1
                    continue

                # Inserir produto no banco
                connect.execute('''
                    INSERT INTO produtos (nome, preco, quantidade, categoria, usuario_email)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nome, preco, quantidade, categoria, user_email))

                produtos_importados += 1

            except Exception as e:
                erros.append(f"Linha {index + 2}: {str(e)}")
                produtos_erro += 1

        # Commit das alterações
        connect.commit()

        # Excluir arquivo após importação
        try:
            os.remove(caminho_completo)
            print(f"🗑️  Arquivo '{arquivo_selecionado}' excluído com sucesso!")
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível excluir o arquivo: {e}")

        # Relatório final
        print(f"\n✅ Importação concluída!")
        print(f"📦 Produtos importados com sucesso: {produtos_importados}")

        if produtos_erro > 0:
            print(f"❌ Produtos com erro: {produtos_erro}")
            print("\n📋 ERROS ENCONTRADOS:")
            for erro in erros[:10]:  # Mostrar apenas os primeiros 10 erros
                print(f"  - {erro}")
            if len(erros) > 10:
                print(f"  ... e mais {len(erros) - 10} erros")

        if produtos_importados > 0:
            print(
                f"\n🎉 {produtos_importados} produtos foram adicionados ao seu estoque!")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

    except ImportError:
        print("❌ Erro: Biblioteca 'openpyxl' não encontrada!")
        print("💡 Para instalar: pip install openpyxl")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()
    except Exception as e:
        print(f"❌ Erro ao importar produtos: {e}")
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()


def user_panel(connect, user_name, user_email):
    """Painel principal do usuário"""
    print(f"\n{'='*60}")
    print(f"BEM-VINDO AO SEU PAINEL DE GERENCIAMENTO")
    print(f"Usuário: {user_name}")
    print(f"Email: {user_email}")
    print(f"Banco de dados: database.db (centralizado)")
    print(f"{'='*60}")

    option = 0
    while option != 5:
        try:
            print("\n" + "="*50)
            print("SISTEMA DE GERENCIAMENTO")
            print("="*50)
            print("1. Produtos")
            print("2. Vendas")
            print("3. Clientes")
            print("4. Análise de vendas")
            print("5. Sair")
            print("-"*50)

            option = int(input("Digite a opção desejada: "))

            if option == 1:
                menu_produtos(connect, user_email)
            elif option == 2:
                menu_vendas(connect, user_email)
            elif option == 3:
                menu_clientes(connect, user_email)
            elif option == 4:
                menu_analise_vendas(connect, user_email)
            elif option == 5:
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Digite 1, 2, 3, 4 ou 5.")

        except ValueError:
            print("Erro: Digite apenas números para as opções!")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input('Digite enter para continuar...')
