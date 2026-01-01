# app/services/production_service.py
from app.production.production_repository import ProductionRepository

class ProductionService:
    def __init__(self):
        self.production_repository = ProductionRepository()

    def create_op(self, due_date, items_to_produce):
        if not all([due_date, items_to_produce]):
            return {"success": False, "message": "Todos os campos são obrigatórios."}

        try:
            op_id = self.production_repository.create_op(due_date, items_to_produce)
            if op_id:
                return {"success": True, "data": op_id, "message": "Ordem de Produção criada com sucesso."}
            else:
                return {"success": False, "message": "Erro ao criar Ordem de Produção."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar Ordem de Produção: {e}"}

    def update_op(self, op_id, due_date, items_to_produce):
        if not all([op_id, due_date, items_to_produce]):
            return {"success": False, "message": "Todos os campos são obrigatórios."}

        try:
            if self.production_repository.update_op(op_id, due_date, items_to_produce):
                return {"success": True, "message": "Ordem de Produção atualizada com sucesso."}
            else:
                return {"success": False, "message": "Erro ao atualizar Ordem de Produção."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar Ordem de Produção: {e}"}

    def get_op_details(self, op_id):
        try:
            details = self.production_repository.get_op_details(op_id)
            if details:
                return {"success": True, "data": details}
            else:
                return {"success": False, "message": "Ordem de Produção não encontrada."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar detalhes da Ordem de Produção: {e}"}

    def list_ops(self, search_term="", search_field="id"):
        try:
            orders = self.production_repository.list_ops(search_term, search_field)
            return {"success": True, "data": orders}
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar Ordens de Produção: {e}"}
