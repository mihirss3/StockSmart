
from django.db import connection, IntegrityError


def getFromDB(query, args):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        return cursor.fetchall()

def postToDB(query, args):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            if cursor.rowcount > 0:
                return True, None, cursor.lastrowid
        return False, None, None
    except Exception as e:
        print(str(e))
        return False, str(e), None

def deleteFromDB(query, args):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            if cursor.rowcount == 0:
                return False, None
            return True, None
    except Exception as e:
        print(str(e))
        return False, str(e)
