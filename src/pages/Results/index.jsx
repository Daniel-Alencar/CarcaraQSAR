import { useLocation } from 'react-router-dom';

import { Header } from '../../components/Header';
import { ProgressBar } from '../../components/ProgressBar';
import { Graph } from '../../components/Graph';
import Button from '../../components/Button';
import { Tabs } from '../../components/Tabs';

import styles from './styles.module.css';

import { userName, statesProgressBar, projectName } from '../../settings';

import Graph1 from '../../assets/results/graph1.png';
import Graph2 from '../../assets/results/graph2.png';
import Graph3 from '../../assets/results/graph3.png';
import Graph4 from '../../assets/results/graph4.png';
import Graph5 from '../../assets/results/graph5.png';

import Graph6 from '../../assets/results/graph1.png';
import Graph7 from '../../assets/results/graph2.png';
import Graph8 from '../../assets/results/graph3.png';
import Graph9 from '../../assets/results/graph4.png';
import Graph10 from '../../assets/results/graph5.png';

import { DownloadSimple } from '@phosphor-icons/react';
import { useState } from 'react';

const graphsWithoutExternalSet = [Graph1, Graph2, Graph3, Graph4, Graph5];
const graphsWithExternalSet = [Graph6, Graph7, Graph8, Graph9, Graph10];

const graphs = [
  graphsWithoutExternalSet,
  graphsWithExternalSet
];

export default function Results() {

  const href = '/results';
  const progress = 4;

  const tabsNames = ["Sem conjunto externo", "Com conjunto externo"];

  const location = useLocation();
  const state = location.state;

  let pageNumber = 0;
  if(state) {
    if(state.pageNumber) {
      pageNumber = state.pageNumber;
    }
  }

  const [selectedTab, setSelectedTab] = useState(0);

  const downloadGraph = () => {};

  return(
    <>
      <Header 
        title={projectName}
        userName={userName}
      />
      <ProgressBar 
        progressNumber={progress}
        subProgressNumber={pageNumber}
      />

      <div className={styles.container}>

        <Tabs 
          tabs={tabsNames} 
          selectedTab={selectedTab}
          setSelectedTab={setSelectedTab}
        />

        <div className={styles.graphContainer}>
          <Graph 
            width={550}
            image={graphs[selectedTab][pageNumber]}
          />
          <button 
            className={styles.downloadButton}
            onClick={downloadGraph}
          >
            <DownloadSimple size={30} color='var(--black-color-1)' />
          </button>
        </div>

      </div>

      {
        statesProgressBar[progress].childs.length > (pageNumber + 1)
        ?
          <Button 
            name={'Próximo'} 
            URL={'/results'}
            stateToPass={{
              pageNumber: pageNumber + 1
            }}
          />
        :
          <Button 
            name={'Próximo'} 
            URL={'/outliers'}
          />
      }
    </>
  )
}