
import pandas as pd
from utils import convert_binary_array_to_variables, convert_variables_to_binary_array, get_variables

from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import StandardScaler

from sklearn.svm import SVC, SVR



def create_model(dataframe, variables):
  
  X = dataframe[variables]
  y = dataframe.iloc[:, -1]

  # Normalizar os dados
  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  # Dividir o conjunto de dados em treino e teste
  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
  )

  # Criar o modelo
  model = SVR(kernel='rbf', C=1.0, gamma='scale')

  # Treinar o modelo
  model.fit(X_train, y_train)

  # Fazer previsões
  y_pred = model.predict(X_test)
  
  # Avaliar o modelo usando o coeficiente R²
  r2 = r2_score(y_test, y_pred)
  print("Coeficiente R² do modelo:", r2)

  return r2

def evaluate_best_variable(dataframe):

  variables = get_variables(dataframe)

  metric_values = []
  for i, variable in enumerate(variables):
    print(f"Testando variável {i}:{variable}")
    metric = create_model(dataframe, [variable])
    metric_values.append(metric)
  
  maximum_value = max(metric_values)
  maximum_index = metric_values.index(maximum_value)

  return variables[maximum_index], maximum_value



class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[tuple(node)] = []

    def add_child(self, parent, child):
        self.graph[tuple(parent)].append(child)

    def greedy_search(self, start, full_variables):
        visited = set()
        frontier = [(self.calculate_R2(start, full_variables), start)]
        best_node = None
        best_R2 = 0

        while frontier:
            # Ordena a fronteira pelo valor de R2 decrescente
            frontier.sort(reverse=True)
            # Obtém o nó com o maior valor de R2
            current_R2, current_node = frontier.pop(0)

            if tuple(current_node) in visited:
                continue

            visited.add(tuple(current_node))

            print(f"Valor R2 = {current_R2} para o nó atual")

            # Condição de parada
            if current_R2 >= r2_condition:
                print(f"R2 >= {r2_condition}. Parando a busca.")
                best_node = current_node
                best_R2 = current_R2
                break
            
            # Atualiza o melhor nó encontrado até agora
            if current_R2 > best_R2:
                best_node = current_node
                best_R2 = current_R2

            for child in self.generate_children(current_node):
                if tuple(child) not in visited:
                    frontier.append(
                       (self.calculate_R2(child, full_variables), child)
                    )
        return best_node, best_R2

    def calculate_R2(self, binary_array, full_variables):
        choosen_variables = convert_binary_array_to_variables(
           binary_array, full_variables
        )
        return create_model(dataframe, choosen_variables)

    def generate_children(self, node):
        children = []

        # Adiciona 1 em uma posição diferente do array para gerar os filhos
        for i in range(len(node)):
            if(node[i] == 1):
                continue
            child = node[:i] + [1] + node[i+1:]
            children.append(child)

        return children



# Criação do Dataframe
r2_condition = 0.99
filepath = "base_compressed.csv"
dataframe = pd.read_csv(filepath)


# Escolha da melhor variável inicial
print("BUSCA PELA MELHOR VARIÁVEL")

variable, value = evaluate_best_variable(dataframe)
print("Melhor variável:", variable)
print("Melhor R2:", value)
print("\n")

# Escolha da melhor configuração de variáveis
print('BUSCA GULOSA:')

# Definindo valores iniciais para a Busca pela melhor escolha
full_variables = get_variables(dataframe)
start_node = convert_variables_to_binary_array(full_variables, [variable])

graph = Graph()
# Adiciona o nó inicial
graph.add_node(start_node)
# Realiza a busca
best_node, best_R2 = graph.greedy_search(start_node, full_variables)
print("Melhor R2:", best_R2)

full_variables = get_variables(dataframe)
variables = convert_binary_array_to_variables(best_node, full_variables)
print(f"Quantidade de variáveis: {len(variables)}")

new_dataframe = dataframe[variables]
# Adicionando a última coluna
last_column_name = list(dataframe.columns)[-1]
new_dataframe[last_column_name] = dataframe[last_column_name].tolist()
print("Quantidade de colunas do novo Dataframe:", len(list(new_dataframe.columns)))

new_dataframe.to_csv("base_best.csv")
