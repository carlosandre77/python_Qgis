#aula 2
import os 
import processing
from qgis.core import *
from qgis.utils import  iface
from PyQt5.QtCore import QVariant

#função para listar as camadas do projeto
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'
def list_files(path,type):
    lst=[]
    for root,directory,files in os.walk(path):
        for file in files:
            if file.endswith(type):
                lst.append(file)
    return lst
#função par abrir as camadas do projeto
def open_vector_layers(path,type):
    files = list_files(path,type)
    vectors={}
    for file in files:
        filename = file.split('.')[0]
        vector = iface.addVectorLayer(path+file,filename,'ogr')
        vectors.update({filename:vector})
    return vectors

def new_attribute(layer,field_name,type):
    if type == 1:
        field_type = QVariant.String
    elif type == 2:
        field_type = QVariant.int
    else:
        field_type = QVariant.Double
    
    layer.startEditing()
    layer.addAttribute(QgsField(field_name,field_type))
    #layer.commitChanges()
    return

    
def create_folder(path):
    if not os.path.exists(path+'reproject'):
        os.makedirs(path)

def reproject(path,epsg):
    create_folder(path)
    for shape in list_files(path,'.shp'):
        input_path = path + shape
        out_path = path + 'reproject/' + shape.replace('.','_reprojetado_' + str(epsg)+'.')
        processing.run("native:reprojectlayer", 
                    {'INPUT':input_path,
                    'TARGET_CRS':QgsCoordinateReferenceSystem(f'EPSG:{epsg}'),
                    'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=23 +south +ellps=GRS80',
                    'OUTPUT':out_path})
                    
    return
    
#aplica um filtro
def apply_filter(layer,field,param):    
    return layer.setSubsetString(f"{field} = '{param}'")

# aplica buffer e inporta no projeto
def alerta_aero(layer,param,path,field,state):
    apply_filter(layer,'uf','MT')
    if param == 'seco':
        buffer = 200
    elif param == 'chuva':
        buffer = 1000
    else:
        buffer = 3000        
    processing.run("native:buffer", {
                    'INPUT': layer,
                    'DISTANCE':buffer,
                    'SEGMENTS':5,
                    'END_CAP_STYLE':0,
                    'JOIN_STYLE':0,
                    'MITER_LIMIT':2,
                    'DISSOLVE':True,
                    'OUTPUT':path+'buffer.shp'})
    iface.addVectorLayer(path+'buffer.shp',"análise","ogr")
                    
    return 
   


