import React, { useState, useEffect } from 'react';
import './Modal.css';

const Modal = ({ isOpen, onClose, schema, formData, onSubmit }) => {
  const [localFormData, setLocalFormData] = useState(formData);

  useEffect(() => {
    if (formData) {
      setLocalFormData(formData); // Only update if formData is defined
    }
  }, [formData, schema]);

  const handleChange = (e, field, index) => {
    const value = e.target.value;
    setLocalFormData((prevData) => {
      return { ...prevData, [field]: value };
    });
  };

  const handleSubmit = () => {
    console.log('localFormData', localFormData)
    onSubmit(localFormData);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Add {schema}</h2>
        <form>
          {Object.keys(localFormData).map((field, index) => {
    
            return (
              <div key={index} className="form-group">
                {console.log(field)}
             <label>{field}</label>
              <input
                  type="text"
                  value={localFormData[field]}
                  onChange={(e) => handleChange(e, field)}
                  placeholder={field}
                />
              </div>
            );
          })}
          <button type="button" className="submit-button" onClick={handleSubmit}>
            Add
          </button>
          <button type="button" className="close-button" onClick={onClose}>
            Close
          </button>
        </form>
      </div>
    </div>
  );
};

export default Modal;
