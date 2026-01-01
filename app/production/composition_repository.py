# app/production/composition_repository.py
import sqlite3
from app.database import get_db_manager

class CompositionRepository:
    def __init__(self):
        self.db_manager = get_db_manager()

    def get_bom(self, product_id):
        conn = self.db_manager.get_connection()
        bom = conn.execute('''
            SELECT
                C.ID,
                I.ID as ID_INSUMO,
                I.DESCRICAO,
                C.QUANTIDADE,
                U.SIGLA,
                I.CUSTO_MEDIO
            FROM TCOMPOSICAO C
            JOIN TITEM I ON C.ID_INSUMO = I.ID
            JOIN TUNIDADE U ON I.ID_UNIDADE = U.ID
            WHERE C.ID_PRODUTO = ?
        ''', (product_id,)).fetchall()
        return bom

    def update_composition(self, product_id, new_composition):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute("DELETE FROM TCOMPOSICAO WHERE ID_PRODUTO = ?", (product_id,))
                if new_composition:
                    cursor.executemany(
                        "INSERT INTO TCOMPOSICAO (ID_PRODUTO, ID_INSUMO, QUANTIDADE) VALUES (?, ?, ?)",
                        [(product_id, item['id_insumo'], item['quantidade']) for item in new_composition]
                    )
            return True
        except sqlite3.Error:
            return False

    def validate_bom_item(self, product_id, material_id):
        if material_id == product_id:
            return False, "Um produto não pode ser componente de si mesmo."

        conn = self.db_manager.get_connection()
        material = conn.execute('SELECT DESCRICAO, TIPO_ITEM FROM TITEM WHERE ID = ?', (material_id,)).fetchone()

        if not material or material['TIPO_ITEM'] not in ('Insumo', 'Ambos'):
            return False, f"O item '{material['DESCRICAO'] if material else ''}' é um 'Produto' e não pode ser usado como insumo."

        return True, None
