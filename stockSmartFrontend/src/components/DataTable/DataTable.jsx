import React, {  useEffect, useMemo, useState} from "react";
import "./DataTable.css";
import {MaterialReactTable} from "material-react-table";
import DeleteIcon from '@mui/icons-material/Delete';


const DataTable = ({ data, setData, schema }) => {
  
  const columns = useMemo(() => {
    // Define the columns from the data (excluding the delete column)
    const baseColumns = Object.keys(data[0] || {}).map((key) => ({
      accessorKey: key,
      header: key,
      field: key,
      id: key,
      enableEditing: true,
      size: 10
    }));

    // Add the delete column at the end
    const deleteColumn = {
      accessorKey: "delete", // Adding a delete column key
      header: "Actions",
      Cell: ({ row }) => (
        <button
          className="table-button"
          onClick={(e) => {
            e.stopPropagation();
            handleDeleteRow(row); 
          }}
        >
  <DeleteIcon style={{ color: "#ca5353" }} />
  </button>
      ),
    };

    return [deleteColumn, ...baseColumns]; // Return columns with the delete column at the end
  }, [data]);


  const handleSaveRow = async ({ table, row, values }) => {
    console.log("values", values)

    const apiEndpoints = {
      "User": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/user/${row.original.EmailId}`,
      "Promotional Offer": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/promotionaloffer/${row.original.PromotionalOfferId}`,
      "Supplier": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/supplier/${row.original.SupplierId}`,
      "Category": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/category/${row.original.CategoryId}`,
      "Product": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/product/${row.original.ProductId}`,
      "Inventory": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/inventory/${row.original.InventoryId}`,
    };
  
    const endpoint = apiEndpoints[schema];
    if (!endpoint) {
      console.error(`No API endpoint defined for schema: ${schema}`);
      alert("Update failed: Unknown schema");
      return;
    }

    let body = {};
    switch (schema) {
      case "User":
        body = {
          Password: values.Password || "defaultPassword", 
          Type: values.Type,
          FirstName: values.FirstName,
          LastName: values.LastName,
        };
        break;
      case "Promotional Offer":
        body = {
          StartDate: values.StartDate,
          EndDate: values.EndDate,
          DiscountRate: parseFloat(values.DiscountRate),
        };
        break;
      case "Supplier":
        body = {
          Name: values.Name,
          Address: values.Address,
          Contact: values.Contact,
        };
        break;
      case "Category":
        body = {
          Name: values.Name,
          LeadTime: values.LeadTime,
          StorageRequirements: values.StorageRequirements,
        };
        break;
      case "Product":
        body = {
          Name: values.Name,
          PackagingType: values.PackagingType,
          Weight: parseFloat(values.Weight),
          CategoryId: parseInt(values.CategoryId, 10),
          SupplierId: parseInt(values.SupplierId, 10),
        };
        break;
      case "Inventory":
        body = {
          StockDate: values.StockDate,
          ProductId: parseInt(values.ProductId, 10),
          UnitPrice: parseFloat(values.UnitPrice),
          ManufactureDate: values.ManufactureDate,
          ExpiryDate: values.ExpiryDate,
          Quantity: parseInt(values.Quantity, 10),
        };
        break;
      default:
        console.error(`Unknown schema: ${schema}`);
        alert("Update failed: Unknown schema");
        return;
    }
  
    console.log(schema, " body: ", JSON.stringify(body))
    try {
      const response = await fetch(endpoint, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });
  
      if (!response.ok) {
        throw new Error(`Failed to update ${schema}. Status: ${response.status}`);
      }
  
      fetchData(schema);
  
      alert(`${schema} row updated successfully`);
    } catch (error) {
      fetchData(schema);
      table.setEditingRow(null);
      console.error("Error updating row:", error);
      alert(`An error occurred while updating ${schema}.`);
    } finally {
      table.setEditingRow(null); // Exit editing mode
    }
  };
  

  const handleDeleteRow = async (row) => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete this item?`
    );

    if (confirmDelete) {
      try {
        const apiEndpoints = {
          "User": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/user/${row.original.EmailId}`, // Example for User, assuming Email is unique
          "Promotional Offer": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/promotionaloffer/${row.original.PromotionalOfferId}`, // Example for Promotional Offer, assuming Id is unique
          "Supplier": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/supplier/${row.original.SupplierId}`, // Example for Supplier, assuming SupplierId is unique
          "Category": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/category/${row.original.CategoryId}`, // Example for Category
          "Product": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/product/${row.original.ProductId}`, // Example for Product
          "Inventory": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/inventory/${row.original.InventoryId}`, // Example for Inventory
        };

        const url = apiEndpoints[schema];
        if (!url) {
          alert("No delete API defined for this schema");
          return;
        }

        const response = await fetch(url, {
          method: "DELETE",
        });

        if (!response.ok) {
          throw new Error("Failed to delete the item");
        }

        fetchData(schema);
        alert(`${schema} row deleted successfully`);
      } catch (error) {
        console.error("Error deleting item:", error);
        alert("An error occurred while deleting the item");
      }
    }
  };

  const fetchData = async (schema) => {
    const apiEndpoints = {
      User: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/user',
      "Promotional Offer": 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/promotionaloffer',
      Supplier: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/supplier',
      Category: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/category',
      Product: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/product',
      Inventory: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/inventory',
      // Order: 'https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/order',
    };
  
    try {
      const url = apiEndpoints[schema];
      if (!url) {
        console.error(`No API endpoint defined for schema: ${schema}`);
        return;
      }
  
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      setData(result.data);
      console.log(`${schema} data fetched successfully:`, result.data);
    } catch (error) {
      console.error(`Error fetching ${schema} data:`, error);
    }
  };

  useEffect(()=>{
    
    fetchData();
  }, [data])

  return (
    <MaterialReactTable
    enableStickyHeader
    muiTableContainerProps={{ sx: { maxHeight: '550px' } }}
      title="Data Table"
      columns={columns}
      data={data}
      enableEditing
      editDisplayMode="modal"
      onEditingRowSave={handleSaveRow}
    />
  );
};

export default DataTable;
