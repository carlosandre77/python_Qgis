from qgis.core import QgsExpression, QgsVectorLayer

project= QgsProject.instance()

##nome do local que sera corfigurada a base
base_proj=('pau_darco')

##caminho dos arquivos
path = ( r'C:\Users\Carlos André-DIGITAL\Documents\digital map - geo\PROJETOS DMG\PAU_DARCO\SHAPES\Nova pasta'.replace('\\', '/'+'/'))

for root, directory, files in os.walk(path):
    for file in files:
        if file.endswith('.shp'):
           path_vector = os.path.join(path,file)
           layer = QgsVectorLayer(path_vector,file[0:-4],"ogr")
           QgsProject.instance().addMapLayer(layer)
           ##identificação das principais feições
           if layer.name() == 'bairro_'+ base_proj:
               lay_bairros = QgsProject.instance().mapLayersByName(layer.name())[0]
               print(lay_bairros.name())
           if layer.name() == 'lotes_'+ base_proj:
               lay_lotes = QgsProject.instance().mapLayersByName(layer.name())[0]
               print(lay_lotes.name())
                
           if layer.name() == 'quadras_'+ base_proj:
               lay_quadras = QgsProject.instance().mapLayersByName(layer.name())[0]
               print(lay_quadras.name())
               
           if layer.name() == 'edificacoes_'+ base_proj:
               lay_edificacoes = QgsProject.instance().mapLayersByName(layer.name())[0]
               print(lay_edificacoes.name())

### alterar campos 
campo_area = "area_m2"
campo_perimetro = "perimetro"

lay_bairros.startEditing()
##adicionar campos
lay_bairros.addAttribute(QgsField(str(campo_area),QVariant.Double))
lay_bairros.addAttribute(QgsField(str(campo_perimetro),QVariant.Double))
lay_bairros.addAttribute(QgsField(str("qtd_quadr"),QVariant.Int))
lay_bairros.addAttribute(QgsField(str("qtd_lote"),QVariant.Int))
lay_bairros.addAttribute(QgsField(str("qtd_edific"),QVariant.Int))

i = 0
for feature in lay_bairros.getFeatures():
        id = feature.id()
        campos = lay_bairros.fields()
        geom = feature.geometry()
        indice_campo_area = campos.indexFromName(str(campo_area))
        indice_campo_perimetro = campos.indexFromName(str(campo_perimetro))
        indice_campo_qtd_quadr = campos.indexFromName("qtd_quadr")
        indice_campo_qtd_lote = campos.indexFromName("qtd_lote")
        indice_campo_qtd_edificacao = campos.indexFromName("qtd_edific")
        area = QgsDistanceArea().measureArea(geom)
        perimetro = QgsDistanceArea().measurePerimeter(geom)
        lay_bairros.changeAttributeValue(id,indice_campo_area,area)
        lay_bairros.changeAttributeValue(id,indice_campo_perimetro,perimetro)
        lay_bairros.changeAttributeValue(id,indice_campo_qtd_quadr,lay_quadras.featureCount())
        lay_bairros.changeAttributeValue(id,indice_campo_qtd_lote,lay_lotes.featureCount())
        lay_bairros.changeAttributeValue(id,indice_campo_qtd_edificacao,lay_edificacoes.featureCount())
        i += 1
        


lay_bairros.commitChanges()


