from django.db import connection

def getFromDB(query, args):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        return cursor.fetchall()