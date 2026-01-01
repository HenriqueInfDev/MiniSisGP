import sqlite3
import os
import atexit

# Global variable to hold the database connection
_connection = None

def get_db_path():
    # Caminho específico para Windows, conforme solicitado pelo usuário.
    return r'C:\MiniSis\Ordem de Produção\Dados\DADOS.DB'

DB_PATH = get_db_path()

def _create_tables(conn):
    cursor = conn.cursor()
    # Tabela de Unidades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UNIDADE (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT NOT NULL UNIQUE,
        SIGLA TEXT NOT NULL UNIQUE
    )
    ''')
    # Tabela de Itens (Produtos e Insumos)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ITEM (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DESCRICAO TEXT NOT NULL UNIQUE,
        TIPO_ITEM TEXT NOT NULL CHECK(TIPO_ITEM IN ('Insumo', 'Produto', 'Ambos')),
        ID_UNIDADE INTEGER NOT NULL,
        SALDO_ESTOQUE REAL NOT NULL DEFAULT 0,
        CUSTO_MEDIO REAL NOT NULL DEFAULT 0,
        FOREIGN KEY (ID_UNIDADE) REFERENCES UNIDADE (ID)
    )
    ''')
    # Tabela de Composição (Ficha Técnica)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS COMPOSICAO (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PRODUTO INTEGER NOT NULL,
        ID_INSUMO INTEGER NOT NULL,
        QUANTIDADE REAL NOT NULL,
        FOREIGN KEY (ID_PRODUTO) REFERENCES ITEM (ID),
        FOREIGN KEY (ID_INSUMO) REFERENCES ITEM (ID),
        UNIQUE (ID_PRODUTO, ID_INSUMO)
    )
    ''')
    # Tabela de Ordem de Produção (Mestre)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ORDEMPRODUCAO (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATA_CRIACAO TEXT NOT NULL,
        DATA_PREVISTA TEXT,
        STATUS TEXT NOT NULL CHECK(STATUS IN ('Planejada', 'Em Andamento', 'Concluída', 'Cancelada'))
    )
    ''')
    # Tabela de Itens da Ordem de Produção (Detalhe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ORDEMPRODUCAO_ITENS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_ORDEM_PRODUCAO INTEGER NOT NULL,
        ID_PRODUTO INTEGER NOT NULL,
        QUANTIDADE_PRODUZIR REAL NOT NULL,
        FOREIGN KEY (ID_ORDEM_PRODUCAO) REFERENCES ORDEMPRODUCAO (ID),
        FOREIGN KEY (ID_PRODUTO) REFERENCES ITEM (ID),
        UNIQUE (ID_ORDEM_PRODUCAO, ID_PRODUTO)
    )
    ''')
    # Tabela de Movimentação de Estoque
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MOVIMENTO (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_ITEM INTEGER NOT NULL,
        TIPO_MOVIMENTO TEXT NOT NULL,
        QUANTIDADE REAL NOT NULL,
        VALOR_UNITARIO REAL,
        ID_ORDEM_PRODUCAO INTEGER,
        DATA_MOVIMENTO TEXT NOT NULL,
        FOREIGN KEY (ID_ITEM) REFERENCES ITEM (ID),
        FOREIGN KEY (ID_ORDEM_PRODUCAO) REFERENCES ORDEMPRODUCAO (ID)
    )
    ''')
    # Tabela de Nota de Entrada (Mestre)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ENTRADANOTA (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATA_ENTRADA TEXT NOT NULL,
        FORNECEDOR TEXT,
        NUMERO_NOTA TEXT,
        VALOR_TOTAL REAL,
        STATUS TEXT NOT NULL CHECK(STATUS IN ('Em Aberto', 'Finalizada'))
    )
    ''')
    # Tabela de Itens da Nota de Entrada (Detalhe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ENTRADANOTA_ITENS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_ENTRADA INTEGER NOT NULL,
        ID_INSUMO INTEGER NOT NULL,
        QUANTIDADE REAL NOT NULL,
        VALOR_UNITARIO REAL NOT NULL,
        FOREIGN KEY (ID_ENTRADA) REFERENCES ENTRADANOTA (ID),
        FOREIGN KEY (ID_INSUMO) REFERENCES ITEM (ID),
        UNIQUE (ID_ENTRADA, ID_INSUMO)
    )
    ''')

    # Inserção de unidades padrão (com nomes de coluna em maiúsculas)
    unidades = [('Grama', 'g'), ('Quilograma', 'kg'), ('Mililitro', 'ml'), ('Litro', 'L'), ('Unidade', 'un')]
    for nome, sigla in unidades:
        cursor.execute("SELECT ID FROM UNIDADE WHERE NOME = ?", (nome,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO UNIDADE (NOME, SIGLA) VALUES (?, ?)", (nome, sigla))

    conn.commit()

def initialize_database():
    global _connection
    if _connection is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        _connection = sqlite3.connect(DB_PATH)
        _connection.row_factory = sqlite3.Row
        _create_tables(_connection)
        atexit.register(close_connection)
        print(f"Banco de dados inicializado em: {DB_PATH}")

def get_db_connection():
    if _connection is None:
        raise Exception("A conexão com o banco de dados não foi inicializada.")
    return _connection

def close_connection():
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        print("Conexão com o banco de dados fechada.")

if __name__ == '__main__':
    initialize_database()
