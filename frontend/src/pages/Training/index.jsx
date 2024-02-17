import { ProgressBar } from '../../components/ProgressBar';
import { Header } from '../../components/Header';

import styles from './styles.module.css';

import { projectName } from '../../settings';
import { RadionInput } from '../../components/RadioInput';
import { useContext, useEffect, useState } from 'react';
import { InlineInput } from '../../components/InlineInput';
import Button from '../../components/Button';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import ProjectContext from '../../context/ProjectContext';

import PopUp from '../../components/PopUp';

import { 
  getTrainingSettings, setTrainingSettings, train 
} from '../../api/training';

import Loading from '../../components/Loading';
import { CheckboxInput } from '../../components/CheckboxInput';

export const algorithms = [
  "Random Forest",
  "Regressão linear",
  "KNN",
  "Support Vector Machines (SVM)",
];

export const algorithmsDescriptions = [
  "O algoritmo Random Forest é um método de aprendizado de máquina que combina múltiplas árvores de decisão para tomar decisões mais precisas e estáveis. Ele funciona criando um conjunto de árvores de decisão, cada uma treinada em uma amostra aleatória dos dados e usando diferentes conjuntos de recursos. Ao fazer previsões, as árvores votam em conjunto, e a classe ou valor com mais votos é escolhido como a previsão final. Isso reduz a tendência de overfitting e melhora a robustez do modelo.",
  "A regressão linear é um algoritmo de aprendizado de máquina supervisionado usado para modelar a relação entre uma variável independente (ou mais) e uma variável dependente, geralmente de natureza contínua. Ele assume que a relação entre as variáveis pode ser representada por uma linha reta, daí o termo 'linear'. O objetivo é encontrar os coeficientes que melhor ajustam essa linha aos dados, de modo a minimizar a diferença entre as previsões do modelo e os valores reais.",
  "O algoritmo KNN (K-Nearest Neighbors) é uma técnica simples e poderosa no campo da aprendizagem de máquina. Sua simplicidade é uma de suas principais vantagens, tornando-o fácil de entender e implementar. Ele opera no princípio de 'vizinhos mais próximos', onde as decisões são baseadas na proximidade dos pontos de dados no espaço de características.",
  "As Máquinas de Vetores de Suporte são algoritmos de aprendizado de máquina que são usados tanto em tarefas de classificação quanto de regressão. O SVM busca encontrar um hiperplano que melhor separa as classes em um espaço multidimensional, maximizando a margem entre as classes. Isso torna o SVM eficaz na classificação de dados não lineares e na manipulação de dados com dimensionalidade elevada. Além disso, os SVMs podem fazer uso de truques de kernel para transformar dados em espaços de características mais complexos e, assim, abordar problemas de classificação mais desafiadores."
]

export const algorithmsParameters = [
  [["n_estimators", "Número de árvores"], ["max_features", "Quantidade de features"]],
  [["regularization", "Regularização"]],
  [["k_neighbors", "K vizinhos mais próximos"]],
  [["kernel", "Kernel"], ["CParameter", "Parâmetro C"]],
];

export default function Training() {

  const { authTokens } = useContext(AuthContext);
  const { projectDetails } = useContext(ProjectContext);
  const { projectID } = useParams();

  const navigate = useNavigate();

  const href = '/training';
  const progress = 3;

  const location = useLocation();
  const state = location.state;

  let pageNumber = 0;
  if(state) {
    if(state.pageNumber) {
      pageNumber = state.pageNumber;
    }
  }

  const [choosenAlgorithm, setChoosenAlgorithm] = useState(algorithms[0]);
  const [algorithmParameters, setAlgorithmParameters] = useState({});
  const [withFullSet, setWithFullSet] = useState(false);
  
  const [trained, setTrained] = useState(false);
  const [loading, setLoading] = useState(false);

  const changeParameters = (key, value) => {
    let values = algorithmParameters;
    values[key] = value;
    setAlgorithmParameters(values);

    console.log(values);
  }

  const nextButtonAction = async() => {
    const trainingSettings = await getTrainingSettings(projectID, authTokens.access);

    if(
      trainingSettings.algorithm == choosenAlgorithm && 
      trainingSettings.withFullSet == withFullSet
      ) {
      console.log("O algorítmo não mudou");
      console.log("A configuração de conjunto completo não mudou");
      console.log("Não precisa modificar!");
      return true;

    } else {
      console.log("Algo mudou, precisa modificar!");
      const response = await setTrainingSettings(
        projectID, 
        choosenAlgorithm, 
        algorithmParameters,
        withFullSet,
        authTokens.access
      );
      return response;
    }
  }

  const saveAndTrain = async() => {
    setLoading(true);

    const response = await setTrainingSettings(
      projectID, 
      choosenAlgorithm, 
      algorithmParameters,
      withFullSet,
      authTokens.access
    );
    if(response) {
      const response = await train(projectID, authTokens.access);
      setLoading(false);
      setTrained(true);

      return true;
    }
    return false;
  }

  const navigateToResults = () => {
    navigate(`/${projectID}/results`);
  }

  useEffect(() => {
    getTrainingSettings(projectID, authTokens.access)
    .then((response) => {
      console.log(response.algorithm);
      setChoosenAlgorithm(response.algorithm);

      console.log(response.parameters);
      setAlgorithmParameters(response.parameters);

      console.log(response.withFullSet);
      setWithFullSet(response.withFullSet);
    })
    .catch(error => {
      console.log(error);
    })
  }, []);

  if(pageNumber == 0) {
    return(
      <>
        <Header 
          title={projectDetails.name}
        />
        <ProgressBar 
          progressNumber={progress}
          subProgressNumber={pageNumber}
        />

        <div className={styles.container}>

          <div>
            <RadionInput 
              name={"Aplicar algoritmo"}
              options={algorithms}
              setOption={setChoosenAlgorithm}
              firstOption={choosenAlgorithm}
            />
            <CheckboxInput 
              name={"Com conjunto completo?"}
              value={withFullSet} 
              setValue={setWithFullSet}
            />
          </div>
          
          <div className={styles.informationContainer}>
            <p className={styles.information}>
              {algorithmsDescriptions[algorithms.indexOf(choosenAlgorithm)]}
            </p>
          </div>

        </div>

        <Button 
          name={'Voltar'} 
          URL={'/variables-selection'}
          side={'left'}
        />
        <Button 
          name={'Próximo'} 
          URL={'/training'}
          stateToPass={{
            pageNumber: 1
          }}
          side={'right'}
          action={nextButtonAction}
        />
      </>
    )

  } else if(pageNumber == 1) {
    return(
      <>
        <Header
          title={projectDetails.name} 
        />
        <ProgressBar 
          progressNumber={progress}
          subProgressNumber={pageNumber}
        />

        <div className={styles.contentContainer}>
          <div className={styles.leftDiv}>
            <div className={styles.parametersContainer}>
              {
                algorithmsParameters[
                  0
                ].map((key, index) => {
                  return(
                    <InlineInput 
                      key={index}
                      name={key[1]} 
                      type={'number'}
                      setValue={(value) => changeParameters(key[0], value)}
                      value={algorithmParameters[key[0]] ? algorithmParameters[key[0]] : 0}
                    />
                  )
                })
              }
            </div>
            <button 
              onClick={saveAndTrain}
              className={styles.button}
            >
              Salvar e Treinar
            </button>
          </div>
          <div className={styles.rightDiv}>
            {
              loading && <Loading />
            }
          </div>

        </div>

        <PopUp show={trained}
          title={"Treinamento finalizado"}
          description={
            `O treinamento com o algoritmo ${choosenAlgorithm} está finalizado! Clique no botão abaixo para ver os resultados do treinamento!`
          }
          buttonName={"Ver resultados"}
          action={navigateToResults}
        />

        <Button 
          name={'Voltar'} 
          URL={'/training'}
          stateToPass={{
            pageNumber: 0
          }}
          side={'left'}
        />
        {
          trained &&
          <Button 
            name={'Próximo'} 
            URL={'/results'}
            stateToPass={{
              pageNumber: 0
            }}
            side={'right'}
          />
        }
      </>
    )
  }
}