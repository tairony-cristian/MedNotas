from app.models.anotacao import Anotacao
from app.database import DatabaseConnection

class AnotacaoController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def _execute_sql(self, sql, params=None):
        try:
            self.db.cursor.execute(sql, params or {})
            self.db.connection.commit()
        except Exception as e:
            print(f"Erro ao executar SQL: {e}")
            raise

    def adicionar_anotacao(self, anotacao):
        sql = '''
            INSERT INTO app_anotacoes 
            (data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            anotacao.data, anotacao.procedimento, anotacao.quant_procedimento, 
            anotacao.quant_ampola, anotacao.custo, anotacao.local, 
            anotacao.medico, anotacao.observacao
        )
        self._execute_sql(sql, params)

    def atualizar_anotacao(self, id, anotacao):
        sql = '''
            UPDATE app_anotacoes SET 
            data=:data, procedimento=:procedimento, quant_procedimento=:quant_procedimento, 
            quant_ampola=:quant_ampola, custo=:custo, local=:local, medico=:medico, observacao=:observacao
            WHERE id=:id
        '''
        params = anotacao.__dict__
        params['id'] = id
        self._execute_sql(sql, params)


    def deletar_anotacao(self, id):
        sql = 'DELETE FROM app_anotacoes WHERE id=:id'
        self._execute_sql(sql, {'id': id})

    def buscar_anotacao(self, termo_pesquisa):
        sql = '''
            SELECT * FROM app_anotacoes 
            WHERE data LIKE :termo OR procedimento LIKE :termo OR local LIKE :termo 
            OR medico LIKE :termo OR observacao LIKE :termo
        '''
        params = {'termo': f'%{termo_pesquisa}%'}
        return self._fetch_all(sql, params)
    
    def listar_anotacoes(self):
        return self._fetch_all('SELECT * FROM app_anotacoes')

    def _fetch_all(self, sql, params=None):
        self.db.cursor.execute(sql, params or {})
        return self.db.cursor.fetchall()

    def close_connection(self):
        self.db.close()
