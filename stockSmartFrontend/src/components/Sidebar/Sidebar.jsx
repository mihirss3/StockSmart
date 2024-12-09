import React, {useEffect, useState} from "react";
import "./Sidebar.css";

const Sidebar = ({ schemas, setSelectedSchema }) => {
  const [selectedItem, setSelectedItem] = useState("Category");

  // Set the default selected item when the component loads
  useEffect(() => {
    setSelectedSchema(selectedItem); // Send the default selected schema to the parent
  }, [selectedItem, setSelectedSchema]);

  return (
    <div className="sidebar">
      <div className="schemaHeading">
      <h2 >Schemas</h2>
      </div>
      <ul>
        {schemas.map((schema) => (
           <li
           className={`schemaName ${schema === selectedItem ? "selected" : ""}`}
           key={schema}
           onClick={() => {
             setSelectedItem(schema);
             setSelectedSchema(schema); // Pass selected schema to parent
           }}
         >
            {schema}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
