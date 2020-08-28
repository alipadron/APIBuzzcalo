"""
Descripción:

Clase "Database", útil para decrementar complejidad al momento 
de realizar alguna consuta desde alguna parte del proyecto.
"""
import time
import os

import psycopg2


class Database:

    conn, cursor = None, None

    def __init__(self, pool_conn=None):
        """
        Constructor de la case Database.

        :param pool_conn. Conexión de la base de datos.

        Si pool_conn es diferente de None, se usará esta clase solo
        para manejar la conexión, su cursor y consultas sobre el cursor.

        Si pool_conn es igual a None, se levantarán recursos para una sola
        conexión.
        """
        if pool_conn == None:
            try:
                params = {
                    'host'      : os.getenv('pg_host'),
                    'database'  : os.getenv('pg_database'),
                    'user'      : os.getenv('pg_user'),
                    'password'  : os.getenv('pg_password')
                }

                # print( params )
                self.conn = psycopg2.connect( **params )
                self.cursor = self.conn.cursor()
                print('[INFO] Conexión creada con Postgres.\n')

            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
        else:
            # Esta conexión vendría desde la case 'DatabasePool'
            self.conn = pool_conn
            self.cursor = self.conn.cursor()

    
    def raw_query( self, sql:str ) -> list:
        """
        Método que recibe una consulta de tipo SELECT.

        :param sql str. Consulta en formato sql.
        """
        out = []
        try:
            time.sleep( .128 )
            self.cursor.execute( sql )
            out = self.cursor.fetchall()
            self.commit()
        except psycopg2.Error:
            self.roolback()

        return out


    def raw_insert(self, sql:str, values:list):
        """ 
        Se ejecuta una consulta de insersión, en caso de no ser ejecutada
        con éxito, se emitirá errores.

        :param sql str. Consulta en formato sql.

        :param values list. Parámetros que necesitará la consuta de inserción.
        """
        try:
            self.cursor.execute( sql, (values) )
            self.commit()
        except psycopg2.Error as err:
            # pass
            self.roolback()
            # print('[INFO] Error durante inserción.')
            # print( err )

    
    def raw_delete(self, sql:str):
        """
        Método que permite eliminar filas un tabla.

        :param sql str. Consulta en formato sql.
        """
        try:
            self.cursor.execute( sql )
            self.commit()
        except psycopg2.Error:
            self.roolback()


    def raw_update( self, sql:str):
        """
        Método que permite actualizar filas de una tabla.

        :param sql str. Consulta en formato sql.
        """
        try:
            time.sleep( .256 )
            self.cursor.execute( sql )
            self.commit()
        except psycopg2.Error:
            self.roolback()


    def close_cursor(self):
        
        if not self.cursor:
            raise Exception('[INFO] Cursor vacío, imposible cerrar.')

        self.cursor.close()


    def close_connection(self):

        if not self.conn:
            raise Exception('[INFO] Conexión vacía, imposible cerrar.')
        
        self.conn.close()


    def close(self):
        """
        Cierra la conexion inicializada. Se cierra el cursor actual,
        posteriormente la conexion.
        """
        # print('Cerrando conexión con Postgres.\n')
        if not self.conn:
            raise Exception('[INFO] Conexión vacía, imposible cerrar.')
            

        self.close_cursor()
        self.close_connection()


    def commit( self ):
        """ 
        Commit, materializa la transacción. 
        """
        if not self.conn:
            raise Exception('[INFO] Conexión vacía, no existe commit.')
        
        # print('[INFO] Commit')
        self.conn.commit()


    def roolback(self):
        """
        Roolback de la transacción, habilidatado para el cursor del
        instancia de la clase.
        """
        if not self.conn:
            raise Exception('[INFO] Conexión vacía, no existe roolback.')
        
        # print('[INFO] Rollback')
        self.conn.rollback()
