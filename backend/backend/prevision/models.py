from django.db import models

from joblib import dump, load

class PrevisionModel(models.Model):
  model_file = models.FileField (
    upload_to='models/', null=True, blank=True
  )
  variables = models.JSONField(default=list)

  def retrieve_model(self):
    # Carregar o modelo de volta
    model = load(self.model_file.path)
    return model


  def __str__(self):
    return f"Modelo de previsão {self.id}"