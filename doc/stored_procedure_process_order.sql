CREATE PROCEDURE process_order(
    IN p_order_date DATE,
    IN p_order_items JSON
)
BEGIN
    DECLARE v_inventory_quantity INT;
    DECLARE v_quantity_to_update INT;
    DECLARE v_error_message VARCHAR(255);

    -- Start transaction
    START TRANSACTION;

    -- Insert new order
    INSERT INTO `Order` (OrderDate) VALUES (p_order_date);
    SET @order_id = LAST_INSERT_ID();

    -- Use FOREACH to iterate through JSON array
    SET @item_count = JSON_LENGTH(p_order_items);
    WHILE @item_count > 0 DO
        -- Extract item details
        SET @inventory_id = JSON_UNQUOTE(JSON_EXTRACT(p_order_items, CONCAT('$[', @item_count - 1, '].InventoryId')));
        SET @quantity = JSON_UNQUOTE(JSON_EXTRACT(p_order_items, CONCAT('$[', @item_count - 1, '].Quantity')));
        SET @item_count = @item_count - 1;

        -- Check inventory quantity
        SELECT Quantity INTO v_inventory_quantity 
        FROM Inventory 
        WHERE InventoryId = @inventory_id;

        IF v_inventory_quantity < @quantity THEN
            -- If not enough stock, rollback and throw an error
            SET v_error_message = CONCAT('InventoryId ', @inventory_id, ' does not have enough stock. It has only ', v_inventory_quantity, ' quantities left.');
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_error_message;
        END IF;

        -- Update inventory quantity
        SET v_quantity_to_update = v_inventory_quantity - @quantity;
        UPDATE Inventory 
        SET Quantity = v_quantity_to_update
        WHERE InventoryId = @inventory_id;

        -- Insert into order_contains_inventories
        INSERT INTO Order_Contains_Inventories (OrderId, InventoryId, Quantity)
        VALUES (@order_id, @inventory_id, @quantity);

    END WHILE;

    -- Commit the transaction
    COMMIT;
END;