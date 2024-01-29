import pyodbc

class SQLConnector(object):
    """This class connects to a SQL server and runs queries"""

    def __init__(self,server_name, database_name):
        self.server_name = server_name
        self.database_name = database_name
        
    def run_query(self, sql, parameters = None):
        cursor = self.connect()
        if parameters == None:
            cursor.execute(sql)
        else:
            cursor.execute(sql,parameters)
        return cursor

    def connect(self):
        #connection_string = 'Driver={SQL Server};' + 'Server={};Database={};Trusted_Connection=yes;'.format(self.server_name, self.database_name)
        #conn = pyodbc.connect(connection_string)
        conn = self.get_connection()
        return conn.cursor()

    def get_connection(self):
        connection_string = 'Driver={SQL Server};' + 'Server={};Database={};Trusted_Connection=yes;'.format(self.server_name, self.database_name)
        conn = pyodbc.connect(connection_string)
        return conn