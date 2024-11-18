import React, {useEffect, useState} from 'react';
import './InventoryAnalysis.css';
import Sidebar from '../Sidebar/Sidebar'

const InventoryAnalysis = () => {

  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch data from the backend
    const fetchExpiringProducts = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/top15ProductsExpiringSoon"); // API endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        setProducts(data); // Set fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchExpiringProducts();
  }, []);

  return (
    <div className="inventory-analysis-container">
        {/* <Sidebar /> */}
      <div className="content">
        <main className="main-content">
          <h2 className="main-title">Current Inventory Analysis</h2>
          <div className="metric-cards">
            <div className="metric-card purple">
              <h3>30,000</h3>
              <p>Total items</p>
              <span className="growth">⬆ 12%</span>
            </div>
            <div className="metric-card blue">
              <h3>270</h3>
              <p>Total orders</p>
              <span className="growth">⬆ 12%</span>
            </div>
            <div className="metric-card orange">
              <h3>1,000</h3>
              <p>Today's revenue</p>
              <span className="growth">⬆ 12%</span>
            </div>
          </div>
        </main>
      </div>
      <div style={{ padding: "20px" }} className='queryTable'>
     <h2>Products Expiring Soon</h2>
     {isLoading ? (
       <p>Loading...</p>
     ) : (
       <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
         <thead>
           <tr>
           <th>Serial No.</th>
             <th>Product Name</th>
             <th>Expiry Date</th>
             <th>Supplier Name</th>
             <th>Quantity to Replace</th>
           </tr>
         </thead>
         <tbody>
           {products.map((product, index) => (
             <tr key={index}>
              <td>{index+1}</td>

               <td>{product.ProductName}</td>
               <td>{product.ExpiryDate}</td>
               <td>{product.SupplierName}</td>
               <td>{product.QuantityOfProductsGettingExpired}</td>
             </tr>
           ))}
         </tbody>
       </table>
     )}
      </div>
     
    </div>
 
  );
};

export default InventoryAnalysis;
