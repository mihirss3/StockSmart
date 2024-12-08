import React, {useEffect, useState} from 'react';
import './InventoryAnalysis.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const InventoryAnalysis = () => {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Sample data for testing
  const sampleData = {
    "Graph 1": [
      { "Product Name": "Soup - Knorr, Chicken Noodle", "Quantity": 131.0 },
      { "Product Name": "Cheese - St. Andre", "Quantity": 24.0 },
      { "Product Name": "Club Soda - Schweppes, 355 Ml", "Quantity": 32.0 },
      { "Product Name": "Shrimp - 16/20, Peeled Deviened", "Quantity": 101.0 },
      { "Product Name": "Cracker - Cheddar", "Quantity": 80.0 },
      {
        "Product Name": "Beef - Striploin",
        "Quantity": 3.0
    },
    {
        "Product Name": "Wine - Fino Tio Pepe Gonzalez",
        "Quantity": 65.0
    },
    {
        "Product Name": "Tea - Orange Pekoe",
        "Quantity": 11.0
    },
    {
        "Product Name": "Cucumber - Pickling",
        "Quantity": 16.0
    },
    {
        "Product Name": "Water - Spring Water 500ml",
        "Quantity": 39.0
    },
    {
        "Product Name": "Cape Capensis - Fillet",
        "Quantity": 55.0
    },
    {
        "Product Name": "Pastry - Trippleberry Muffin - Mini",
        "Quantity": 30.0
    },
    {
        "Product Name": "Wine - Redchard Merritt",
        "Quantity": 53.0
    },
    {
        "Product Name": "Onions - Spanish",
        "Quantity": 4.0
    },
    {
        "Product Name": "Cheese - Pont Couvert",
        "Quantity": 70.0
    },
    {
        "Product Name": "Ice Cream Bar - Super",
        "Quantity": 49.0
    },
    {
        "Product Name": "Potatoes - Peeled",
        "Quantity": 10.0
    },

      { "Product Name": "Oil - Hazelnut", "Quantity": 95.0 }
    ]
  };

  useEffect(() => {
    // Fetch data from the backend
    // const fetchExpiringProducts = async () => {
    //   try {
    //     const response = await fetch("http://localhost:8000/administrator/administer/inventory"); // API endpoint
    //     if (!response.ok) {
    //       throw new Error("Failed to fetch data");
    //     }
    //     const data = await response.json();
    //     console.log(data.data)
    //     setProducts(data.data); // Set fetched data
    //   } catch (error) {
    //     console.error("Error fetching data:", error);
    //   } finally {
    //     setIsLoading(false);
    //   }
    // };
    // fetchExpiringProducts();
    // Simulate API call with sample data
    setProducts(sampleData["Graph 1"]);
    setIsLoading(false);
  }, []);

  const chartData = {
    labels: products.map(item => item['Product Name']),
    datasets: [{
      label: 'Quantity',
      data: products.map(item => item.Quantity),
      backgroundColor: 'rgba(53, 162, 235, 0.8)',
    }]
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Product Inventory Levels'
      }
    },
    scales: {
      y: {
        min: 0,
        max: 10, // Show 10 items at a time
        ticks: {
          autoSkip: false
        }
      }
    }
  };
  
  // Wrap the Bar component in a scrollable container
  return (
    <div className="inventory-analysis-container">
      <div className="content">
        <main className="main-content">
          {/* Your existing metric cards */}
          {!isLoading && (
            <div style={{ 
              height: '500px', 
              marginTop: '20px',
              overflowY: 'scroll',
              border: '1px solid #eee',
              padding: '10px'
            }}>
              <div style={{ minHeight: '1000px' }}>
                <Bar options={options} data={chartData} />
              </div>
            </div>
          )}
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
                {products.length>0 && Object.keys(products[0]).map((key)=> <th>{key}</th>)}
              </tr>
            </thead>
            <tbody>
              {products?.map((product, index) => (
                <tr key={index}>
                  {Object.keys(product).map((key)=> <td>{product[key]}</td>)}
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