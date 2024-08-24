import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="notas.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
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
                observacao TEXT
            )
        ''')
        self.connection.commit()

    def close(self):
        self.connection.close()

