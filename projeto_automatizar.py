import sys
sys.path.insert(0,os.path.join(os.getcwd(),'GitHub/Estudos_e_Exerecicios/curso_pyqgis/'))
from minhas_funcoes import list_files,open_vector_layers,new_attribute, reproject, apply_filter, alerta_aero,create_folder


#################################################
    
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
def to_geopackage(layer,out_path,selected):
    options = QgsVectorFileWriter.SaveVectorOptions()
    if selected:
        options.onlySelectedFeatures = True
    transform_context = QgsProject.instance().transformContext()
    QgsVectorFileWriter.writeAsVectorFormatV2(layer,out_path,transform_context,options)
    return
    
def fix_geometries(path,camadas):
    for camada in camadas:
        input_path = path + camada +'.shp'
        #create_folder(path)
        out = path + camada+'2.shp'
        processing.run("native:fixgeometries", 
                        {'INPUT': input_path,
                        'METHOD':1,
                        'OUTPUT':out})
    return

def select_location(pontos,pol):
    processing.run("native:selectbylocation", 
    {'INPUT': pontos,
    'PREDICATE':[0,1,4,5],
    'INTERSECT':pol,
    'METHOD':0})

def apply_filter(layer,field,param):    
    return layer.setSubsetString(f"{field} = '{param}'")
    
def dividi_folders(camadas,camada_base,index):
    base = camadas[camada_base]
    spatial = camadas.copy()
    del spatial[camada_base]
    for i in base.uniqueValues(index):
        output_path = path + 'result/'+i
        create_folder(output_path)
        apply_filter(base,'uf',i)
        in_folder = output_path +'/'+i
        to_geopackage(base,in_folder,False)
        #####
        for camada in spatial:
            nome= camada.split('_')[0]
            select_location(camadas[camada],base)
            to_geopackage(camadas[camada],in_folder+ f'_{nome}',True)
        base.setSubsetString("")
    
#################inicio da execução
path = 'C:\\Users\\k\\Documents/cursos/pyqgis/seção 4/dados/'
reproject(path,31983)
camadas = open_vector_layers(path+'/reproject/','.shp')

path = 'C:\\Users\\k\\Documents/cursos/pyqgis/seção 4/dados/reproject/'
camadas = open_vector_layers(path,'.shp')
fix_geometries(path,camadas)
camada_base = 'municipios_reprojetado_319832'
fix_geometries(path,camadas)
dividi_folders(camadas, 'municipios_reprojetado_319832',4)


    