import arcpy
import numpy as np

def extract(multi_band_raster,coordinate_list,false_left = 0,false_north = 0, unit = 'CELL'):
    array = arcpy.RasterToNumPyArray(multi_band_raster)
    min_x = float(arcpy.GetRasterProperties_management(multi_band_raster,'LEFT').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(multi_band_raster,'TOP').getOutput(0))
    cell_x = float(arcpy.GetRasterProperties_management(multi_band_raster,'cellsizex').getOutput(0))
    cell_y = float(arcpy.GetRasterProperties_management(multi_band_raster,'cellsizey').getOutput(0))
    out_list = []
    for x,y in coordinate_list:
        value = [x,y]
        if unit.lower() == 'cell':
            col,row = int((x-min_x)/cell_x)-false_left,int((max_y-y)/cell_y)-false_north
        elif unit.lower() == 'map':
            col,row = int((x-false_left-min_x)/cell_x),int((max_y-y-false_north)/cell_y)
        for band in range(len(array)):
            value.append(array[band][row,col])
        out_list.append(value)
    return out_list

if __name__ == '__main__':
    raster = 'E:/QingChu/radiation work/ground validation/simulated radiation30/radiation_wgs_tif.tif'
    h_file = open('e:/QingChu/radiation work/ground validation/program output/hilltoprad.txt')
    hilltoprad = h_file.readlines()
    hilltoprad = float(hilltoprad)
    #coordinate = [[117.399496,42.393346],[117.398270,42.39062646],[117.399155,42.396745],[117.39765,42.392258],[117.399218,42.391347]]
    coordinate = [[117.40151600,42.39191138]]
    MAE = np.zeros((7,7)) 
    RMSE = np.zeros((7,7))
    min_cost = 99999
    opt_north,opt_left = 0,0
    for left in range(-3,4):
        for north in range(-3,4):
            res = extract(raster,coordinate,false_left = m,false_north = n)
            res = np.array(res)
            RMSE[left+3,north+3] = np.mean(np.power(np.array(res) - np.array(hilltoprad)))
            MAE[left+3,north+3] = np.mean(np.absolute(np.array(res) - np.array(hilltoprad)))
            cost = RMSE[left+3,north+3]+MAE[left+3,north+3]
            if cost < min_cost:
                min_cost,opt_left,opt_north = cost,left,north
    cost = RMSE + MAE
    print min_cost,opt_left,opt_north     

##    out_file = open('E:/QingChu/radiation work/ground validation/program output/try.csv','w+')
##    for i in range(len(coordinate)):
##        out_file.write('point_'+str(i+1)+',')
##    out_file.write('\n')
##    for i in range(len(res[0])):
##        for j in range(len(res)):
##            out_file.write(str(res[j][i])+',')
##        out_file.write('\n')
##    out_file.close()
        
    
