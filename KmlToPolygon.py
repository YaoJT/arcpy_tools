##encoding:utf-8
##this script was used to create one polygon file (.shp) from several kml files listed in one folder

import os
import arcpy

in_file = arcpy.GetParameterAsText(0)
out_file = arcpy.GetParameterAsText(1)

##in_file = 'g:/beijing/summer'
##out_file = 'g:/beijing/summer/convert'

if os.path.exists(out_file) == False:
    os.makedirs(out_file)
    
gg = os.listdir(in_file)
ff = []
for f in gg:
    if os.path.splitext(f)[1] == '.kml' or os.path.splitext[f][1] == '.kmz':
        ff.append(f)
arcpy.AddMessage(ff)
arcpy.CreateFeatureclass_management(out_file,'result.shp','POLYGON')
arcpy.AddField_management(os.path.join(out_file,'result.shp'),'Name','TEXT')
out_feature = os.path.join(out_file,'result.shp')

for i in range(len(ff)):
    in_file1 = os.path.join(in_file,ff[i])
    arcpy.KMLToLayer_conversion(in_file1,out_file)
    arcpy.AddMessage(ff[i]+'has been succesfully converted')
    arcpy.Append_management(os.path.join(os.path.join(out_file,os.path.splitext(ff[i])[0]+'.gdb'),'Placemarks_polygon'),out_feature,'NO_TEST')
    arcpy.AddMessage(ff[i]+'has been succesfully added to the result feature')
