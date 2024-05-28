
import math
import pandas as pd

from variables_selection.algorithms.utils.utils import convert_binary_array_to_variables, convert_variables_to_binary_array, get_variables

from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import StandardScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

class Graph:
    def __init__(self, dataframe, r2_condition):
        self.dataframe = dataframe

        self.r2_condition = r2_condition
        self.graph = {}

    def add_node(self, node):
        self.graph[tuple(node)] = []

    def add_child(self, parent, child):
        self.graph[tuple(parent)].append(child)

    def calculate_R2(self, binary_array, full_variables):
        choosen_variables = convert_binary_array_to_variables(
           binary_array, full_variables
        )
        return self.evaluate_model(choosen_variables)

    def greedy_search(self, start, full_variables):
        visited = set()
        best_node = None
        best_R2 = 0
        i = 0

        frontier = []
        frontier.append((self.calculate_R2(start, full_variables), start))

        while len(frontier) > 0:
            i += 1
            # Ordena a fronteira pelo valor de R2 decrescente
            frontier = sorted(frontier, key=lambda x: x[0], reverse=True)
            for item in frontier:
                print(item[0])

            # Obtém o nó com o maior valor de R2
            current_R2, current_node = frontier.pop(0)

            if tuple(current_node) in visited:
                continue
            visited.add(tuple(current_node))

            print(f"Valor R2 = {current_R2} para o nó atual")

            # Abre o arquivo em modo de escrita ('w')
            with open("Valores R2.csv", "a") as arquivo:
                # Escreve os dados no arquivo
                arquivo.write(f"{i}, {current_R2}, {current_node}\n")
            print("Dados foram salvos no arquivo.")

            # Condição de parada
            if current_R2 >= self.r2_condition:
                print(f"R2 >= {self.r2_condition}. Parando a busca.")
                best_node = current_node
                best_R2 = current_R2
                break
            
            # Atualiza o melhor nó encontrado até agora
            if current_R2 > best_R2:
                best_node = current_node
                best_R2 = current_R2

            childrens = self.generate_children(current_node)

            bests_R2 = []
            for child in childrens:
                bests_R2.append(self.calculate_R2(child, full_variables))
            
            # Obtém os índices dos maiores elementos de bests_R2
            child_quantity = 5

            bests_indexes = sorted(
                range(len(bests_R2)), 
                key=lambda i: bests_R2[i], 
                reverse=True
            )[:child_quantity]

            print(f"Melhores índices: {bests_indexes}")

            for index in bests_indexes:

                print(f"length child {index}: {len(childrens[index])}")
                for i, value in enumerate(childrens[index]):
                    if(value == 1):
                        print(i)

                if (
                    tuple(childrens[index]) not in visited 
                    and bests_R2[index] >= current_R2
                ):
                    frontier.append(
                       (self.calculate_R2(childrens[index], full_variables), childrens[index])
                    )
            
            print(f"Quantidade da barreira: {len(frontier)}")
        return best_node, best_R2

    def generate_children(self, node):
        children = []
        # Adiciona 1 em uma posição diferente do array para gerar os filhos
        for i in range(len(node)):
            if node[i] == 0:
                child = node[:i] + [1] + node[i+1:]
                children.append(child)

        return children
    
    def evaluate_model(self, variables):
  
        X = self.dataframe[variables]
        y = self.dataframe.iloc[:, -1]

        # Normalizar os dados
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Dividir o conjunto de dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Cria um modelo
        if(False):
            model = SVR(kernel='rbf', C=1.0, gamma='scale')
        else:
            max_features = int(math.ceil(math.log2(len(variables))))
            if(max_features == 0):
                max_features = 1
            model = RandomForestRegressor(
                n_estimators=100,
                max_features=max_features
            )

        # Treinar o modelo
        model.fit(X_train, y_train)

        # Fazer previsões
        y_pred = model.predict(X_test)
        
        # Avaliar o modelo usando o coeficiente R²
        r2 = r2_score(y_test, y_pred)

        return r2
    
    def evaluate_best_variable(self):

        variables = get_variables(self.dataframe)

        metric_values = []
        for i, variable in enumerate(variables):
            print(f"Testando variável {i}:{variable}")
            metric = self.evaluate_model([variable])
            metric_values.append(metric)
        
        best_R2 = max(metric_values)
        maximum_index = metric_values.index(best_R2)
        best_variable = variables[maximum_index]

        with open("best_variable.csv", 'a') as arquivo:
            arquivo.write(f"Variable, R2_value\n")
            arquivo.write(f"{best_variable}, {best_R2}\n")

        return best_variable, best_R2
    
    def execution(self, variable: str):

        # Definindo valores iniciais para a Busca pela melhor escolha
        full_variables = get_variables(self.dataframe)
        start_node = convert_variables_to_binary_array(full_variables, [variable])

        # Realizando a busca
        self.add_node(start_node)
        best_node, best_R2 = self.greedy_search(start_node, full_variables)
        print("Melhor R2:", best_R2)

        # Criando novo dataframe
        variables = convert_binary_array_to_variables(best_node, full_variables)
        new_dataframe = self.dataframe[variables]

        # Adicionando a última coluna do novo Dataframe
        last_column_name = list(self.dataframe.columns)[-1]
        new_dataframe[last_column_name] = self.dataframe[last_column_name].tolist()
        new_dataframe.to_csv("base_best.csv", index=False)

        return best_node, best_R2
