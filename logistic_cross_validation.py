import arcpy
import random
import numpy as np


def ROC_analyst(prob_list,observe_list,out_figure,step = 0.01):
    import matplotlib.pyplot as plt
    prob_list,observe_list = np.array(prob_list),np.array(observe_list)
## calculate AUC
    true_list,false_list = [],[]
    for x in range(len(prob_list)):
        if observe_list[x] == 1:
            true_list.append(prob_list[x])
        else:
            false_list.append(prob_list[x])
    true_num = 0.0
    for x in true_list:
        true_num += np.sum(false_list < x)
    AUC = true_num/(len(true_list)*len(false_list))

## drawing ROC plot    
    x,y = [0],[0]
    for i in np.arange(0,1,step):
        TP = np.sum(np.array(true_list)>i)/float(len(true_list))
        FP = np.sum(np.array(false_list)>i)/float(len(false_list))
        x.append(FP)
        y.append(TP)
    plt.figure()
    plt.plot(x,y,'-')
    plt.plot([0,1],[0,1],'-')
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.text(0.5,0.3,'AUC = %s' %round(AUC,4))
    plt.savefig(out_figure)
    del plt
    return AUC
    


if __name__ == '__main__':
    lucc = 'g:/CLUE-sII/data/lucc2015_f'
    land_array = arcpy.RasterToNumPyArray(lucc)
    land_type = np.array([1,2,3,51,52,53])
    predict_map = ['g:/logistics/probablity_'+str(x) for x in land_type]
    predict_array = []
    out_space = 'g:/logistics/'
    for x in predict_map:
        predict_array.append(arcpy.RasterToNumPyArray(x))
    total_num = 100000
    out_res = []
    
    min_x = float(arcpy.GetRasterProperties_management(lucc,'LEFT').getOutput(0))
    max_x = float(arcpy.GetRasterProperties_management(lucc,'RIGHT').getOutput(0))
    min_y = float(arcpy.GetRasterProperties_management(lucc,'BOTTOM').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(lucc,'TOP').getOutput(0))
    cell_size_x = float(arcpy.GetRasterProperties_management(lucc,'cellsizex').getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(lucc,'cellsizey').getOutput(0))

    min_x_p = float(arcpy.GetRasterProperties_management(predict_map[0],'LEFT').getOutput(0))
    max_x_p = float(arcpy.GetRasterProperties_management(predict_map[0],'RIGHT').getOutput(0))
    min_y_p = float(arcpy.GetRasterProperties_management(predict_map[0],'BOTTOM').getOutput(0))
    max_y_p = float(arcpy.GetRasterProperties_management(predict_map[0],'TOP').getOutput(0))
    cell_size_x_p = float(arcpy.GetRasterProperties_management(predict_map[0],'cellsizex').getOutput(0))
    cell_size_y_p = float(arcpy.GetRasterProperties_management(predict_map[0],'cellsizey').getOutput(0))    
    
    num = 0
    while True:
        result = []
        x,y = random.uniform(min_x,max_x),random.uniform(min_y,max_y)
        row,col = int((max_y-y)/cell_size_y),int((x-min_x)/cell_size_x)
        row_p,col_p = int((max_y_p-y)/cell_size_y_p),int((x-min_x_p)/cell_size_x_p)
        if (land_array[row,col] in land_type) and predict_array[0][row_p,col_p] >= 0 and predict_array[0][row_p,col_p] <= 1:
            land_list = (land_type == land_array[row,col])
            radio_list = ([predict_array[x][row_p,col_p] for x in range(6)])
            result.append(land_list)
            result.append(radio_list)
            out_res.append(result)
            num += 1
        if num >= total_num:
            break
    for i in range(len(land_type)):
        print 'strat processing of land use %s' %land_type[i]
        prob_list = [out_res[x][1][i] for x in range(total_num)]
        observe_list = [out_res[x][0][i] for x in range(total_num)]
        out_figure = out_space+'ROC_'+str(land_type[i])+'.jpg'
        AUC=ROC_analyst(prob_list,observe_list,out_figure)
        print land_type[i],AUC
        
   
        
        
