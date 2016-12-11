# #############
import arcpy
from arcpy import env
import numpy
import os





def statistic_m(input_raster,statistic_raster,dbf):
    a = os.path.split(dbf)
    b = os.path.splitext(a[1])
    sta = []
    array_sta = arcpy.RasterToNumPyArray(statistic_raster)
    array_inp = arcpy.RasterToNumPyArray(input_raster)
    none_sta = arcpy.Raster(statistic_raster).noDataValue
    none_inp = arcpy.Raster(input_raster).noDataValue
    sta_lst,inp_lst = [],[]
    for i in array_sta:
        for j in i:
            if j not in sta_lst and j != none_sta:
                sta_lst.append(j)

    for i in array_inp:
        for j in i:
            if j not in inp_lst and j != none_inp:
                inp_lst.append(j)
                
    arcpy.AddMessage(sta_lst)
    arcpy.AddMessage(inp_lst)
    print sta_lst,inp_lst
    
##    input_mini = int(arcpy.GetRasterProperties_management(input_raster,'MINIMUM').getOutput(0))
##    input_maxi = int(arcpy.GetRasterProperties_management(input_raster,'MAXIMUM').getOutput(0))
##    statistic_mini = int(arcpy.GetRasterProperties_management(statistic_raster,'MINIMUM').getOutput(0))
##    statistic_maxi = int(arcpy.GetRasterProperties_management(statistic_raster,'MAXIMUM').getOutput(0))
#   statistic_mini = 1
#   statistic_maxi = 3
    arcpy.CreateTable_management(a[0],a[1])
    arcpy.AddField_management(dbf,'region','LONG')
    
    for hh in inp_lst:
        arcpy.AddField_management(dbf,'c'+str(hh),'LONG')
    rows = arcpy.InsertCursor(dbf)
    for i in sta_lst:
        row = rows.newRow()
        row.setValue('region',int(i))
#        sta.append([])
        statistic = arcpy.sa.EqualTo(statistic_raster,int(i))
        for j in inp_lst:
            num  = 0
            input1 = arcpy.sa.EqualTo(input_raster,int(j))
            result = arcpy.sa.Times(statistic,input1)
            result_array = arcpy.RasterToNumPyArray(result)
            for k in result_array:
                num = num + len([x for x in k if x ==1])
            arcpy.AddMessage(num)
            row.setValue('c'+str(j),num)
#            sta[i].append(num)
            arcpy.AddMessage("succesfully statist the {0} of {1} as {2}".format(i,j,num))
            print "succesfully statist the {0} of {1} as {2}".format(i,j,num)
        rows.insertRow(row)
        
        
    del rows,row
    
            
    

if __name__ == '__main__':
    arcpy.CheckOutExtension('spatial')
##    arcpy.env.overwriteOutput = True
##    input_raster = 'G:/GHG_landuse/lucc2005'
##    statistic_raster = 'G:/GHG_landuse/province'
##    out_dbf = 'G:/GHG_landuse/yao1.dbf'

    
    input_raster = arcpy.GetParameterAsText(0)
    statistic_raster = arcpy.GetParameterAsText(1)
    out_dbf = arcpy.GetParameterAsText(2)
    statistic_m(input_raster,statistic_raster,out_dbf)
    arcpy.CheckInExtension('spatial')

