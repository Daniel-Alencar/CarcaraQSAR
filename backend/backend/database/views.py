from io import StringIO
import pandas as pd
import json
import csv

from threading import Thread

from django.core.exceptions import ObjectDoesNotExist

from django.http import FileResponse, StreamingHttpResponse
import os
from collections import OrderedDict

from django.utils.encoding import smart_str
from django.core.files.base import ContentFile

from padelpy import from_smiles

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from .utils import get_line_descriptors, getBoxPlotImage, getHistogramImage

from project_management.models import Project
from database.models import Database, Normalization

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import time

# Create your views here.
@permission_classes([IsAuthenticated])
def minha_view(request):
  # Define a função de resposta SSE

  def event_stream():
    # Exemplo de 10 mensagens
    for i in range(10):
      # Simula um processo demorado
      time.sleep(1)
      # Envia a mensagem para o cliente
      yield f"data: Mensagem {i}\n\n"

  # Retorna a resposta SSE
  response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
  response['Cache-Control'] = 'no-cache'
  return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convertAndSendDatabase_view(request):
  print("Convertendo o arquivo SMILES")

  if 'file' in request.FILES:
    uploaded_file = request.FILES.get('file')
    project_id = request.POST.get('project_id')

    project = get_object_or_404(Project, id=project_id)

    # Cria uma lista das linhas do arquivo
    file_content = uploaded_file.read().decode('utf-8')
    list_file_content = file_content.split('\n')
    list_file_content.remove('')

    # Variáveis auxiliares
    keys = set()
    list_descriptors = []

    # Salva uma lista das características em comum de todas as moléculas
    def analisingFeatures():
      nonlocal keys
      nonlocal list_descriptors
      nonlocal list_file_content
      nonlocal project

      keys = set()
      list_descriptors = []
      length = len(list_file_content)

      for i in range(length):
        print("Analisando características:", list_file_content[i])
        if(project.database):
          print(f"Progresso: {i + 1}/{length}")
          project.database.set_conversion_progress(i + 1, length)
          
        descriptors = from_smiles(list_file_content[i].split(',')[0])

        # Envia a mensagem de progresso para o cliente
        # yield f"data: {i}/{length} moléculas analisadas\n\n"

        list_descriptors.append(descriptors)

        if(i == 0):
          keys = set(descriptors.keys())
        else:
          new_keys = set(descriptors.keys())
          keys = keys.intersection(new_keys)
      
      keys = list(keys)
      keys.append('alvo')
    
    # Cria o arquivo com as características, o salva e o retorna
    def createFileAndSave():
      nonlocal keys
      nonlocal list_descriptors
      nonlocal file_content
      nonlocal list_file_content
      nonlocal project
      nonlocal project_id
      nonlocal uploaded_file

      file_name = uploaded_file.name
      # Cria arquivo CSV
      with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Escreve o cabeçalho
        csv_writer.writerow(keys)
        
        # Escreve os dados do CSV
        for i, line_smiles in enumerate(list_file_content):

          line_smiles_split = line_smiles.split(',')
          list_descriptors[i]['alvo'] = line_smiles_split[1]
          line_descriptors = get_line_descriptors(keys, list_descriptors[i])

          line_descriptors_split =line_descriptors.split(',')

          csv_writer.writerow(line_descriptors_split)
      
        # Cria um DataFrame do Pandas com o conteúdo do arquivo
        data_dataframe = pd.read_csv(file_name)
        rows, columns = data_dataframe.shape
        # Ler o arquivo.csv e o atribui a uma variável (para salvar no Database)
        with open(file_name, 'rb') as arquivo:
          file_content = arquivo.read()
        # Salvar database com as informações
        database = Database().create(
          name=file_name,
          file=None,
          file_separator=',',
          lines=rows,
          columns=columns
        )
        database.file.save(file_name, ContentFile(file_content))
        project.database = database
        # Salvar modificações no backend
        project.save()

        os.remove(file_name)

        # Abra o arquivo e retorne como uma resposta de arquivo
        with open(f"media/{project.database.file}", 'rb') as file:
          response = HttpResponse(file.read(), content_type='application/force-download')
          response['Content-Disposition'] = f'attachment; filename="{file_name}"'
          return response

    analisingFeatures()
    response = createFileAndSave()
    return response

  return JsonResponse({ "message": "Nenhum arquivo encontrado!" })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendDatabase_view(request):

  if 'file' in request.FILES:
    uploaded_file = request.FILES.get('file')
    project_id = request.POST.get('project_id')
    separator = request.POST.get('separator')
    isSmiles = request.POST.get('separator')
    if(isSmiles == 'true'):
      isSmiles = True
    else:
      isSmiles = False

    project = get_object_or_404(Project, id=project_id)

    # Cria um DataFrame do Pandas com o conteúdo do arquivo
    file_content = uploaded_file.read().decode('utf-8')
    data_dataframe = pd.read_csv(
      StringIO(file_content), 
      sep=separator
    )
    rows, columns = data_dataframe.shape

    database = Database().create(
      name=uploaded_file.name,
      file=uploaded_file,
      file_separator=separator,
      lines=rows,
      columns=columns
    )
    project.database = database
    
    # Salvar no backend
    project.save()

    return JsonResponse({ "message": f"{uploaded_file.name} enviado!"})
  return JsonResponse({ "message": "Arquivo não enviado!" })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDatabase_view(request):
  project_id = request.GET.get('project_id')
  transposed = request.GET.get('transposed')
  if transposed == "true":
    transposed = True
  else:
    transposed = False

  project = get_object_or_404(Project, id=project_id)
  database = project.database

  if(database):
    if(database.file):

      # Cria um DataFrame do Pandas com o conteúdo do arquivo
      file_content = database.file.read().decode('utf-8')
      data_dataframe = pd.read_csv(
        StringIO(file_content), 
        sep=database.file_separator
      )

      # Pega somente as primeiras linhas do database
      data_dataframe = data_dataframe.head()

      # Faz a transposição se necessário
      columns = data_dataframe.columns
      if transposed:
        data_dataframe = data_dataframe.T
        data_dataframe.insert(0, 'columns', columns)

        # Gerar nomes de coluna com a lógica 'a1', 'a2', 'a3', ...
        columns_names = [
          'a' + str(i) for i in range(1, len(data_dataframe.columns) + 1)
        ]
        data_dataframe.columns = columns_names

      # Transforma para o formato Json
      data_dictionary = data_dataframe.to_dict(orient='records')

      return JsonResponse({
        'database': data_dictionary,
        'fileSeparator': database.file_separator,
        'name': database.name,
        'lines': database.lines,
        'columns': database.columns,
      })
  
  return JsonResponse({
    'message': 'Nenhum arquivo no projeto!',
    'database': None,
  })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getVariables_view(request):
  project_id = request.GET.get('project_id')

  project = get_object_or_404(Project, id=project_id)
  database = project.database

  if(database):
    if(database.file):

      # Cria um DataFrame do Pandas com o conteúdo do arquivo
      file_content = database.file.read().decode('utf-8')
      data_dataframe = pd.read_csv(
        StringIO(file_content), 
        sep=database.file_separator
      )

      variables = data_dataframe.columns.tolist()
      variables.pop()

      return JsonResponse({
        'variables': variables
      })
  
  return JsonResponse({
    'message': 'Database não encontrado!',
  })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getHistogram_view(request):

  project_id = request.GET.get('project_id')
  variable = request.GET.get('variable')
  divisions_bins = request.GET.get('divisions')
  num_bins = int(divisions_bins)

  project = get_object_or_404(Project, id=project_id)
  database = project.database

  if(database):
    if(database.file):

      # Cria um DataFrame do Pandas com o conteúdo do arquivo
      file_content = database.file.read().decode('utf-8')
      data_dataframe = pd.read_csv(
        StringIO(file_content), 
        sep=database.file_separator
      )

      # Faz o filtro de acordo com a variável
      variable_data = data_dataframe[variable].values
      variable_array = np.array(variable_data)

      # Crie uma máscara booleana indicando quais elementos do array são NaN
      mask_nan = np.isnan(variable_array)

      # Conte a quantidade de valores NaN usando np.sum() na máscara
      number_of_Nan_values = np.sum(mask_nan)

      # Remova os valores NaN do array
      variable_array = variable_array[~np.isnan(variable_array)]

      histogram_image = getHistogramImage(variable_array, num_bins)

      return Response({ 
        'imageInBase64': histogram_image,
        'numberOfNaNValues': number_of_Nan_values
      }, status=200)
  return Response({ 
    'message': 'Database não encontrado!',
  })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBoxPlot_view(request):
  
  project_id = request.GET.get('project_id')
  variable = request.GET.get('variable')

  project = get_object_or_404(Project, id=project_id)
  database = project.database

  if(database):
    if(database.file):

      # Cria um DataFrame do Pandas com o conteúdo do arquivo
      file_content = database.file.read().decode('utf-8')
      data_dataframe = pd.read_csv(
        StringIO(file_content), 
        sep=database.file_separator
      )

      # Faz o filtro de acordo com a variável
      variable_data = data_dataframe[variable].values
      variable_array = np.array(variable_data)

      # Crie uma máscara booleana indicando quais elementos do array são NaN
      mask_nan = np.isnan(variable_array)

      # Conte a quantidade de valores NaN usando np.sum() na máscara
      number_of_Nan_values = np.sum(mask_nan)

      # Remova os valores NaN do array
      variable_array = variable_array[~np.isnan(variable_array)]

      boxPlot_image = getBoxPlotImage(variable_array)

      return Response({ 
        'imageInBase64': boxPlot_image,
        'numberOfNaNValues': number_of_Nan_values,
      }, status=200)

  return Response({ 
    'message': 'Database não encontrado!',
  }, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setNormalizationSettings_view(request):

  project_id = request.POST.get('project_id')
  normalization = request.POST.get('normalization')

  project = get_object_or_404(Project, id=project_id)

  if(project.database):
    if(project.database.normalization):
      project.database.normalization.update(normalization, False)
    else:
      normalization_instance = Normalization.objects.create(name=normalization)
      project.database.normalization = normalization_instance
      project.database.save()

    return Response({
      'message': f'Normalização {normalization} salva!'
    }, status=200)
  return Response({
    'message': 'Não existe Database associado ao projeto!'
  }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNormalizationSettings_view(request):

  project_id = request.GET.get('project_id')
  project = get_object_or_404(Project, id=project_id)

  if(project.database):
    if(project.database.normalization):

      data = {
        'normalization': project.database.normalization.name,
        'applied': project.database.normalization.applied
      }
      return Response(data, status=200)

    else:
      
      normalization = Normalization.objects.create(name="NÃO APLICAR")
      project.database.normalization = normalization
      project.database.save()

      data = {
        'normalization': project.database.normalization.name,
        'applied': project.database.normalization.applied
      }
      return Response(data, status=200)

  return Response({
    'message': 'Não existe Database associado ao projeto!'
  }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getConversionProgress_view(request):
  try:
    project_id = request.GET.get('project_id')
    project = get_object_or_404(Project, id=project_id)

    database = project.database

    if(database):    
      return Response({
        'progress': database.conversion_progress,
      }, status=200)
    else:
      return Response({
        'message': "Database não encontrado!",
      }, status=500)
  except ObjectDoesNotExist:
    return HttpResponse("Project or training not found", status=404)