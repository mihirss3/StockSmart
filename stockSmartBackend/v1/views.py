from rest_framework.response import Response
from rest_framework.views import APIView
from v1.utils.db_utils import *


class IndexView(APIView):
    def get(self, request):
        return Response({"message": "The backend is running fine"})

class LoginView(APIView):
    def post(self, request):
        data = request.data
        emailId = data.get("emailId")
        password = data.get("password")
        rows = getFromDB("""SELECT Type FROM User WHERE EmailId = %s AND Password = %s""", (emailId,password))
        if not rows:
            return Response({
                "success": False,
                "message": "Invalid Credentials. Please check your email id and password again"
            }, status=403)
        else:
            userType = rows[0][0]
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {"type": userType}
            }, status=200)

class AdminAdministerUserView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("INSERT INTO User(EmailId, Password, Type, FirstName, LastName, PhoneNumber) "
                 "VALUES(%s, %s, %s,%s, %s, %s)",
                 (data.get("emailId"), data.get("password"), data.get("type"),data.get("firstName"),data.get("lastName"), data.get("phoneNumber")))
        if exception:
            if 'Duplicate' in exception:
                return Response({
                    "success": False,
                    "message": "User with this email id already exists"
                }, status=500)
            if 'chk_email_format' in exception:
                return Response({
                    "success": False,
                    "message": "Please enter correct email"
                }, status=400)
            if 'chk_password_complexity' in exception:
                return Response({
                    "success": False,
                    "message": "Please enter correct password. It must be at least 6 characters long and contain at least one digit, one uppercase and one lowercase letter"
                }, status=400)
        if result:
            rows = getFromDB("""SELECT * FROM User WHERE emailId = %s""", (data.get("emailId"),))
            newUser = rows[0]
            return Response({
                "success": True,
                "message": "New user created successfully",
                "data": {
                    "User": {
                        "UserId": newUser[0],
                        "EmailId": newUser[1],
                        "Password": newUser[2],
                        "Type": newUser[3],
                        "FirstName": newUser[4],
                        "LastName": newUser[5],
                        "PhoneNumber": newUser[6]
                    }
                }
            }, status=201)
        else:
            return Response({
                "success": False,
                "message": "New user was not created, please check your input"
            }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT EmailId, FirstName, LastName, PhoneNumber FROM User WHERE Type='Analyst'""",())
        for row in rows:
            data.append({
                "EmailId" : row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "PhoneNumber": row[3]
            })
        return Response({
            "success": True,
            "message": "New user created successfully",
            "data": {
                "Users": data
            }
        }, status=200)

    def delete(self, request, emailId):
        result, exception = deleteFromDB("DELETE FROM User WHERE EmailId = %s", (emailId,))
        if exception:
            return Response({
                "success": False,
                "message": exception
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "User deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "User not found"
                }, status=404)

    def put(self, request, emailId):
        data = request.data
        update_query = """
                    UPDATE User 
                    SET Type = %s, FirstName = %s, LastName = %s, PhoneNumber = %s
                    WHERE EmailId = %s
                """
        result, exception = postToDB(update_query, (
            data.get("Type"), data.get("FirstName"), data.get("LastName"), data.get("PhoneNumber"),emailId
        ))
        if exception:
            return Response({
                "success": False,
                "message": exception
            }, status=500)
        else:
            if result:
                rows = getFromDB("""SELECT * FROM User WHERE EmailId = %s""", (emailId,))
                updated_user = rows[0]
                return Response({
                    "success": True,
                    "message": "User updated successfully",
                    "data": {
                        "User": {
                            "UserId": updated_user[0],
                            "EmailId": updated_user[1],
                            "Password": updated_user[2],
                            "Type": updated_user[3],
                            "FirstName": updated_user[4],
                            "LastName": updated_user[5],
                            "PhoneNumber": updated_user[6]
                        }
                    }
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Failed to update user"
                }, status=400)




