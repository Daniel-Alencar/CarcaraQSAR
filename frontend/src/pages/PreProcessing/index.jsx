import { useContext, useEffect, useState } from 'react';
import { Header } from '../../components/Header';

import { ProgressBar } from '../../components/ProgressBar';

import { Graph } from '../../components/Graph';
import { RadionInput } from '../../components/RadioInput';

import styles from './styles.module.css';

import Button from '../../components/Button';
import { VariablesList } from '../../components/VariablesList';

import { useLocation, useParams } from 'react-router-dom';
import { getBoxPlot, getHistogram, getVariables } from '../../api/database';

import AuthContext from '../../context/AuthContext';
import ProjectContext from '../../context/ProjectContext';

import { InlineInput } from '../../components/InlineInput';

export const options = [
  "MinMaxScaler",
  "StandardScaler",
  "RobustScaler",
  "Normalizer",
  "QuantileTransformer",
  "PowerTransformer",
  "FunctionTransformer",
];

export const optionsDescriptions = [
  "O MinMaxScaler é um método de normalização que dimensiona os dados para um intervalo específico, geralmente entre 0 e 1. Isso é alcançado transformando os valores de tal forma que o valor mínimo se torna 0 e o valor máximo se torna 1, preservando a relação de proporção entre os dados originais.",
  "O StandardScaler é um método de normalização que transforma os dados de tal forma que eles tenham média zero e desvio padrão igual a 1. Isso é útil para dados que seguem uma distribuição normal e ajuda a eliminar o viés de escala nos algoritmos de aprendizado de máquina.",
  "O RobustScaler é uma técnica de normalização que é resistente a outliers. Ele dimensiona os dados, tornando-os robustos a valores discrepantes, usando estatísticas robustas, como a mediana e o intervalo interquartil.",
  "O Normalizer é um método de normalização que ajusta cada amostra de dados individualmente, escalando os valores para que eles tenham norma 1. Isso é útil quando o comprimento das amostras é importante, como em tarefas de processamento de texto ou séries temporais.",
  "O QuantileTransformer é um método de normalização que transforma os dados de forma que a distribuição resultante seja uma distribuição uniforme. Isso é feito por meio de mapeamento dos valores para percentis de uma distribuição de referência, o que é útil para lidar com dados que não seguem uma distribuição normal.",
  "O PowerTransformer é uma técnica de normalização que aplica uma transformação que torna os dados mais semelhantes a uma distribuição normal. Ele inclui duas opções comumente usadas: Box-Cox e Yeo-Johnson, que lidam com diferentes tipos de dados.",
  "O FunctionTransformer é um método de normalização que permite aos usuários aplicar funções personalizadas para transformar seus dados. Isso é útil quando os dados requerem uma transformação não linear específica.",
];

export function PreProcessing({ index }) {

  const { authTokens } = useContext(AuthContext);
  const { projectDetails } = useContext(ProjectContext);
  const { projectID } = useParams();

  const href = '/pre-processing';
  const progress = 1;

  const location = useLocation();
  const state = location.state;

  let pageNumber = 0;
  if(state) {
    if(state.pageNumber) {
      pageNumber = state.pageNumber;
    }
  }

  // Primeira página do Pré-processing
  const [variablesNames, setVariablesNames] = useState([]);
  const [variable, setVariable] = useState("");

  const [histogram, setHistogram] = useState(null);
  const [divisions, setDivisions] = useState(20);
  const [boxPlot, setBoxPlot] = useState(null);

  // Segunda página do Pré-processing
  const [option, setOption] = useState(options[0]);

  const getGraphs = () => {
    // Resgata o Histograma
    getHistogram(projectID, variable, divisions, authTokens.access)
    .then((response) => {
      const histogram = response.imageInBase64;
      // Cria a URL da imagem a partir da string Base64
      const histogramImage = `data:image/png;base64,${histogram}`;
      setHistogram(histogramImage);
    })
    .catch((error) => {
      console.log(error);
    })

    // Resgata o BoxPlot
    getBoxPlot(projectID, variable, authTokens.access)
    .then((response) => {
      const boxPlot = response.imageInBase64;
      // Cria a URL da imagem a partir da string Base64
      const boxPlotImage = `data:image/png;base64,${boxPlot}`;
      setBoxPlot(boxPlotImage);
    })
    .catch((error) => {
      console.log(error);
    })
  }

  const clearGraphs = () => {
    setHistogram(null);
    setBoxPlot(null);
  } 

  const onChangeVariable = (index, variableName) => {
    clearGraphs();
    // Setar variável escolhida
    setVariable(variableName);
    // Recuperar os gráficos
    getGraphs();
  }

  useEffect(() => {
    // Recuperar Database
    getVariables(projectID, authTokens.access)
    .then((response) => {
      if(response.variables) {
        // Salvar nomes das variáveis
        setVariablesNames(response.variables);
      }
    })
    .catch((error) => {
      console.log(error);
    })  
  }, [])

  useEffect(() => {
    // Setar variável escolhida
    setVariable(variablesNames[0]);
  }, [variablesNames])

  useEffect(() => {
    // Recuperar os gráficos
    getGraphs();
  }, [variable])

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

        <div className={styles.firstContainer}>
          <VariablesList
            variablesNames={variablesNames}
            onChangeVariable={onChangeVariable}
          />

          <div className={styles.graphsContainer}>
            {
              histogram &&
              <Graph name={"Histograma"} image={histogram}/>
            }
            {
              boxPlot &&
              <Graph name={"Box-Plot"} image={boxPlot}/>
            }
          </div>

          <div>
            <InlineInput 
              name={"Divisões para o Histograma: "} type={'number'}
              value={divisions}
              setValue={setDivisions}
              width={65}
            />
          </div>

        </div>
        
        <Button 
          name={'Voltar'} 
          URL={`/${projectID}/database`}
          side={'left'}
        />
        <Button 
          name={'Próximo'} 
          URL={`/${projectID}/pre-processing`} 
          stateToPass={{
            pageNumber: 1
          }}
          side={'right'}
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

        <div className={styles.secondContainer}>

          <RadionInput 
            name={"Normalização dos dados"}
            options={options} 
            setOption={setOption}
          />
          <div className={styles.informationContainer}>
            <p className={styles.information}>
              {optionsDescriptions[options.indexOf(option)]}
            </p>
          </div>

        </div>

        <Button 
          name={'Voltar'} 
          URL={`/${projectID}/pre-processing`}
          stateToPass={{
            pageNumber: 0
          }}
          side={'left'}
        />
        <Button 
          name={'Próximo'} 
          URL={`/variables-selection`}
          side={'right'}
        />
      </>
    )
  }
}