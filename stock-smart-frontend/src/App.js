import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [helloMessage, setHelloMessage] = useState('');
  const [worldMessage, setWorldMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/hello')
      .then(response => {
        setHelloMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the 'hello' message!", error);
      });

    axios.get('http://127.0.0.1:8000/world')
      .then(response => {
        setWorldMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the 'world' message!", error);
      });
  }, []);

  return (
    <div>
      <h1>React App</h1>
      <p>{helloMessage}</p>
      <p>{worldMessage}</p>
    </div>
  );
}

export default App;
