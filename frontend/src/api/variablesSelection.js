
// Salva configurações da seleção de variáveis 
export const setVariablesSettings = async (
  projectID, 
  removeConstantVariables, listOfVariables,
  algorithm, algorithmParameters, 
  rowsToRemoveString,
  accessToken
) => {

  const listOfVariablesString = JSON.stringify(listOfVariables)
  const parametersString = JSON.stringify(algorithmParameters)

  const formData = new FormData();
  formData.append('project_id', projectID);
  formData.append('algorithm', algorithm);
  formData.append('algorithm_parameters', parametersString);
  formData.append('remove_constant_variables', removeConstantVariables);
  formData.append('list_of_variables', listOfVariablesString);
  formData.append('rows_to_remove', rowsToRemoveString);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/set_settings`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    return true;
    
  } else {
    console.log(`Status: ${response.status}`);
    return false;
  }
}

// Resgata configurações da seleção de variáveis
export const getVariablesSettings = async (
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/get_settings?project_id=${projectID}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    
  } else {
    console.log(`Status: ${response.status}`);
  }
  return dataResponse;
}

// Remover linhas do Database
export const removeDatabaseRows = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/remove_rows`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    return true;
    
  } else {
    console.log(`Status: ${response.status}`);
    return false;
  }
}

// Remover variáveis constantes do Database
export const removeDatabaseConstantVariables = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/remove_constant_variables`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    return true;
    
  } else {
    console.log(`Status: ${response.status}`);
    return false;
  }
}

// Remover variáveis do Database
export const removeDatabaseVariables = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/remove_variables`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    return true;
    
  } else {
    console.log(`Status: ${response.status}`);
    return false;
  }
}

// Faz a seleção de variáveis com o algoritmo bioinspirado
export const makeSelection = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/make_selection`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    return true;
    
  } else {
    console.log(`Status: ${response.status}`);
    return false;
  }
}