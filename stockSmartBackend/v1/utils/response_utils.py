from rest_framework.response import Response


def handleExceptionResponse(exception):
    if exception is None:
        return Response({
            "success": False,
            "message": "There is some bug in the code, we have reported it to the team. Come back later to retry."
        }, status=500)
    if 'Duplicate' in exception:
        return Response({
            "success": False,
            "message": "You are trying to insert a duplicate record. This entry already exists."
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
    if 'chk_inventory_dates' in exception:
        return Response({
            "success": False,
            "message": "Please enter correct dates. ManufactureDate <= StockDate AND ManufactureDate <= ExpiryDate AND StockDate <= ExpiryDate"
        }, status=400)
    if 'chk_quantity' in exception:
        return Response({
            "success": False,
            "message": "Please enter correct quantity. Quantity cannot be negative"
        }, status=400)
    if 'chk_unitprice' in exception:
        return Response({
            "success": False,
            "message": "Please enter correct price. Price cannot be negative"
        }, status=400)
    return Response({
        "success": False,
        "message": str(exception)
    }, status=500)

def handleGetResponse(data):
    return Response({
        "success": True,
        "message": "All entries queried successfully",
        "data": data
    }, status=200)

def handlePostResponse(data):
    return Response({
        "success": True,
        "message": "New entry created successfully",
        "data": data
    }, status=201)

def handleDeleteResponse(data):
    if data:
        return Response({
            "success": True,
            "message": "Entry deleted successfully"
        }, status=200)
    else:
        return Response({
            "success": False,
            "message": "Entry not found"
        }, status=404)

def handlePutResponse(data):
    if data:
        return Response({
            "success": True,
            "message": "Entry updated successfully",
            "data": data
        }, status=200)
    else:
        return Response({
            "success": False,
            "message": "Failed to update entry"
        }, status=400)
