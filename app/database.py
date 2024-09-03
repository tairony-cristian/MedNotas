import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="notas.db"):
        """ Inicializa a conexão com o banco de dados e cria as tabelas necessárias. """
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Erro ao conectar com o banco de dados: {e}")
            raise

    def create_tables(self):
        """ Cria a tabela de anotações no banco de dados, se não existir. """
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_anotacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT, 
                    procedimento TEXT, 
                    quant_procedimento INTEGER, 
                    quant_ampola INTEGER,
                    custo REAL,
                    local TEXT,
                    medico TEXT,
                    nota_fiscal TEXT,
                    observacao TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela: {e}")
            raise

    def _execute_sql(self, sql, params=None):
        """ Executa uma instrução SQL com parâmetros fornecidos. """
        try:
            self.cursor.execute(sql, params or ())
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar SQL: {e}")
            raise

    def _fetch_all(self, sql, params=None):
        """ Retorna todos os resultados de uma consulta SQL. """
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            raise

    def close_connection(self):
        """ Fecha a conexão com o banco de dados. """
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")
            raise

    # CRUD Methods
    def adicionar_anotacao(self, anotacao):
        """ Adiciona uma nova anotação ao banco de dados. """
        sql = '''
            INSERT INTO app_anotacoes 
            (data, procedimento, quant_procedimento, quant_ampola, custo, local, medico, nota_fiscal, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            anotacao['data'], anotacao['procedimento'], anotacao['quant_procedimento'], 
            anotacao['quant_ampola'], anotacao['custo'], anotacao['local'], 
            anotacao['medico'], anotacao['nota_fiscal'], anotacao['observacao'] 
        )
        try:
            self._execute_sql(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao adicionar anotação: {e}")
            raise

    def atualizar_anotacao(self, id, anotacao):
        """ Atualiza uma anotação existente com base no ID. """
        sql = '''
            UPDATE app_anotacoes SET 
            data = ?, procedimento = ?, quant_procedimento = ?, 
            quant_ampola = ?, custo = ?, local = ?, medico = ?, nota_fiscal = ?, observacao = ?
            WHERE id = ?
        '''

        params = (
            anotacao['data'], anotacao['procedimento'], anotacao['quant_procedimento'], 
            anotacao['quant_ampola'], anotacao['custo'], anotacao['local'], 
            anotacao['medico'], anotacao['nota_fiscal'], anotacao['observacao'], id
        )
        try:
            self._execute_sql(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao atualizar anotação: {e}")
            raise

    def buscar_anotacao(self, termo_pesquisa):
        """ Busca anotações no banco de dados com base em um termo de pesquisa. """
        sql = '''
            SELECT * FROM app_anotacoes 
            WHERE data LIKE ? OR procedimento LIKE ? OR local LIKE ? 
            OR medico LIKE ? OR nota_fiscal LIKE ? OR observacao LIKE ?
        '''
        params = (f'%{termo_pesquisa}%',) * 6
        try:
            return self._fetch_all(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao buscar anotações: {e}")
            raise
    
    def buscar_anotacao_por_id(self, id_anotacao):
        """ Busca uma anotação específica com base no ID. """
        sql = 'SELECT * FROM app_anotacoes WHERE id = ?'
        try:
            self.cursor.execute(sql, (id_anotacao,))
            result = self.cursor.fetchone()
            if result:
                columns = [column[0] for column in self.cursor.description]
                return dict(zip(columns, result))
            return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar anotação por ID: {e}")
            raise

    def buscar_anotacao_por_periodo_data(self, data_inicio, data_fim):
        """ Busca anotações dentro de um período de datas. """
        try:
            sql = '''
                SELECT * FROM app_anotacoes 
                WHERE data BETWEEN ? AND ?
            '''
            params = (data_inicio, data_fim)
            return self._fetch_all(sql, params)
        except ValueError as e:
            print(f"Erro ao converter datas: {e}")
            raise

    def buscar_anotacao_por_local(self, local):
        """ Busca anotações com base no local. """
        sql = 'SELECT * FROM app_anotacoes WHERE local LIKE ?'
        params = (f'%{local}%',)
        try:
            return self._fetch_all(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao buscar anotações por local: {e}")
            raise

    def buscar_anotacao_por_medico(self, medico):
        """ Busca anotações com base no médico. """
        sql = 'SELECT * FROM app_anotacoes WHERE medico LIKE ?'
        params = (f'%{medico}%',)
        try:
            return self._fetch_all(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao buscar anotações por médico: {e}")
            raise

    def buscar_anotacao_por_nota_fiscal(self, nota_fiscal):
        """ Busca anotações com base na nota fiscal. """
        sql = 'SELECT * FROM app_anotacoes WHERE nota_fiscal LIKE ?'
        params = (f'%{nota_fiscal}%',)
        try:
            return self._fetch_all(sql, params)
        except sqlite3.Error as e:
            print(f"Erro ao buscar anotações por nota fiscal: {e}")
            raise


    def listar_anotacoes(self):
        """ Lista todas as anotações no banco de dados. """
        sql = 'SELECT * FROM app_anotacoes'
        try:
            return self._fetch_all(sql)
        except sqlite3.Error as e:
            print(f"Erro ao listar anotações: {e}")
            raise
    
    def deletar_anotacao(self, id):
        """ Deleta uma anotação do banco de dados com base no ID. """
        sql = 'DELETE FROM app_anotacoes WHERE id = ?'
        try:
            self._execute_sql(sql, (id,))
        except sqlite3.Error as e:
            print(f"Erro ao deletar anotação: {e}")
            raise