# app/item/item_operations.py
import sqlite3
from datetime import datetime
from ..database import get_db_connection

def list_units():
    """Lista todas as unidades de medida disponíveis."""
    conn = get_db_connection()
    units = conn.execute('SELECT ID, NOME, SIGLA FROM UNIDADE').fetchall()
    return units

def add_item(description, item_type, unit_id):
    """
    Adiciona um novo item na tabela TITEM.
    Retorna o ID do novo item em caso de sucesso, ou None em caso de falha.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO ITEM (DESCRICAO, TIPO_ITEM, ID_UNIDADE) VALUES (?, ?, ?)',
            (description, item_type, unit_id)
        )
        new_id = cursor.lastrowid
        conn.commit()
        print(f"Item '{description}' adicionado com sucesso com ID {new_id}.")
        return new_id
    except sqlite3.IntegrityError:
        print(f"Erro: Item com a descrição '{description}' já existe.")
        get_db_connection().rollback()
        return None

def manual_input_material(item_id, quantity, total_value):
    """Registra a entrada de um insumo, atualiza saldo e custo médio."""
    conn = get_db_connection()
    cursor = conn.cursor()

    item = cursor.execute('SELECT * FROM ITEM WHERE ID = ?', (item_id,)).fetchone()
    if not item or item['TIPO_ITEM'] not in ('Insumo', 'Ambos'):
        print("Erro: Apenas itens do tipo 'Insumo' ou 'Ambos' podem ter entrada manual.")
        return False

    old_balance = item['SALDO_ESTOQUE']
    old_average_cost = item['CUSTO_MEDIO']

    new_balance = old_balance + quantity
    input_unit_value = total_value / quantity if quantity > 0 else 0

    # Cálculo do novo custo médio
    new_average_cost = ((old_balance * old_average_cost) + (quantity * input_unit_value)) / new_balance if new_balance > 0 else 0

    # Atualizar saldo e custo do item
    cursor.execute(
        'UPDATE ITEM SET SALDO_ESTOQUE = ?, CUSTO_MEDIO = ? WHERE ID = ?',
        (new_balance, new_average_cost, item_id)
    )

    # Registrar movimento
    cursor.execute(
        '''INSERT INTO MOVIMENTO (ID_ITEM, TIPO_MOVIMENTO, QUANTIDADE, VALOR_UNITARIO, DATA_MOVIMENTO)
           VALUES (?, 'Entrada Manual', ?, ?, ?)''',
        (item_id, quantity, input_unit_value, datetime.now().isoformat())
    )

    conn.commit()
    print(f"Entrada de {quantity} un. do item ID {item_id} registrada. Novo saldo: {new_balance}.")
    return True

def list_items():
    """Lista todos os itens com seus saldos e custos."""
    conn = get_db_connection()
    items = conn.execute('''
        SELECT I.ID, I.DESCRICAO, I.TIPO_ITEM, U.SIGLA, I.SALDO_ESTOQUE, I.CUSTO_MEDIO
        FROM ITEM I
        JOIN UNIDADE U ON I.ID_UNIDADE = U.ID
        ORDER BY I.ID
    ''').fetchall()
    return items

def get_item_by_id(item_id):
    """Busca um item específico pelo seu ID."""
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM ITEM WHERE ID = ?', (item_id,)).fetchone()
    return item

def update_item(item_id, description, item_type, unit_id):
    """Atualiza os dados de um item existente."""
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE ITEM SET DESCRICAO = ?, TIPO_ITEM = ?, ID_UNIDADE = ? WHERE ID = ?',
            (description, item_type, unit_id, item_id)
        )
        conn.commit()
        print(f"Item ID {item_id} atualizado com sucesso.")
        return True
    except sqlite3.IntegrityError:
        print(f"Erro: A descrição '{description}' já pode existir em outro item.")
        get_db_connection().rollback()
        return False

def search_items(search_type, search_text):
    """
    Busca itens por um campo específico (ID, Descrição, Unidade, Quantidade).
    """
    conn = get_db_connection()

    base_query = '''
        SELECT I.ID, I.DESCRICAO, I.TIPO_ITEM, U.SIGLA, I.SALDO_ESTOQUE, I.CUSTO_MEDIO
        FROM ITEM I
        JOIN UNIDADE U ON I.ID_UNIDADE = U.ID
    '''

    params = ()
    query = base_query

    if search_type == 'ID':
        if not search_text.isdigit():
            return [] # Retorna vazio se o ID não for um número
        query += " WHERE I.ID = ?"
        params = (int(search_text),)
    elif search_type == 'Unidade':
        query += " WHERE U.SIGLA LIKE ?"
        params = (f'%{search_text}%',)
    elif search_type == 'Quantidade':
        try:
            val = float(search_text)
            query += " WHERE I.SALDO_ESTOQUE = ?"
            params = (val,)
        except ValueError:
            return []
    else: # Por padrão, busca por Descrição
        query += " WHERE I.DESCRICAO LIKE ?"
        params = (f'%{search_text}%',)

    items = conn.execute(query, params).fetchall()
    return items

def delete_item(item_id):
    """
    Exclui um item do banco de dados, se não houver dependências.
    Retorna (True, "Mensagem de sucesso") ou (False, "Mensagem de erro").
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Verificar se o item é um insumo em alguma composição
    composition_check = cursor.execute('SELECT 1 FROM COMPOSICAO WHERE ID_INSUMO = ?', (item_id,)).fetchone()
    if composition_check:
        return False, "Não é possível excluir: O item está sendo usado como insumo na composição de um produto."

    # 2. Verificar se o item (produto) está em alguma ordem de produção
    order_check = cursor.execute('SELECT 1 FROM ORDEMPRODUCAO_ITENS WHERE ID_PRODUTO = ?', (item_id,)).fetchone()
    if order_check:
        return False, "Não é possível excluir: O item (produto) está incluído em uma ou mais Ordens de Produção."

    # 3. Verificar se há movimentação de estoque para este item
    movement_check = cursor.execute('SELECT 1 FROM MOVIMENTO WHERE ID_ITEM = ?', (item_id,)).fetchone()
    if movement_check:
        return False, "Não é possível excluir: O item possui registros de movimentação de estoque."

    # 4. Se o item for um produto, verificar se sua própria composição está vazia
    #    (Itens em sua composição já são cobertos pelo check 1, esta é uma garantia extra)
    own_composition_check = cursor.execute('SELECT 1 FROM COMPOSICAO WHERE ID_PRODUTO = ?', (item_id,)).fetchone()
    if own_composition_check:
        return False, "Não é possível excluir: O produto possui uma composição definida. Remova os insumos primeiro."


    try:
        cursor.execute('DELETE FROM ITEM WHERE ID = ?', (item_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return True, "Item excluído com sucesso."
        else:
            return False, "Erro: Item não encontrado para exclusão."

    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro no banco de dados ao tentar excluir o item: {e}"
