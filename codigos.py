#criar instancia
project = QgsProject.instance()
#identificar nome e caminho
print(project)

#abrir projeto
project.read('C:/Users/k/Documents/cursos/pyqgis/seção 4/dados/dados_sig.qgs')
print(project.fileName())

#salvar projeto
project.write('C:/Users/k/Documents/cursos/pyqgis/seção 4/dados/dados_sig.qgs')

#setar elipsoid
project.ellipsoid

#qtd camadas projeto
print(project.count())

#setar crs
project.setCrs(QgsCoordinateReferenceSystem("EPSG:31983"))
# setar nome do projeto

#//////////////////////////////////////////////////
#dados vetoriais
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'
#abrindo camada vetorial
path_layer = path + '/aeroportos.shp'
layer = QgsVectorLayer(path_layer,"aeroporto","ogr")
#adicionar camada no canvas
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'
path_layer = path + '/aeroportos.shp'
layer = QgsVectorLayer(path_layer,"aeroporto","ogr")
QgsProject.instance().addMapLayer(layer)

#segunda maneira de inportar camadas
layer = iface.addVectorLayer(path_layer,"aeroporto","ogr")

#//////////////////////////
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'

for root, directory, files in os.walk(path):
    for file in files:
        if file.endswith('.shp'):
           path_vector = os.path.join(path,file)
           layer = QgsVectorLayer(path_vector,file[0:-4],"ogr")
           QgsProject.instance().addMapLayer(layer)


path = os.getcwd()+'/cursos/pyqgis/seção 4/dados/'
#abrir camada vetorial
path_layer = path + '/aeroportos.shp'
layer = QgsVectorLayer(path_layer,"areoportos","ogr")

#adicionar camada canvas
QgsProject.instance().addMapLayer(layer)
#obter id layer
print(layer.id())
#extent
print(layer.extent())
#criar novos atributos
layer.startEditing()
layer.addAttribute(QgsField('teste',QVariant.String))
layer.commitChanges()
#obter informaçães campo
print(layer.fields().names())
#deelet campo
layer.startEditing()
layer.deleteAttribute(2)
layer.commitChanges()

/////////////////////////////////////

#remover atributo pelo nome
campos=layer.fields().names()
i=int(0)
for campos in campos:
    if campos == 'teste':
        layer.deleteAttribute(i)
        print(campos,i)



path = os.getcwd()+'/cursos/pyqgis/seção 4/dados/'
path_layer = path + '/aeroportos.shp'
layer = QgsVectorLayer(path_layer,"areoportos","ogr")
QgsProject.instance().addMapLayer(layer)

count = 0 
for feature in layer.getFeatures():
	while count < 5:
		print(feature.attributes()[14])
		count += 1 
#UPDATE CAMPO
#delerar campo 'teste
layer.startEditing()
layer.deleteAttribute(14)
layer.commitChanges()

#adicionar  x campo
layer.startEditing()
layer.addAttribute(QgsField('x',QVariant.Double))
layer.commitChanges()
count = 0 
for feature in layer.getFeatures():
	while count < 5:
		print(feature.geometry())
		count += 1 
layer.startEditing()
for feature in layer.getFeatures():
        id = feature.id()
        x = feature.geometry().asPoint()[0]
        attr_value = {14:x}
        layer.changeAttributeValues(id,attr_value)

layer.commitChanges()

#adicionar  y campo
layer.startEditing()
layer.addAttribute(QgsField('y',QVariant.Double))
layer.commitChanges()

count = 0 
for feature in layer.getFeatures():
	while count < 5:
		print(feature.geometry())
		count += 1
layer.startEditing()
for feature in layer.getFeatures():
        id = feature.id()
        y = feature.geometry().asPoint()[1]
        attr_value = {15:y}
        layer.changeAttributeValues(id,attr_value)

layer.commitChanges()

//////////////SELEÇÃO DE FEIÇÕES//////////////////////
#seleção por expressão
layer.selectByExpression("TipoAero = 'Nacional'",QgsVectorLayer.SetSelection)
#inverter
layer.invertSelection()
#adicionar seleção 
layer.selectByExpression("nome iLike 'N%'",QgsVectorLayer.AddToSelection)

#remover seleçao
layer.selectByExpression("nome iLike 'A%'",QgsVectorLayer.RemoveFromSelection)
#criar ojeto com seleção
selection = layer.selectedFeatures()
for feature in selection:
     print(feature.attributes())

#deletar campos
layer.startEditing()
layer.deleteAttribute(13)

layer.commitChanges()


#criar coluna nova do tipo texto
layer.startEditing()
layer.addAttribute(QgsField('executor',QVariant.String,'text',255))
layer.commitChanges()
#update de valores na tabela em selecionados
layer.startEditing()
for feature in selection:
    id = feature.id()
    layer.changeAttributeValue(id,13,'newmar')

layer.commitChanges()

////////////////////////////////////////////////////////////////
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'

for root, directory, files in os.walk(path):
    for file in files:
        if file.endswith('.shp'):
           path_vector = os.path.join(path,file)
           layer = QgsVectorLayer(path_vector,file[0:-4],"ogr")
           QgsProject.instance().addMapLayer(layer)

aeroportos = QgsProject.instance().mapLayersByName("aeroportos")[0]
municipios = QgsProject.instance().mapLayersByName("municipios")[0]
rodovias = QgsProject.instance().mapLayersByName("rodovias")[0]

d= QgsDistanceArea()
d.setEllipsoid("GRS80")

count = 0
for feature in municipios.getFeatures():
    if count < 5:
        municipio = feature["municipio"]
        geom = feature.geometry()
        area = d.measureArea(geom)
        areaha = d.convertAreaMeasurement(area,QgsUnitTypes.AreaHectares)
        perimeter = d.measurePerimeter(geom)
        print(municipio)
        print('Area m2: ', area)
        print('Area Ha: ', areaha)
        print('Perimetro: ',perimeter)
        print(municipio)
        count += 1
    else:
        break

aeroportos.selectByExpression("OBJECTID in (2411,2425)",QgsVectorLayer.SetSelection)


///////////////////////
path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'

for root, directory, files in os.walk(path):
    for file in files:
        if file.endswith('.shp'):
           path_vector = os.path.join(path,file)
           layer = QgsVectorLayer(path_vector,file[0:-4],"ogr")
           QgsProject.instance().addMapLayer(layer)


municipios = QgsProject.instance().mapLayersByName("municipios")[0]
print(municipios.featureCount())

municipios.setSubsetString("uf = 'PR'")

##exportando arquivo vetorial

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName ="ESRI Shapefile"
out_path = os.path.join(path,'results/municipios4')
transform = QgsProject.instance().transformContext()
QgsVectorFileWriter.writeAsVectorFormatV2(municipios,out_path,transform,options)


///////////////////////////manipulação raster//////////////////////

#### aula 18

path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/cbers.tif'
#primeira forma de adicionar raster
rlayer = QgsRasterLayer(path,"cbers")
QgsProject.instance().addMapLayer(rlayer)
#segunda forma de adicionar camada
#iface.addRasterLayer(path,"cbers")
rlayer.htmlMetadata()

print(rlayer.width(),rlayer.height())
print(rlayer.extent().toString())
print(rlayer.rasterType())
print(rlayer.bandCount())
print(rlayer.bandName(4))

print(rlayer.renderer().type())

#### aula 19
raster = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/merge.tif'
rlayer = QgsRasterLayer(raster,"dem")
#QgsProject.instance().addMapLayer(rlayer)

fcn = QgsColorRampShader()
fcn.setColorRampType(QgsColorRampShader.Interpolated)
lst = [
QgsColorRampShader.ColorRampItem(0 ,QColor(20, 0, 153)),
QgsColorRampShader.ColorRampItem(300,QColor(102, 204, 255)),
QgsColorRampShader.ColorRampItem(900,QColor(255, 255, 0)),
QgsColorRampShader.ColorRampItem(1100, QColor(255, 80, 80)),
QgsColorRampShader.ColorRampItem(1600,QColor(255, 0, 0)),
]
fcn.setColorRampItemList(lst)
shader = QgsRasterShader()
shader.setRasterShaderFunction(fcn)
renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(),1,shader)
rlayer.setRenderer(renderer)
rlayer.triggerRepaint()
QgsProject.instance().addMapLayer(rlayer)

#aula 20

statistics = rlayer.dataProvider().bandStatistics(1,QgsRasterBandStats.All)

print(statistics.stdDev)


#aula 23
#função para listar as camadas do projeto
def list_files(path,tipo):
    lst=[]
    for root,directory,files in os.walk(path):
        for file in files:
            if file.endswith(tipo):
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

path = os.getcwd()+ '/cursos/pyqgis/seção 4/dados/'
camadas = open_vector_layers(path,'.shp')

for i in camadas['piaui_dissolve'].getFeatures():
    print(i.attributes())
##########################





#@KZandre360360