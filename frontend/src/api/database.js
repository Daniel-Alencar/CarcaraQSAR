
// Envia Base de dados para o backend
export const sendDatabase = async (projectID, selectedFile, accessToken) => {

  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('project_id', projectID);

  let response = await fetch(
    `${import.meta.env.VITE_REACT_APP_BACKEND_LINK}/database/send`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + String(accessToken)
      },
      body: formData,
  })

  let dataResponse = await response.json();
  if(response.status == 200) {

    console.log(dataResponse);
    
  } else {
    console.log(`Status: ${response.status}`);
    alert('Erro interno do servidor!');
  }
}