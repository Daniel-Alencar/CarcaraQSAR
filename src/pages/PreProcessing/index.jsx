import { useState } from 'react';
import { DefaultPage } from '../DefaultPage';
import { UserBar } from '../../components/UserBar';

import { ProgressBar } from '../../components/ProgressBar';
import { statesProgressBar, userName } from '../../settings';

import { DataTable } from '../../components/DataTable';

import Histograma from '../../assets/histograma.png';
import BoxPlot from '../../assets/box-plot.png';

import { Graph } from '../../components/Graph';
import { RadionInput } from '../../components/RadioInput';

import styles from './styles.module.css';

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

  const href = '/pre-processing';
  const progress = 1;

  const [option, setOption] = useState(options[0]);

  if(true) {
    return(
      <>
        <UserBar name={userName} />
        <ProgressBar progressNumber={progress}/>

        <div className={styles.container}>
          <DataTable vertical={true} onlyTitles/>

          <div className={styles.graphsContainer}>

            <Graph name={"Histograma"} image={Histograma}/>
            <Graph name={"Box-Plot"} image={BoxPlot}/>

          </div>

        </div>
      </>
    )  
  } else {
    return(
      <>
        <UserBar name={userName} />
        <ProgressBar progressNumber={progress}/>

        <div className={styles.container}>

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
      </>
    )
  }
}