from rest_framework.views import APIView
from v1.utils.db_utils import *
from v1.utils.response_utils import *


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
        result, exception, userId = postToDB("INSERT INTO User(EmailId, Password, Type, FirstName, LastName, PhoneNumber) "
                 "VALUES(%s, %s, %s,%s, %s, %s)",
                 (data.get("EmailId"), data.get("Password"), data.get("Type"),data.get("FirstName"),data.get("LastName"), data.get("PhoneNumber")))
        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM User WHERE UserId = %s""", (userId,))
            row = rows[0]
            newUser = {"UserId": row[0], "EmailId": row[1], "Password": row[2], "Type": row[3], "FirstName": row[4], "LastName": row[5], "PhoneNumber": row[6]}
            return handlePostResponse(newUser)
        return handleExceptionResponse(None)

    def get(self, request):
        rows = getFromDB("""SELECT EmailId, FirstName, LastName, PhoneNumber FROM User WHERE Type='Analyst'""",())
        data = [
            {"EmailId": row[0], "FirstName": row[1], "LastName": row[2], "PhoneNumber": row[3]}
            for row in rows
        ]
        return handleGetResponse(data)

    def delete(self, request, emailId):
        result, exception = deleteFromDB("DELETE FROM User WHERE EmailId = %s", (emailId,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)

    def put(self, request, emailId):
        data = request.data
        update_query = """
                    UPDATE User 
                    SET Type = %s, FirstName = %s, LastName = %s, PhoneNumber = %s
                    WHERE EmailId = %s
                """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("Type"), data.get("FirstName"), data.get("LastName"), data.get("PhoneNumber"),emailId
        ))
        if exception:
            return handleExceptionResponse(exception)
        else:
            if result:
                rows = getFromDB("""SELECT * FROM User WHERE EmailId = %s""", (emailId,))
                row = rows[0]
                updated_user = {"UserId": row[0], "EmailId": row[1], "Type": row[3], "FirstName": row[4],
                           "LastName": row[5], "PhoneNumber": row[6]}
                return handlePutResponse(updated_user)
            else:
                return handlePutResponse(None)

class AdminAdministerInventoryView(APIView):
    def post(self, request):
        data = request.data
        result, exception, inventoryId = postToDB("""
            INSERT INTO Inventory(StockDate, ProductId, UnitPrice, ManufactureDate, ExpiryDate, Quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get("StockDate"),
            data.get("ProductId"),
            data.get("UnitPrice"),
            data.get("ManufactureDate"),
            data.get("ExpiryDate"),
            data.get("Quantity")
        ))

        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM Inventory WHERE InventoryId = %s""", (inventoryId,))
            new_inventory = rows[0]
            return handlePostResponse(new_inventory)
        return handleExceptionResponse(None)

    def get(self, request):
        rows = getFromDB("""SELECT * FROM Inventory""", ())
        data = [
            {"InventoryId": row[0],"StockDate": row[1],"ProductId": row[2],"UnitPrice": row[3],"ManufactureDate": row[4],"ExpiryDate": row[5],"Quantity": row[6]}
            for row in rows
        ]
        return handleGetResponse(data)

    def put(self, request, inventory_id):
        data = request.data
        update_query = """
            UPDATE Inventory 
            SET StockDate = %s, ProductId = %s, UnitPrice = %s, ManufactureDate = %s, ExpiryDate = %s, Quantity = %s
            WHERE InventoryId = %s
        """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("StockDate"),
            data.get("ProductId"),
            data.get("UnitPrice"),
            data.get("ManufactureDate"),
            data.get("ExpiryDate"),
            data.get("Quantity"),
            inventory_id
        ))

        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM Inventory WHERE InventoryId = %s""", (inventory_id,))
            updated_inventory = rows[0]
            return handlePutResponse(updated_inventory)

        else:
            return handlePutResponse(None)

    def delete(self, request, inventory_id):
        result, exception = deleteFromDB("DELETE FROM Inventory WHERE InventoryId = %s", (inventory_id,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)

class AdminAdministerSupplierView(APIView):
    def post(self, request):
        data = request.data
        result, exception, supplierId = postToDB("""
            INSERT INTO Supplier(Name, Address, Contact)
            VALUES (%s, %s, %s)
        """, (
            data.get("Name"),
            data.get("Address"),
            data.get("Contact")
        ))

        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM Supplier WHERE SupplierId = %s""", (supplierId,))
            row = rows[0]
            new_supplier = {"SupplierId": row[0],"Name": row[1],"Address": row[2],"Contact": row[3]}
            return handlePostResponse(new_supplier)
        return handleExceptionResponse(None)

    def get(self, request):
        rows = getFromDB("""SELECT SupplierId, Name, Address, Contact FROM Supplier""", ())
        data = [
            {"SupplierId": row[0],"Name": row[1],"Address": row[2],"Contact": row[3]}
            for row in rows
        ]
        return handleGetResponse(data)

    def put(self, request, supplier_id):
        data = request.data
        update_query = """
            UPDATE Supplier 
            SET Name = %s, Address = %s, Contact = %s
            WHERE SupplierId = %s
        """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("Name"), data.get("Address"), data.get("Contact"), supplier_id
        ))

        if exception:
            return handleExceptionResponse(exception)

        if result:
            rows = getFromDB("""SELECT * FROM Supplier WHERE SupplierId = %s""", (supplier_id,))
            row = rows[0]
            updated_supplier = {"SupplierId": row[0],"Name": row[1],"Address": row[2],"Contact": row[3]}
            return handlePutResponse(updated_supplier)
        else:
            return handlePutResponse(None)

    def delete(self, request, supplier_id):
        result, exception = deleteFromDB("DELETE FROM Supplier WHERE SupplierId = %s", (supplier_id,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)

class AdminAdministerCategoryView(APIView):
    def post(self, request):
        data = request.data
        result, exception, categoryId = postToDB("""
            INSERT INTO Category(Name, LeadTime, StorageRequirements)
            VALUES (%s, %s, %s)
        """, (
            data.get("Name"),
            data.get("LeadTime"),
            data.get("StorageRequirements")
        ))

        if exception:
            return handleExceptionResponse(exception)

        if result:
            rows = getFromDB("""SELECT * FROM Category WHERE CategoryId = %s""", (categoryId,))
            row = rows[0]
            new_category = [{"CategoryId": row[0],"Name": row[1],"LeadTime": row[2],"StorageRequirements": row[3]}]
            return handlePostResponse(new_category)

        return handleExceptionResponse(None)

    def get(self, request):
        rows = getFromDB("""SELECT CategoryId, Name, LeadTime, StorageRequirements FROM Category""", ())
        data = [
            {"CategoryId": row[0],"Name": row[1],"LeadTime": row[2],"StorageRequirements": row[3]}
            for row in rows
        ]
        return handleGetResponse(data)

    def put(self, request, category_id):
        data = request.data
        update_query = """
            UPDATE Category 
            SET Name = %s, LeadTime = %s, StorageRequirements = %s
            WHERE CategoryId = %s
        """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("Name"),
            data.get("LeadTime"),
            data.get("StorageRequirements"),
            category_id
        ))
        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM Category WHERE CategoryId = %s""", (category_id,))
            row = rows[0]
            updated_category = {"CategoryId": row[0],"Name": row[1],"LeadTime": row[2],"StorageRequirements": row[3]}
            return handlePutResponse(updated_category)
        else:
            return handlePutResponse(None)

    def delete(self, request, category_id):
        result, exception = deleteFromDB("DELETE FROM Category WHERE CategoryId = %s", (category_id,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)

class AdminAdministerProductView(APIView):
    def post(self, request):
        data = request.data
        result, exception, productId = postToDB("""
            INSERT INTO Product(Name, PackagingType, Weight, CategoryId, SupplierId)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("Name"),
            data.get("PackagingType"),
            data.get("Weight"),
            data.get("CategoryId"),
            data.get("SupplierId")
        ))

        if exception:
            return handleExceptionResponse(exception)

        if result:
            rows = getFromDB("""SELECT * FROM Product WHERE ProductId = %s""", (productId,))
            row = rows[0]
            new_product = {"ProductId": row[0],"Name": row[1],"PackagingType": row[2],"Weight": row[3],"CategoryId": row[4],"SupplierId": row[5]}
            return handlePostResponse(new_product)
        return handleExceptionResponse(None)

    def get(self, request):
        rows = getFromDB("""SELECT ProductId, Name, PackagingType, Weight, CategoryId, SupplierId FROM Product""", ())
        data = [
            {"ProductId": row[0],"Name": row[1],"PackagingType": row[2],"Weight": row[3],"CategoryId": row[4],"SupplierId": row[5]}
            for row in rows
        ]
        return handleGetResponse(data)

    def put(self, request, product_id):
        data = request.data
        update_query = """
            UPDATE Product 
            SET Name = %s, PackagingType = %s, Weight = %s, CategoryId = %s, SupplierId = %s
            WHERE ProductId = %s
        """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("Name"),
            data.get("PackagingType"),
            data.get("Weight"),
            data.get("CategoryId"),
            data.get("SupplierId"),
            product_id
        ))

        if exception:
            return handleExceptionResponse(exception)
        if result:
            rows = getFromDB("""SELECT * FROM Product WHERE ProductId = %s""", (product_id,))
            row = rows[0]
            updated_product = {"ProductId": row[0],"Name": row[1],"PackagingType": row[2],"Weight": row[3], "CategoryId": row[4],"SupplierId": row[5]}
            return handlePutResponse(updated_product)
        else:
            return handlePutResponse(None)

    def delete(self, request, product_id):
        result, exception = deleteFromDB("DELETE FROM Product WHERE ProductId = %s", (product_id,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)

class AdminAdministerPromotionalOfferView(APIView):
    def post(self, request):
        data = request.data
        result, exception, promotionalOfferId = postToDB("""
            INSERT INTO PromotionalOffer(StartDate, EndDate, DiscountRate)
            VALUES (%s, %s, %s)
        """, (
            data.get("StartDate"),
            data.get("EndDate"),
            data.get("DiscountRate")
        ))

        if exception:
            return handleExceptionResponse(exception)

        if result:
            rows = getFromDB("""SELECT * FROM PromotionalOffer WHERE PromotionalOfferId = %s""", (promotionalOfferId,))
            row = rows[0]
            new_offer = {"PromotionalOfferId": row[0],"StartDate": row[1],"EndDate": row[2],"DiscountRate": row[3]}
            return handlePostResponse(new_offer)

        return handleExceptionResponse(exception)

    def get(self, request):
        rows = getFromDB("""SELECT PromotionalOfferId, StartDate, EndDate, DiscountRate FROM PromotionalOffer""", ())
        data = [
            {"PromotionalOfferId": row[0],"StartDate": row[1],"EndDate": row[2],"DiscountRate": row[3]}
            for row in rows
        ]
        return handleGetResponse(data)

    def put(self, request, promotional_offer_id):
        data = request.data
        update_query = """
            UPDATE PromotionalOffer 
            SET StartDate = %s, EndDate = %s, DiscountRate = %s
            WHERE PromotionalOfferId = %s
        """
        result, exception, lastUpdatedRowId = postToDB(update_query, (
            data.get("StartDate"),
            data.get("EndDate"),
            data.get("DiscountRate"),
            promotional_offer_id
        ))

        if exception:
            return handleExceptionResponse(exception)

        if result:
            rows = getFromDB("""SELECT * FROM PromotionalOffer WHERE PromotionalOfferId = %s""",
                             (promotional_offer_id,))
            row = rows[0]
            updated_offer = {"PromotionalOfferId": row[0],"StartDate": row[1],"EndDate": row[2],"DiscountRate": row[3]}
            return handlePutResponse(updated_offer)
        else:
            return handlePutResponse(None)

    def delete(self, request, promotional_offer_id):
        result, exception = deleteFromDB("DELETE FROM PromotionalOffer WHERE PromotionalOfferId = %s",
                                         (promotional_offer_id,))
        if exception:
            return handleExceptionResponse(exception)
        else:
            return handleDeleteResponse(result)
