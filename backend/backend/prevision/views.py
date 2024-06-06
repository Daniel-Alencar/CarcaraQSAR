import os
import json
import pandas as pd
import numpy as np
from io import StringIO

from django.shortcuts import get_object_or_404
from django.core.files import File

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from project_management.models import Project

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createModel_view(request):

  project_id = request.POST.get('project_id')
  project = get_object_or_404(Project, id=project_id)

  result = project.create_prevision_model()
  if(result):
    return Response({
      'message': 'Modelo criado com sucesso!'
    }, status=200)
  return Response({
    'message': 'Modelo não criado!'
  }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makePrevision_view(request):

  project_id = request.POST.get('project_id')
  project = get_object_or_404(Project, id=project_id)
  variables_values = request.POST.get('variables_values')
  variables_values = json.loads(variables_values)

  # Redimensione os dados para uma matriz 2D
  dataframe = pd.DataFrame([variables_values])
  dataframe_transposto = dataframe.T

  # Faz a normalização dos valores das variáveis
  # (Deve ser utilizado a normalização correta)
  scaler = MinMaxScaler()
  X_subset = scaler.fit_transform(dataframe_transposto)
  X_subset = X_subset.T

  # Recupera o model do banco de dados
  if(project.prevision_model):
    model = project.prevision_model.retrieve_model()

    # Realiza a previsão
    prevision = model.predict(X_subset)

    # Retorna valor da previsão
    return Response({
      'prevision': prevision
    }, status=200)
  return Response({
    'message': 'Não há modelo de previsão no banco de dados!'
  }, status=200)
