# ADGSTUDIOS 2021
import pyodbc
class sqlserver():
    def __init__(self,connectionstring):
	    self.connectionstring = connectionstring
            
    def ExecuteQuery(self, Query):
        try:
            conn = pyodbc.connect(self.connectionstring)
            cursor = conn.cursor()
            cursor.execute(Query)
            cursor.commit()
            print("Query Executed")
        except Exception as e:
            print(e)
    def fields(self, cur):
        results = {}
        column = 0
        for d in cur.description:
            results[d[0]] = column
            column = column + 1
        return results
    def GetRecordsOfColumn(self, SelectQuery, ColumnName):
        try:
            conn = pyodbc.connect(self.connectionstring)
            cursor = conn.cursor()
            cursor.execute(SelectQuery)
            field_map = self.fields(cursor)
            values = []
            for row in cursor:
                values.append(row[field_map[ColumnName]])
            return values
        except Exception as e:
            print(e)
    def GetRecordsAsDict(self, SelectQuery, ColumnName):
        try:
            conn = pyodbc.connect(self.connectionstring)
            cursor = conn.cursor()
            cursor.execute(SelectQuery)
            return {'results':
            [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]}
        except Exception as e:
            print(e)