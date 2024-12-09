import React, { useEffect, useState } from 'react';
import './InventoryAnalysis.css';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const InventoryAnalysis = () => {
  const [chartOneData, setChartOneData] = useState([]);
  const [chartTwoData, setChartTwoData] = useState([]);
  const [chartThreeData, setChartThreeData] = useState([]);
  const [chartFourData, setChartFourData] = useState([]);
  const [kpiProductsInStock, setkpiProductsInStock] = useState([]);
  const [kpiProductsOutOfStock, setkpiProductsOutOfStock] = useState([]);
  const [kpiProductsOutOfStockSoon, setkpiProductsOutOfStockSoon] = useState([]);
  const [kpiProductsExpiringSoon, setkpiProductsExpiringSoon] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseOne = await fetch('https://smart-stock-backend-1044918252759.us-central1.run.app/analyst/AnalystChartOneView');
        const responseTwo = await fetch('https://smart-stock-backend-1044918252759.us-central1.run.app/analyst/AnalystChartTwoView');
        const responseThree = await fetch('https://smart-stock-backend-1044918252759.us-central1.run.app/analyst/AnalystChartThreeView');
        const responseFour = await fetch('https://smart-stock-backend-1044918252759.us-central1.run.app/analyst/AnalystChartFourView');
        const responseKpi = await fetch('https://smart-stock-backend-1044918252759.us-central1.run.app/analyst/AnalystKPIView');

        const dataOne = await responseOne.json();
        const dataTwo = await responseTwo.json();
        const dataThree = await responseThree.json();
        const dataFour = await responseFour.json();
        const dataKpi = await responseKpi.json();

        setChartOneData(dataOne.data || []);
        setChartTwoData(dataTwo.data || []);
        setChartThreeData(dataThree.data || []);
        setChartFourData(dataFour.data || []);
        setkpiProductsInStock(dataKpi.data.ProductsInStock || []);
        setkpiProductsExpiringSoon(dataKpi.data.ProductsExpiringSoon || []);
        setkpiProductsOutOfStock(dataKpi.data.ProductsOutOfStock || []);
        setkpiProductsOutOfStockSoon(dataKpi.data.ProductsOutOfStockSoon || []);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const filterData = (data, query) => {
    if (!query) return data;
    return data.filter((item) =>
      Object.values(item).some((value) =>
        value?.toString().toLowerCase().includes(query.toLowerCase())
      )
    );
  };

  const generateSuggestions = () => {
    const combinedData = [...chartOneData, ...chartTwoData, ...chartThreeData];
    const uniqueNames = [
      ...new Set(combinedData.map((item) => item['Product Name']?.toLowerCase() || '')),
    ];
    return uniqueNames.filter((name) => name.includes(searchQuery.toLowerCase())).slice(0, 5);
  };

  useEffect(() => {
    if (searchQuery) {
      setSuggestions(generateSuggestions());
    } else {
      setSuggestions([]);
    }
  }, [searchQuery]);

  const filteredChartOneData = filterData(chartOneData, searchQuery);
  const filteredChartTwoData = filterData(chartTwoData, searchQuery);
  const filteredChartThreeData = filterData(chartThreeData, searchQuery);

  const currentStockData = {
    labels: filteredChartOneData?.map((item) => item['Product Name']) || [],
    datasets: [
      {
        label: 'Current Stock',
        data: filteredChartOneData?.map((item) => item.Quantity) || [],
        backgroundColor: 'rgba(53, 162, 235, 0.8)',
        barThickness: 2,
      },
    ],
  };

  const categoryData = {
    labels: filteredChartTwoData?.map((item) => item['Product Name']) || [],
    datasets: [
      {
        label: 'Quantity',
        data: filteredChartTwoData?.map((item) => item.Quantity) || [],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
        ],
      },
    ],
  };

  const expiryData = {
    labels: filteredChartThreeData?.map((item) => item['Product Name']) || [],
    datasets: [
      {
        label: 'Quantity',
        data: filteredChartThreeData?.map((item) => item.Quantity) || [],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  const forecastData = {
    labels: chartFourData?.map((item) => item['ProductName']) || [],
    datasets: [
      {
        label: 'ForecastQuantity',
        data: chartFourData?.map((item) => item.ForecastQuantity) || [],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };
  console.log("Mohit")
  console.log(forecastData)

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: { size: 12 },
        },
      },
      title: { display: true },
    },
    layout: {
      padding: { top: 20, left: 10, right: 10, bottom: 10 },
    },
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y', // Switch axis to make it horizontal
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: { size: 12 },
        },
      },
      title: { display: true, text: 'Current Stock Levels' },
    },
    layout: {
      padding: { top: 20, left: 10, right: 10, bottom: 10 },
    },
    scales: {
      y: { ticks: { autoSkip: false, maxTicksLimit: 20 } },
      x: { ticks: { stepSize: 1 } },
    },
  };

  const doughnutOptions = {
    ...options,
    plugins: {
      ...options.plugins,
      title: { display: true, text: 'Top Products' },
    },
  };

  const lineOptions = {
    ...options,
    plugins: {
      ...options.plugins,
      title: { display: true, text: 'Products Near Expiry' },
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
        },
      },
      y: {
        ticks: {
          stepSize: 1,
        },
      },
    },
  };


  const forecastOptions = {
    ...options,
    plugins: {
      ...options.plugins,
      title: { display: true, text: 'Product Forecast' },
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
        },
      },
      y: {
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="inventory-analysis-container">
      <div className="content">
        <main className="main-content main-inventory-content">
          <h2 className="main-title">Current Inventory Analysis</h2>
          {/* Search Bar */}
          <div className="metric-cards">
            <div className="metric-card red">
              <h3>{kpiProductsOutOfStock}</h3>
              <p>Products Out Of Stock</p>
            </div>
            <div className="metric-card red">
              <h3>{kpiProductsOutOfStockSoon}</h3>
              <p>Products Running Out Of Stock Soon</p>
            </div>
            <div className="metric-card red">
              <h3>{kpiProductsExpiringSoon}</h3>
              <p>Products Expiring Soon</p>
            </div>
            <div className="metric-card purple">
              <h3>{kpiProductsInStock}</h3>
              <p>Products In Stock</p>
            </div>
        </div>

          <div className="search-container" style={{paddingTop: "50px", paddingBottom: "30px"}}>
            <input
              type="text"
              className="search-input"
              placeholder="Search for products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {suggestions.length > 0 && (
              <ul className="suggestions-list">
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    className="suggestion-item"
                    onClick={() => setSearchQuery(suggestion)}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            )}
          </div>



          {isLoading ? (
            'Loading...'
          ) : (
            <div className="charts-grid">
              <div className="chart-container">
                    <div style={{ height: '800px', /* width: "200px", */ overflowY: 'scroll', padding: '10px' }}>
                        <Bar options={barOptions} data={currentStockData} />
                    </div>
              </div>

              <div className="chart-container">
                <div style={{ height: '800px', padding: '10px' }}>
                  <Doughnut options={doughnutOptions} data={categoryData} />
                </div>
              </div>

              <div className="chart-container">
                <div style={{ height: '800px', padding: '10px' }}>
                  <Line options={lineOptions} data={expiryData} />
                </div>
              </div>

              <div className="chart-container">
                <div style={{ height: '800px', padding: '10px' }}>
                  <Line options={forecastOptions} data={forecastData} />
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default InventoryAnalysis;