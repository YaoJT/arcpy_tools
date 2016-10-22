## calculate fragmentation based on grid
## coding: utf-8
## author: Yaojingtao, jingtao_yao@cau.edu.cn

import arcpy
import numpy as np
import random


def Frag(in_raster,window_x,window_y,from_value,to_value):
    in_array = arcpy.RasterToNumPyArray(in_raster)
    none_value = arcpy.Raster(in_raster).noDataValue
    cell_size_x = int(arcpy.GetRasterProperties_management(in_raster,'CELLSIZEX').getOutput(0))
    cell_size_y = int(arcpy.GetRasterProperties_management(in_raster,'CELLSIZEY').getOutput(0))
    min_x = float(arcpy.GetRasterProperties_management(in_raster,'LEFT').getOutput(0))
    max_x = float(arcpy.GetRasterProperties_management(in_raster,'RIGHT').getOutput(0))
    min_y = float(arcpy.GetRasterProperties_management(in_raster,'BOTTOM').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(in_raster,'TOP').getOutput(0))
    row_num = int(max_y - min_y)/cell_size_y
    col_num = int(max_x-min_x)/cell_size_x
    row_num_new = int(row_num/window_y)
    col_num_new = int(col_num/window_x)
    min_x_new = min_x
    min_y_new = min_y + row_num%window_y
    corner = arcpy.Point(min_x_new,min_y_new)
    new_array = np.zeros((row_num_new,col_num_new))
    for row in range(row_num_new):
        for col in range(col_num_new):
            value = 0
            for i in range(window_y):
                for j in range(window_x):
                    new_row,new_col = window_y*row+i,window_x*col+j
                    if i != window_y -1:
                        if in_array[i,j] == from_value and in_array[i+1,j] == to_value:
                            value += 1
                    if j != window_x -1:
                        if in_array[i,j] == from_value and in_array[i,j+1] == to_value:
                            value += 1
            new_array[row,col] = value
    out_res = arcpy.NumPyArrayToRaster(new_array,corner,cell_size_x*window_x,cell_size_y*window_y)
    return out_res

if __name__ == '__main__':

    in_path = 'h:/random9'
    out_path = 'h:/frag1'
    window_x,window_y = 5,5
    from_value,to_value = 2,3
    
    arcpy.CheckOutExtension('spatial')
    arcpy.env.overwriteOutput = True
##    a = np.zeros((26,30))
##    for i in range(26):
##        for j in range(30):
##            a[i,j] = random.randint(1,10)
##    in_raster = arcpy.NumPyArrayToRaster(a)
##    in_raster.save(in_path)
    if from_value == to_value:
        out_raster = Frag(in_path,window_x,window_y,from_value,to_value)
    else:
        out_raster1 = Frag(in_path,window_x,window_y,from_value,to_value)
        out_raster2 = Frag(in_path,window_x,window_y,to_value,from_value)
        out_raster = arcpy.sa.Plus(out_raster1,out_raster2)
    out_raster.save(out_path)
    arcpy.CheckInExtension('spatial')
