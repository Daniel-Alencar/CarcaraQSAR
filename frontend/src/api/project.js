
// Cria projeto
export const createProject = async (e, accessToken) => {
  e.preventDefault();

  const name = e.target.name.value;
  const description = e.target.description.value;

  if(name == "" || description == "") {
    return alert("Preencha os campos corretamente!")
  }

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/new/`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({
        project_name: name,
        project_description: description
      })
  })

  let dataResponse = await response.json();
  if(response.status == 200) {
    window.location.href = '/home';
  } else {
    alert('Erro interno do servidor!');
  }
}

// Retorna projetos ativados
export const searchProjects = async (searchValue, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/projects?query=${searchValue}`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      }
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Retorna projetos compartilhados
export const searchSharedProjects = async (searchValue, accessToken) => {

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/shared_projects?query=${searchValue}`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      }
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Retorna projetos desativados
export const searchDeactivatedProjects = async (searchValue, accessToken) => {

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/deactivated_projects?query=${searchValue}`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      }
  })

  let dataResponse = await response.json();
  return dataResponse;
}

// Ativa projeto
export const activateProject = async (projectID, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/activate_project/${projectID}`, {
      method: 'PUT',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({})
  })

  let dataResponse = await response.json();
}

// Desativa projeto
export const deactivateProject = async (projectID, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/deactivate_project/${projectID}`, {
      method: 'PUT',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({})
  })

  let dataResponse = await response.json();
}

// Compartilha projeto
export const shareProject = async (projectID, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/share_project/${projectID}`, {
      method: 'PUT',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({})
  })

  let dataResponse = await response.json();
}

// Descompartilha projeto
export const deshareProject = async (projectID, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/deshare_project/${projectID}`, {
      method: 'PUT',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({})
  })

  let dataResponse = await response.json();
}

// Remove projeto
export const removeProject = async (projectID, accessToken) => {
  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/delete_project/${projectID}`, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: JSON.stringify({})
  })

  let dataResponse = await response.json();
}

// Retorna projeto específico
export const getProject = async (projectID, accessToken) => {

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project?project_id=${projectID}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
  })

  let dataResponse = await response.json();
  if(response.status == 200) {
  } else {
    alert('Erro interno do servidor!');
  }
  return dataResponse;
}

// Atualizar status
export const updateStatus = async (projectID, accessToken, newStatus) => {

  const formData = new FormData();
  formData.append('project_id', projectID);
  formData.append('new_status', newStatus);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/project/update_status`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken),
      },
      body: formData,
  })

  let dataResponse = await response.json();
}