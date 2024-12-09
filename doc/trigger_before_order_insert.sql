CREATE TRIGGER before_order_insert
BEFORE INSERT ON `Order_Contains_Inventories`
FOR EACH ROW
BEGIN
    DECLARE previousLastDate DATE;
    DECLARE newOrderDate DATE;
    SET previousLastDate = (SELECT MAX(OrderDate) FROM `Order` WHERE OrderId <> NEW.OrderId);
    SET newOrderDate = (SELECT OrderDate FROM `Order` WHERE OrderId = NEW.OrderId);
    IF DATEDIFF(newOrderDate, previousLastDate) >= 1 THEN
        INSERT INTO Stock_Smart_Wide (
            OrderId, OrderDate, TotalPrice, InventoryId, StockDate, UnitPrice,
            ManufactureDate, ExpiryDate, Quantity, ProductId, ProductName,
            PackagingType, Weight, SupplierId, SupplierName, Address, Contact,
            CategoryId, CategoryName, LeadTime, StorageRequirements,
            PromotionalOfferId, StartDate, EndDate, DiscountRate
        )
          SELECT 
            orders.OrderId, 
            orders.OrderDate, 
            orders.TotalPrice, 
            invent.InventoryId, 
            invent.StockDate, 
            invent.UnitPrice, 
            invent.ManufactureDate, 
            invent.ExpiryDate, 
            invent.Quantity,
            prod.ProductId, 
            prod.Name AS ProductName, 
            prod.PackagingType, 
            prod.weight, 
            supp.SupplierId, 
            supp.Name AS SupplierName, 
            supp.Address, 
            supp.Contact,
            cat.CategoryId, 
            cat.Name AS CategoryName, 
            cat.LeadTime, 
            cat.StorageRequirements,
            prom.PromotionalOfferId, 
            prom.StartDate, 
            prom.EndDate, 
            prom.DiscountRate
          FROM 
            `Order` orders
            LEFT JOIN Order_Contains_Inventories a ON orders.OrderId = a.OrderId
            LEFT JOIN Inventory invent ON a.InventoryId = invent.InventoryId
            LEFT JOIN Product prod ON invent.ProductId = prod.ProductId
            LEFT JOIN Category cat ON prod.CategoryId = cat.CategoryId
            LEFT JOIN Supplier supp ON supp.SupplierId = prod.SupplierId
            LEFT JOIN PromotionalOffers_AppliedOn_Order b ON orders.OrderId = b.OrderId
            LEFT JOIN PromotionalOffer prom ON prom.PromotionalOfferId = b.PromotionalOfferId
          WHERE orders.OrderDate = previousLastDate;
    END IF;
END