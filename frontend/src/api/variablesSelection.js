
// Salva configurações da seleção de variáveis 
export const setVariablesSettings = async (
  projectID, 
  removeConstantVariables, listOfVariables,
  algorithm, algorithmParameters, 
  model, modelParameters,
  rowsToRemoveString,
  accessToken
) => {

  console.log("MODEL");
  console.log(modelParameters);
  console.log("ALGORITMO");
  console.log(algorithmParameters);

  const listOfVariablesString = JSON.stringify(listOfVariables);
  const algorithmParametersString = JSON.stringify(algorithmParameters);
  const modelParametersString = JSON.stringify(modelParameters);

  const formData = new FormData();
  formData.append('project_id', projectID);
  formData.append('algorithm', algorithm);
  formData.append('algorithm_parameters', algorithmParametersString);
  formData.append('model', model);
  formData.append('model_parameters', modelParametersString);
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
    return true;
  } else {
    return false;
  }
}

// Resgata configurações da seleção de variáveis
export const getVariablesSettings = async (
  projectID, accessToken
) => {

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/get_settings?project_id=${projectID}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
  })

  let dataResponse = await response.json();
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
    return true;
  } else {
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
    return true;
  } else {
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
    return true;
  } else {
    return false;
  }
}

// Faz a seleção de variáveis com o algoritmo
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
  return response;
}

// Cancela a seleção de variáveis com o algoritmo
export const cancelSelection = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/cancel_selection`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Verifica o status da seleção de variáveis com o algoritmo
export const checkSelectionStatus = async(
  projectID, accessToken
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/status_selection`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Resgatar o progresso na seleção de variáveis através do algoritmo
export const getSelectionProgress = async(
  projectID, accessToken
) => {

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/get_selection_progress?project_id=${projectID}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Seta o progresso na seleção de variáveis
export const setSelectionProgress = async(
  projectID, accessToken, progressValue, maximumValue
) => {

  const formData = new FormData();
  formData.append('project_id', projectID);
  formData.append('progress_value', progressValue);
  formData.append('maximum_value', maximumValue);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/variables-selection/set_selection_progress`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  return dataResponse;
}