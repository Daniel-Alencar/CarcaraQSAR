from django.db import models

from project_management.models import Project





class Algorithm(models.Model):
  # Campo de escolha para o algoritmo
  ALGORITHM_CHOICES = [
    ('random_forest', 'Random Forest'),
    ('linear_regression', 'Regressão linear'),
    ('logistic_regression', 'Regressão logística'),
    ('svm', 'Support Vector Machines (SVM)'),
  ]
  name = models.CharField(max_length=200, choices=ALGORITHM_CHOICES)
  parameters = models.JSONField(default=dict)

  def create(self, name, parameters):
    algorithm = Algorithm.objects.create(
      name=name,
      parameters=parameters
    )
    return algorithm
  
  def update(self, name, parameters):
    self.name = name
    self.parameters = parameters
    self.save()

  def __str__(self):
    return self.name




class RandomForest(Algorithm):
  num_trees = models.IntegerField()
  max_depth = models.IntegerField()

class SVM(Algorithm):
  kernel = models.CharField(max_length=50)
  C_parameter = models.FloatField()

class LinearRegression(Algorithm):
  regularization = models.FloatField()




class Training(models.Model):
  # Para o treinamento
  algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
  trained = models.BooleanField(default=False)
  with_full_set = models.BooleanField(default=False)

  project = models.ForeignKey(Project, on_delete=models.CASCADE)

  leave_one_out =  models.ImageField(
    upload_to='graphics_results/leave_one_out/',
    null=True,
    blank=True,
    default=None
  )
  importance =  models.ImageField(
    upload_to='graphics_results/importance/',
    null=True,
    blank=True,
    default=None
  )
  k_fold_cross_validation =  models.ImageField(
    upload_to='graphics_results/k-fold_cross_validation/',
    null=True,
    blank=True,
    default=None
  )
  y_scrambling =  models.ImageField(
    upload_to='graphics_results/y-scrambling/',
    null=True,
    blank=True,
    default=None
  )
  bootstrap =  models.ImageField(
    upload_to='graphics_results/bootstrap/',
    null=True,
    blank=True,
    default=None
  )

  def __str__(self):
    return f"Treinamento com algoritmo '{self.algorithm.name}'"

class VariablesSelection(models.Model):
  # Para seleção de variáveis
  algorithm = models.CharField(max_length=200)
  remove_constant_variables = models.BooleanField(default=False)
  variables_to_remove = models.JSONField(default=list)

  project = models.ForeignKey(Project, on_delete=models.CASCADE)

  def update(self, algorithm, remove_constant_variables, variables_to_remove):
    self.algorithm = algorithm
    self.remove_constant_variables = remove_constant_variables
    self.variables_to_remove = variables_to_remove
    self.save()

  def __str__(self):
    return f"Seleção de variáveis com o algoritmo '{self.algorithm}'"