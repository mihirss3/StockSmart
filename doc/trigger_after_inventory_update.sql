CREATE TRIGGER after_inventory_update
AFTER UPDATE ON Inventory
FOR EACH ROW
BEGIN
    DECLARE total_quantity INT;
    DECLARE product_name VARCHAR(255);

    -- Calculate total quantity for the product
    SELECT SUM(i.Quantity), p.Name
    INTO total_quantity, product_name
    FROM Inventory i
    INNER JOIN Product p ON i.ProductId = p.ProductId
    WHERE i.ProductId = NEW.ProductId
    GROUP BY i.ProductId;

    -- Check the conditions and insert into AlertTable
    IF total_quantity > 500 THEN
        INSERT INTO Alerts(AlertDateTime, ProductId, ProductName, AlertType, Quantity)
        VALUES (NOW(), NEW.ProductId, product_name, 'OverLoaded', total_quantity);
    ELSEIF total_quantity < 5 THEN
        INSERT INTO Alerts(AlertDateTime, ProductId, ProductName, AlertType, Quantity)
        VALUES (NOW(), NEW.ProductId, product_name, 'OutOfStockSoon', total_quantity);
    END IF;
END