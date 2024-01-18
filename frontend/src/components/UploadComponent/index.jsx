import React, { useContext } from 'react';

import styles from './styles.module.css';

import AuthContext from '../../context/AuthContext';

const UploadComponent = ({ selectedFile, setSelectedFile }) => {

  const { authTokens } = useContext(AuthContext);

  const handleFileChange = (event) => {
    // Atualiza o estado com o arquivo selecionado
    setSelectedFile(event.target.files[0]);
    console.log("Arquivo selecionado!");
  };

  return (
    <>
      <label htmlFor="fileUpload">
        {
          selectedFile 
          ? `Base de dados: ${selectedFile.name}`
          : "Escolha sua base de dados"
        }
      </label>
      <input 
        id='fileUpload'
        type="file"
        accept=".txt"
        onChange={handleFileChange}
        className={styles.fileInput} 
      />
      <button 
        onClick={() => document.getElementById('fileUpload').click()}
        className={styles.uploadContainer}
      >
        Escolher arquivo (CSV, TXT)
      </button>
    </>
  );
};

export default UploadComponent;
