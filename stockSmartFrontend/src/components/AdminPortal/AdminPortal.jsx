import React, { useState, useEffect } from "react";
import "./AdminPortal.css";
import Sidebar from "../Sidebar/Sidebar";
import DataTable from "../DataTable/DataTable";
import Modal from "../Modal/Modal";

const AdminPortal = () => {
  const [selectedSchema, setSelectedSchema] = useState("Category");
  const [data, setData] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");
  const [showModal, setShowModal] = useState(false); // State to manage modal visibility
  const [formData, setFormData] = useState({});
  const [fieldSuggestions, setFieldSuggestions] = useState([]);
  const [loading, setLoading]= useState(true);

  const schemaFields = {
    Category: ["Name", "LeadTime (yyyy-mm-dd)", "StorageRequirements"],
    Product: ["Name", "PackagingType", "Weight", "CategoryId", "SupplierId"],
    Inventory: ["StockDate (yyyy-mm-dd)", "ProductId", "UnitPrice", "ManufactureDate (yyyy-mm-dd)", "ExpiryDate (yyyy-mm-dd)", "Quantity"],
    Supplier: ["Name", "Address", "Contact"],
    "Promotional Offer": ["StartDate (yyyy-mm-dd)", "EndDate (yyyy-mm-dd)", "DiscountRate"],
    User: ["EmailId", "Password", "Type", "FirstName", "LastName", "PhoneNumber"],
    // Order: ["OrderDate (yyyy-mm-dd)", "Inventories"],  // Updated for Order
  };

  const fieldDefaults = {
    Category: { Name: "", "LeadTime (yyyy-mm-dd)": "", StorageRequirements: "" },
    Product: { Name: "", PackagingType: "", Weight: "", CategoryId: "", SupplierId: "" },
    Inventory: { "StockDate (yyyy-mm-dd)": "", ProductId: "", UnitPrice: "", "ManufactureDate (yyyy-mm-dd)": "", "ExpiryDate (yyyy-mm-dd)": "", Quantity: "" },
    Supplier: { Name: "", Address: "", Contact: "" },
    "Promotional Offer": { "StartDate (yyyy-mm-dd)": "", "EndDate (yyyy-mm-dd)": "", DiscountRate: ""},
    User: { EmailId: "", Password: "", Type: "", FirstName: "", LastName: "", PhoneNumber: "" },
    // Order: { "OrderDate (yyyy-mm-dd)": "", Inventories: [] },  // Order format with Inventories
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
      setLoading(false);
      console.log(`${schema} data fetched successfully:`, result.data);
    } catch (error) {
      console.error(`Error fetching ${schema} data:`, error);
    }
  };
  

  useEffect(() => {
    fetchData(selectedSchema);
    setFormData(fieldDefaults[selectedSchema] || {}); // Ensure formData is correctly set based on schema
    setFieldSuggestions(schemaFields[selectedSchema] || []);
  }, [selectedSchema]);

  const handleAdd = async (formData) => {
    const apiEndpoints = {
      "User": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/user`,
      "Promotional Offer": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/promotionaloffer`,
      "Supplier": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/supplier`,
      "Category": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/category`,
      "Product": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/product`,
      "Inventory": `https://smart-stock-backend-1044918252759.us-central1.run.app/administrator/administer/inventory`,
    };
  
    const endpoint = apiEndpoints[selectedSchema]; // Use selectedSchema to determine the schema
  
    if (!endpoint) {
      console.error(`No API endpoint defined for schema: ${selectedSchema}`);
      alert("Add operation failed: Unknown schema");
      return;
    }
  
    // Construct the body for the POST request
    let body = {};
switch (selectedSchema) {
  case "User":
    body = {
      EmailId: formData["EmailId"],
      Password: formData["Password"],
      Type: formData["Type"],
      FirstName: formData["FirstName"],
      LastName: formData["LastName"],
      PhoneNumber: formData["PhoneNumber"],
    };
    break;
  case "Promotional Offer":
    body = {
      StartDate: formData["StartDate (yyyy-mm-dd)"],
      EndDate: formData["EndDate (yyyy-mm-dd)"],
      DiscountRate: parseFloat(formData["DiscountRate"]),
    };
    break;
  case "Supplier":
    body = {
      Name: formData["Name"],
      Address: formData["Address"],
      Contact: formData["Contact"],
    };
    break;
  case "Category":
    body = {
      Name: formData["Name"],
      LeadTime: formData["LeadTime (yyyy-mm-dd)"],
      StorageRequirements: formData["StorageRequirements"],
    };
    break;
  case "Product":
    body = {
      Name: formData["Name"],
      PackagingType: formData["PackagingType"],
      Weight: parseFloat(formData["Weight"]),
      CategoryId: parseInt(formData["CategoryId"], 10),
      SupplierId: parseInt(formData["SupplierId"], 10),
    };
    break;
  case "Inventory":
    body = {
      StockDate: formData["StockDate (yyyy-mm-dd)"],
      ProductId: parseInt(formData["ProductId"], 10),
      UnitPrice: parseFloat(formData["UnitPrice"]),
      ManufactureDate: formData["ManufactureDate (yyyy-mm-dd)"],
      ExpiryDate: formData["ExpiryDate (yyyy-mm-dd)"],
      Quantity: parseInt(formData["Quantity"], 10),
    };
    break;
  default:
    console.error(`Unknown schema: ${selectedSchema}`);
    alert("Add operation failed: Unknown schema");
    return;
}

    console.log("body", JSON.stringify(body))

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });
  
      if (!response.ok) {
        throw new Error(`Failed to add ${selectedSchema}. Status: ${response.status}`);
      }
  
      const newRow = await response.json();
      console.log("newRow", newRow)
  
      fetchData(selectedSchema);
  
      alert(`${selectedSchema} added successfully`);
      setShowModal(false); // Close the modal after success
    } catch (error) {
      console.error("Error adding row:", error);
      alert(`An error occurred while adding ${selectedSchema}`);
    }
  };
  

  return (
    <div className="admin-portal">
      <Sidebar
        schemas={["Category", "Product", "Inventory", "Supplier", "Promotional Offer", "User"]}
        setSelectedSchema={setSelectedSchema}
      />
      <div className="main-content">
        <div className="portal-header">
        <h4 style={{color: 'rgb(23, 41, 53)'}}>Welcome to Admin Portal!</h4>
        <h1 >{selectedSchema}</h1>
        <button
          className="add-button"
          onClick={() => setShowModal(true)} // Open modal when clicked
        >
          Add New {selectedSchema}
        </button>
        </div>
        {!loading &&
        <DataTable
          data={data}
          setData={setData}
          schema={selectedSchema}
        />
}
        {showModal && (
          <Modal
            isOpen={showModal} // Use the isOpen prop
            onClose={() => setShowModal(false)} // Close modal function
            schema={selectedSchema}
            formData={formData} // Pass the form data
            onSubmit={handleAdd} // Pass the onSubmit handler
          />
        )}
      </div>
    </div>
  );
};

export default AdminPortal;
