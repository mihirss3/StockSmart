from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

class IndexView(APIView):
    def get(self, request):
        return Response({"message": "The backend is running fine"})

class ProductView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ProductId, Name, PackagingType, Weight FROM Product")
            rows = cursor.fetchall()
        products = [{"ProductId": row[0], "Name": row[1], "PackagingType": row[2], "Weight": row[3]} for row in rows]
        return Response(products)

class ProductCountView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Product")
            rows = cursor.fetchall()
        productsCount = {"count": rows[0][0]}
        return Response(productsCount)

class Top15ProductsExpiringSoonView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT p.Name,ExpiryDate, s.Name, SUM(i.Quantity) AS QuantityOfProductsGettingExpired FROM Product p LEFT JOIN Supplier s ON p.SupplierId = s.SupplierId INNER JOIN Inventory i ON i.ProductId = p.ProductId GROUP BY 1,2,3 ORDER BY ExpiryDate DESC LIMIT 15")
            rows = cursor.fetchall()
        products = [{"ProductName": row[0], "ExpiryDate": row[1], "SupplierName": row[2], "QuantityOfProductsGettingExpired": row[3]} for row in rows]
        return Response(products)


