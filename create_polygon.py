#coding:utf-8
import arcpy
from arcpy import env
def create_polygon(self):
    point = arcpy.Point()
    array = arcpy.Array()
    featureList = []
    for feature in self:
        for coord in feature:
            point.X = coord[0]
            point.Y = coord[1]
            array.add(point)

        array.add(array.getObject(0))
        polygon = arcpy.Polygon(array)
        array.removeAll()
        featureList.append(polygon)
    return featureList
def create():
    tt = arcpy.GetParameterAsText(0)
    out = arcpy.GetParameterAsText(1)
    file = open(tt)
    li = []
    for line in file:
        li.append(map(float,line.split()))
    code = []
    coord = []
    for i in range(len(li)):
        if len(li[i]) == 2:
            code.append(str(int(li[i][0]))+str(int(li[i][1])))
            coord.append([])
        else:
            coord[len(coord)-1].append([li[i][1],li[i][2]])
    poly = create_polygon(coord)
    arcpy.CopyFeatures_management(poly,out)
    arcpy.AddField_management(out,'code','TEXT')
    cur = arcpy.UpdateCursor(out)
    i = 0
    for row in cur:
        row.code = code[i]
        cur.updateRow(row)
        i = i + 1
    del cur,row,code,li,coord
if __name__ == '__main__':
    create()


    
    
