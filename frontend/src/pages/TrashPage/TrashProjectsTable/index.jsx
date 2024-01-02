import { useEffect, useState } from 'react';

import styles from './styles.module.css';

import { TrashSimple } from "@phosphor-icons/react";
import { useNavigate } from 'react-router-dom';

import { projects } from '../../../settings';

export function TrashProjectsTable() {

  const [data, setData] = useState([]);

  const searchProjects = async () => {

    let response = await fetch(
      `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/deactivated_projects/`, {
        method: 'GET',
        headers: {
          'Content-type': 'application/json',
        }
    })

    let data = await response.json();
    if(response.status == 200) {

      console.log(data);
      setData(data);

    } else {
      alert('Erro interno do servidor!');
    }
  }

  useEffect(() => {
    searchProjects();
  }, []);

  const navigate = useNavigate();
  const handleTo = (URL) => {
    navigate(URL);
  };

  // Estado do checkbox geral da tabela
  const [isCheked, setIsChecked] = useState(false);
  useEffect(() => {
    selectAllData();
  }, [isCheked]);


  // Funções de controle
  const toggleSelected = (id) => {
    setData(
      data.map((item) =>
        item.id === id ? { ...item, selecionado: !item.selecionado } : item
      )
    );
  };

  const removeItem = async (index) => {
    
    const projectID = data[index].id;
    
    data.splice(index, 1);
    setData([...data]);

    let response = await fetch(
      `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/delete_project/${projectID}`, {
        method: 'DELETE',
        headers: {
          'Content-type': 'application/json',
        },
        body: JSON.stringify({})
    })

    let dataResponse = await response.json();
    if(response.status == 200) {
      console.log(dataResponse);
    } else {
      console.log(`Status: ${response.status}`);
    }
  };

  const removeSelectedItens = async () => {
    let newData = data.filter((dado) => {
      return !dado.selecionado;
    });

    setData(newData)
  };

  const selectAllData = () => {
    let newData = [];

    if(isCheked) {
      newData = data.map((dado) => {
        dado.selecionado = true;
        return dado;
      });
    } else {
      newData = data.map((dado) => {
        dado.selecionado = false;
        return dado;
      });
    }

    setData(newData);
  };

  return (
    <>
      <table className={styles.table}>
        <thead className={styles.header}>
          <tr className={styles.descriptionHeader}>
            <th className={`${styles.descriptionItem} ${styles.item1}`}>
              <input
                type="checkbox"
                className={styles.checkbox}
                onClick={() => setIsChecked(!isCheked)}
              />
            </th>
            <th className={`${styles.descriptionItem} ${styles.item2}`}>Nome</th>
            <th className={`${styles.descriptionItem} ${styles.item3}`}>Status</th>
            <th className={`${styles.descriptionItem} ${styles.item4}`}>
              Data de modificação
            </th>
            <th className={`${styles.descriptionItem} ${styles.item5}`}>
              <a 
                className={styles.removeButton}
                onClick={() => removeSelectedItens()}
              >
                <TrashSimple size={20} />
              </a>  
            </th>
          </tr>
        </thead>

        <tbody className={styles.body}>
          {
            data.map((item, index) => (
              <tr key={item.id} className={styles.descriptionBody}>
                <td className={`${styles.item} ${styles.checkboxContainer}`}>
                  <input
                    type="checkbox"
                    checked={item.selecionado}
                    onChange={() => toggleSelected(item.id)}
                  />
                </td>
                <td 
                  className={`${styles.item} ${styles.name}`}
                  onClick={() => handleTo('/database')}
                >
                  {item.nome}
                </td>
                <td className={styles.item}>{item.status}</td>
                <td className={styles.item}>{item.date}</td>
                <td className={styles.item}>
                  <a 
                    className={styles.removeButton}
                    onClick={() => removeItem(index)}
                  >
                    <TrashSimple size={20} />
                  </a>  
                </td>
              </tr>
            ))
          }
        </tbody>
      </table>
    </>
  )
}
