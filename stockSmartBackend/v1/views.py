from rest_framework.response import Response
from rest_framework.views import APIView
from v1.db_utils.utils import getFromDB

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
            return Response({"loginSuccess": False})
        else:
            userType = rows[0][0]
            return Response({"loginSuccess": True, "userType": userType})

