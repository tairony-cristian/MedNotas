from app.models.anotacao import Anotacao
from app.database import DatabaseConnection

class AnotacaoController:
    def __init__(self):
        self.db = DatabaseConnection()

    def adicionar_anotacao(self, data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao):
        anotacao = Anotacao(data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao)
        self.db.cursor.execute('''
            INSERT INTO app_anotacoes (data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (anotacao.data, anotacao.procedimento, anotacao.quant_procedimento, anotacao.quant_ampola, anotacao.custo, anotacao.local, anotacao.medico, anotacao.observacao))
        self.db.connection.commit()

    def listar_anotacoes(self):
        self.db.cursor.execute('SELECT * FROM app_anotacoes')
        return self.db.cursor.fetchall()

    def buscar_anotacao(self, termo_pesquisa):
        self.db.cursor.execute('''
            SELECT * FROM app_anotacoes WHERE data LIKE ? OR procedimento LIKE ? OR local LIKE ? OR medico LIKE ? OR observacao LIKE ?
        ''', (f'%{termo_pesquisa}%', f'%{termo_pesquisa}%', f'%{termo_pesquisa}%', f'%{termo_pesquisa}%', f'%{termo_pesquisa}%'))
        return self.db.cursor.fetchall()

    def atualizar_anotacao(self, id, data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao):
        self.db.cursor.execute('''
            UPDATE app_anotacoes SET data=?, procedimento=?, quant_procedimento=?, quant_ampola=?, custo=?, local=?, medico=?, observacao=? WHERE id=?
        ''', (data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao, id))
        self.db.connection.commit()

    def deletar_anotacao(self, id):
        self.db.cursor.execute('DELETE FROM app_anotacoes WHERE id=?', (id,))
        self.db.connection.commit()

    def close_connection(self):
        self.db.close()
