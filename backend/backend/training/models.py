from django.db import models

from project_management.models import Project





class Algorithm(models.Model):
  # Campo de escolha para o algoritmo
  ALGORITHM_CHOICES = [
    ('random_forest', 'Random Forest'),
    ('linear_regression', 'Linear regression'),
    ('KNN', 'KNN'),
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

class Training(models.Model):
  # Para o treinamento
  algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
  trained = models.BooleanField(default=False)
  with_full_set = models.BooleanField(default=False)

  progress = models.CharField(
    max_length=10,
    null=True,
    blank=True,
    default=None
  )
  execution_type = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    default=None
  )
  task_id = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    default=None
  )

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

  def set_progress(self, actual, total, actual_step, total_steps):
    self.progress = f"{actual}/{total}/{actual_step}/{total_steps}"
    self.save()

  def set_execution_type(self, execution_type):
    self.execution_type = execution_type
    self.save()

  def set_progress_none(self):
    self.progress = None
    self.execution_type = None
    self.save()

  def set_task_id(self, task_id):
    self.task_id = task_id
    self.save()

  def set_task_id_none(self):
    self.task_id = None
    self.save()


  def __str__(self):
    return f"Treinamento com algoritmo '{self.algorithm.name}'"
  
class BootstrapValues(models.Model):
  molecules = models.JSONField(default=list)
  R_value = models.FloatField(null=True)
  R2_value = models.FloatField(null=True)

  training = models.ForeignKey(
    Training, 
    on_delete=models.CASCADE,
    null=True
  )

  def update(self, molecules, R_value, R2_value):
    self.molecules = molecules
    self.R_value = R_value
    self.R2_value = R2_value
    self.save()

  def __str__(self):
    return f"Bootstrap do treinamento"
