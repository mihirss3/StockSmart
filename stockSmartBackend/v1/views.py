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

class AdminAdministerInventoryView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("""
            INSERT INTO Inventory(InventoryId, StockDate, ProductId, UnitPrice, ManufactureDate, ExpiryDate, Quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("InventoryId"),
            data.get("StockDate"),
            data.get("ProductId"),
            data.get("UnitPrice"),
            data.get("ManufactureDate"),
            data.get("ExpiryDate"),
            data.get("Quantity")
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Inventory WHERE InventoryId = %s""", (data.get("InventoryId"),))
            new_inventory = rows[0]
            return Response({
                "success": True,
                "message": "Inventory created successfully",
                "data": {
                    "Inventory": {
                        "InventoryId": new_inventory[0],
                        "StockDate": new_inventory[1],
                        "ProductId": new_inventory[2],
                        "UnitPrice": new_inventory[3],
                        "ManufactureDate": new_inventory[4],
                        "ExpiryDate": new_inventory[5],
                        "Quantity": new_inventory[6]
                    }
                }
            }, status=201)

        return Response({
            "success": False,
            "message": "Failed to create inventory"
        }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT * FROM Inventory""", ())
        for row in rows:
            data.append({
                "InventoryId": row[0],
                "StockDate": row[1],
                "ProductId": row[2],
                "UnitPrice": row[3],
                "ManufactureDate": row[4],
                "ExpiryDate": row[5],
                "Quantity": row[6]
            })
        return Response({
            "success": True,
            "message": "Inventory data fetched successfully",
            "data": {"Inventory": data}
        }, status=200)

    def put(self, request, inventory_id):
        data = request.data
        update_query = """
            UPDATE Inventory 
            SET StockDate = %s, ProductId = %s, UnitPrice = %s, ManufactureDate = %s, ExpiryDate = %s, Quantity = %s
            WHERE InventoryId = %s
        """
        result, exception = postToDB(update_query, (
            data.get("StockDate"),
            data.get("ProductId"),
            data.get("UnitPrice"),
            data.get("ManufactureDate"),
            data.get("ExpiryDate"),
            data.get("Quantity"),
            inventory_id
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Inventory WHERE InventoryId = %s""", (inventory_id,))
            updated_inventory = rows[0]
            return Response({
                "success": True,
                "message": "Inventory updated successfully",
                "data": {
                    "Inventory": {
                        "InventoryId": updated_inventory[0],
                        "StockDate": updated_inventory[1],
                        "ProductId": updated_inventory[2],
                        "UnitPrice": updated_inventory[3],
                        "ManufactureDate": updated_inventory[4],
                        "ExpiryDate": updated_inventory[5],
                        "Quantity": updated_inventory[6]
                    }
                }
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Failed to update inventory"
            }, status=400)

    def delete(self, request, inventory_id):
        result, exception = deleteFromDB("DELETE FROM Inventory WHERE InventoryId = %s", (inventory_id,))
        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "Inventory deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Inventory not found"
                }, status=404)

class AdminAdministerSupplierView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("""
            INSERT INTO Supplier(SupplierId, Name, Address, Contact)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get("SupplierId"),
            data.get("Name"),
            data.get("Address"),
            data.get("Contact")
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Supplier WHERE SupplierId = %s""", (data.get("SupplierId"),))
            new_supplier = rows[0]
            return Response({
                "success": True,
                "message": "Supplier created successfully",
                "data": {
                    "Supplier": {
                        "SupplierId": new_supplier[0],
                        "Name": new_supplier[1],
                        "Address": new_supplier[2],
                        "Contact": new_supplier[3]
                    }
                }
            }, status=201)

        return Response({
            "success": False,
            "message": "Failed to create supplier"
        }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT SupplierId, Name, Address, Contact FROM Supplier""", ())
        for row in rows:
            data.append({
                "SupplierId": row[0],
                "Name": row[1],
                "Address": row[2],
                "Contact": row[3]
            })
        return Response({
            "success": True,
            "message": "Supplier data fetched successfully",
            "data": {"Suppliers": data}
        }, status=200)

    def put(self, request, supplier_id):
        data = request.data
        update_query = """
            UPDATE Supplier 
            SET Name = %s, Address = %s, Contact = %s
            WHERE SupplierId = %s
        """
        result, exception = postToDB(update_query, (
            data.get("Name"), data.get("Address"), data.get("Contact"), supplier_id
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Supplier WHERE SupplierId = %s""", (supplier_id,))
            updated_supplier = rows[0]
            return Response({
                "success": True,
                "message": "Supplier updated successfully",
                "data": {
                    "Supplier": {
                        "SupplierId": updated_supplier[0],
                        "Name": updated_supplier[1],
                        "Address": updated_supplier[2],
                        "Contact": updated_supplier[3]
                    }
                }
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Failed to update supplier"
            }, status=400)

    def delete(self, request, supplier_id):
        result, exception = deleteFromDB("DELETE FROM Supplier WHERE SupplierId = %s", (supplier_id,))
        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "Supplier deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Supplier not found"
                }, status=404)

class AdminAdministerCategoryView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("""
            INSERT INTO Category(CategoryId, Name, LeadTime, StorageRequirements)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get("CategoryId"),
            data.get("Name"),
            data.get("LeadTime"),
            data.get("StorageRequirements")
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Category WHERE CategoryId = %s""", (data.get("CategoryId"),))
            new_category = rows[0]
            return Response({
                "success": True,
                "message": "Category created successfully",
                "data": {
                    "Category": {
                        "CategoryId": new_category[0],
                        "Name": new_category[1],
                        "LeadTime": new_category[2],
                        "StorageRequirements": new_category[3]
                    }
                }
            }, status=201)

        return Response({
            "success": False,
            "message": "Failed to create category"
        }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT CategoryId, Name, LeadTime, StorageRequirements FROM Category""", ())
        for row in rows:
            data.append({
                "CategoryId": row[0],
                "Name": row[1],
                "LeadTime": row[2],
                "StorageRequirements": row[3]
            })
        return Response({
            "success": True,
            "message": "Category data fetched successfully",
            "data": {"Categories": data}
        }, status=200)

    def put(self, request, category_id):
        data = request.data
        update_query = """
            UPDATE Category 
            SET Name = %s, LeadTime = %s, StorageRequirements = %s
            WHERE CategoryId = %s
        """
        result, exception = postToDB(update_query, (
            data.get("Name"),
            data.get("LeadTime"),
            data.get("StorageRequirements"),
            category_id
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Category WHERE CategoryId = %s""", (category_id,))
            updated_category = rows[0]
            return Response({
                "success": True,
                "message": "Category updated successfully",
                "data": {
                    "Category": {
                        "CategoryId": updated_category[0],
                        "Name": updated_category[1],
                        "LeadTime": updated_category[2],
                        "StorageRequirements": updated_category[3]
                    }
                }
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Failed to update category"
            }, status=400)

    def delete(self, request, category_id):
        result, exception = deleteFromDB("DELETE FROM Category WHERE CategoryId = %s", (category_id,))
        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "Category deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Category not found"
                }, status=404)

class AdminAdministerProductView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("""
            INSERT INTO Product(ProductId, Name, PackagingType, Weight, CategoryId, SupplierId)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get("ProductId"),
            data.get("Name"),
            data.get("PackagingType"),
            data.get("Weight"),
            data.get("CategoryId"),
            data.get("SupplierId")
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Product WHERE ProductId = %s""", (data.get("ProductId"),))
            new_product = rows[0]
            return Response({
                "success": True,
                "message": "Product created successfully",
                "data": {
                    "Product": {
                        "ProductId": new_product[0],
                        "Name": new_product[1],
                        "PackagingType": new_product[2],
                        "Weight": new_product[3],
                        "CategoryId": new_product[4],
                        "SupplierId": new_product[5]
                    }
                }
            }, status=201)

        return Response({
            "success": False,
            "message": "Failed to create product"
        }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT ProductId, Name, PackagingType, Weight, CategoryId, SupplierId FROM Product""", ())
        for row in rows:
            data.append({
                "ProductId": row[0],
                "Name": row[1],
                "PackagingType": row[2],
                "Weight": row[3],
                "CategoryId": row[4],
                "SupplierId": row[5]
            })
        return Response({
            "success": True,
            "message": "Product data fetched successfully",
            "data": {"Products": data}
        }, status=200)

    def put(self, request, product_id):
        data = request.data
        update_query = """
            UPDATE Product 
            SET Name = %s, PackagingType = %s, Weight = %s, CategoryId = %s, SupplierId = %s
            WHERE ProductId = %s
        """
        result, exception = postToDB(update_query, (
            data.get("Name"),
            data.get("PackagingType"),
            data.get("Weight"),
            data.get("CategoryId"),
            data.get("SupplierId"),
            product_id
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM Product WHERE ProductId = %s""", (product_id,))
            updated_product = rows[0]
            return Response({
                "success": True,
                "message": "Product updated successfully",
                "data": {
                    "Product": {
                        "ProductId": updated_product[0],
                        "Name": updated_product[1],
                        "PackagingType": updated_product[2],
                        "Weight": updated_product[3],
                        "CategoryId": updated_product[4],
                        "SupplierId": updated_product[5]
                    }
                }
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Failed to update product"
            }, status=400)

    def delete(self, request, product_id):
        result, exception = deleteFromDB("DELETE FROM Product WHERE ProductId = %s", (product_id,))
        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "Product deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Product not found"
                }, status=404)

class AdminAdministerPromotionalOfferView(APIView):
    def post(self, request):
        data = request.data
        result, exception = postToDB("""
            INSERT INTO PromotionalOffer(PromotionalOfferId, StartDate, EndDate, DiscountRate)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get("PromotionalOfferId"),
            data.get("StartDate"),
            data.get("EndDate"),
            data.get("DiscountRate")
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM PromotionalOffer WHERE PromotionalOfferId = %s""", (data.get("PromotionalOfferId"),))
            new_offer = rows[0]
            return Response({
                "success": True,
                "message": "Promotional offer created successfully",
                "data": {
                    "PromotionalOffer": {
                        "PromotionalOfferId": new_offer[0],
                        "StartDate": new_offer[1],
                        "EndDate": new_offer[2],
                        "DiscountRate": new_offer[3]
                    }
                }
            }, status=201)

        return Response({
            "success": False,
            "message": "Failed to create promotional offer"
        }, status=400)

    def get(self, request):
        data = []
        rows = getFromDB("""SELECT PromotionalOfferId, StartDate, EndDate, DiscountRate FROM PromotionalOffer""", ())
        for row in rows:
            data.append({
                "PromotionalOfferId": row[0],
                "StartDate": row[1],
                "EndDate": row[2],
                "DiscountRate": row[3]
            })
        return Response({
            "success": True,
            "message": "Promotional offer data fetched successfully",
            "data": {"PromotionalOffers": data}
        }, status=200)

    def put(self, request, promotional_offer_id):
        data = request.data
        update_query = """
            UPDATE PromotionalOffer 
            SET StartDate = %s, EndDate = %s, DiscountRate = %s
            WHERE PromotionalOfferId = %s
        """
        result, exception = postToDB(update_query, (
            data.get("StartDate"),
            data.get("EndDate"),
            data.get("DiscountRate"),
            promotional_offer_id
        ))

        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)

        if result:
            rows = getFromDB("""SELECT * FROM PromotionalOffer WHERE PromotionalOfferId = %s""",
                             (promotional_offer_id,))
            updated_offer = rows[0]
            return Response({
                "success": True,
                "message": "Promotional offer updated successfully",
                "data": {
                    "PromotionalOffer": {
                        "PromotionalOfferId": updated_offer[0],
                        "StartDate": updated_offer[1],
                        "EndDate": updated_offer[2],
                        "DiscountRate": updated_offer[3]
                    }
                }
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Failed to update promotional offer"
            }, status=400)

    def delete(self, request, promotional_offer_id):
        result, exception = deleteFromDB("DELETE FROM PromotionalOffer WHERE PromotionalOfferId = %s",
                                         (promotional_offer_id,))
        if exception:
            return Response({
                "success": False,
                "message": str(exception)
            }, status=500)
        else:
            if result:
                return Response({
                    "success": True,
                    "message": "Promotional offer deleted successfully"
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "message": "Promotional offer not found"
                }, status=404)


class fetchChartOneData(APIView):
        def get():
            data = []
            rows = getFromDB("""SELECT prod.Name,SUM(inventory.Quantity) 
                             FROM Inventory inventory INNER JOIN Product prod 
                             ON inventory.ProductId=prod.ProductId
                             GROUP BY 1""", ())
            for row in rows:
                data.append({
                    "Product Name": row[0],
                    "Quantity": row[1],
                })
            return Response({
                "success": True,
                "message": "Product Details and Quantity for Graph 1 data fetched successfully",
                "data": {"Graph 1": data}
            }, status=200)
        
class fetchChartTwoData(APIView):
        def get():
            data = []
            rows = getFromDB("""
                SELECT cat.Name,prod.Name,SUM(i.Quantity) FROM 
                Order_Contains_Inventories orders 
                LEFT JOIN 
                Inventory i 
                ON orders.inventoryId=i.InventoryId 
                LEFT JOIN 
                Product prod 
                ON prod.ProductId=i.ProductId 
                LEFT JOIN
                Category cat
                ON cat.CategoryId=prod.CategoryId         
                WHERE prod.CategoryId =  
                ( 
                    SELECT cat.CategoryID FROM 
                    Order_Contains_Inventories orders
                    LEFT JOIN 
                    Inventory i 
                    ON orders.inventoryId=i.InventoryId 
                    LEFT JOIN 
                    Product prod
                    ON prod.ProductId=i.ProductId 
                    LEFT JOIN 
                    Category cat
                    ON prod.CategoryId=cat.CategoryId 
                    GROUP BY cat.CategoryId 
                    ORDER BY SUM(orders.Quantity) DESC 
                    LIMIT 1 
                ) 
                GROUP BY 1,2
                ORDER BY SUM(orders.Quantity*i.UnitPrice) DESC 
                LIMIT 30;""", ())
            for row in rows:
                data.append({
                    "Category Name":row[0],
                    "Product Name": row[1],
                    "Quantity": row[2],
                })
            return Response({
                "success": True,
                "message": "Product Details and Quantity for Graph 1 data fetched successfully",
                "data": {"Graph 2": data}
            }, status=200)
        
class fetchChartThreeData(APIView):
        def get():
            data = []
            rows = getFromDB("""
                SELECT prod.Name,sum(invent.Quantity) FROM 
                (
                SELECT oci.InventoryId
                FROM 
                Order_Contains_Inventories oci
                LEFT JOIN
                `Order` orr
                ON oci.OrderId=orr.OrderId
                WHERE ABS(DATEDIFF(orr.OrderDate,DATE('2024-05-28')))<31 AND orr.OrderDate<DATE('2024-05-28')
                GROUP BY 1
                HAVING SUM(oci.Quantity)<10
                INTERSECT
                SELECT InventoryId FROM Inventory
                WHERE  ExpiryDate>DATE('2024-05-28') 
                AND ABS(DATEDIFF(ExpiryDate,DATE('2024-05-28')))<15
                )id 
                LEFT JOIN
                Inventory invent
                ON id.InventoryId=invent.InventoryId
                LEFT JOIN
                Product prod
                ON invent.ProductId=prod.ProductId
                GROUP BY 1
                """, ())
            for row in rows:
                data.append({
                    "Product Name": row[0],
                    "Quantity": row[1],
                })
            return Response({
                "success": True,
                "message": "Product Details and Quantity for Graph 3 data fetched successfully",
                "data": {"Graph 2": data}
            }, status=200)
        

