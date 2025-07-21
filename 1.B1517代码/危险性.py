import pandas as pd
import numpy as np
import arcpy as ap

filePath = ap.GetParameterAsText(0)  # 城市表格路径
city = ap.GetParameterAsText(1)  # 城市行政区
grid = ap.GetParameterAsText(3)  # 城市格网
# workspace = ap.GetParameterAsText(4)  # 工作空间

# 导入excel数据
excel_file = filePath
# excel_file=r"深圳市数据.csv"
data = pd.read_csv(excel_file)

# 分别对不同的指标进行正负向处理
# 负向指标：人均GDP、地区GDP、万人病床数
data_min = data.loc[:, ['10d累计新增', '10d累计新增3km缓冲区', '10d累计新增5km缓冲区']]


# 进行正向归一化


def positive_normalization(data_0):
    maxium = np.max(data_0, axis=0)
    minium = np.min(data_0, axis=0)
    data_00 = (data_0-minium)*1.0/(maxium-minium)
    return data_00

# 进行负向归一化


def negative_normalization(data_1):
    maxium = np.max(data_1, axis=0)
    minium = np.min(data_1, axis=0)
    data_11 = (data_1-maxium)*1.0/(maxium-minium)
    return data_11


print("--------------")

data_max_1 = positive_normalization(data_max)
print(data_max_1)
# ap.AddMessage(data_max_1)

print("--------------")

data_min_1 = negative_normalization(data_min)
print(data_min_1)

# 将归一化结果纳入一个dataframe中
data_all = pd.concat([data_max_1, data_min_1], axis=1)
data_all_to_array = data_all.values  # dataframe转化成array,方便使用numpy库函数进行熵值的运算
# ap.AddMessage(data_max_1)

# 计算熵值


def entropy(data0):
    n, m = np.shape(data0)  # 样本数，指标个数
    sumzb = np.sum(data0, axis=0)  # axis=0表达列，axis=1表达行
    data0 = data0/sumzb

    # 对ln0处理
    a = data0*1.0
    a[np.where(data0 == 0)] = 1E-6
    # ap.AddMessage(a)

    # 计算每个指标的熵
    e = (-1.0/np.log(n))*np.sum(data0*np.log(a), axis=0)  # 求熵值
    # ap.AddMessage(e)

    # 计算权重
    w = (1-e)/np.sum(1-e)
    # ap.AddMessage(w)

    return w


grades = entropy(data_all_to_array)
print(grades)  # 指标熵权法得分
ap.AddMessage(grades)
print('-------------------')

# 计算各地区脆弱性/危险性得分

# 将各地区数据进行正向归一化处理
data_grid = pd.concat([data_max, data_min], axis=1)
data_grid_to_array = data_grid.values
max = np.max(data_grid_to_array, axis=0)
min = np.min(data_grid_to_array, axis=0)
dataNormalize = (data_grid_to_array-min)*1.0/(max-min)

score_grid = np.dot(dataNormalize, grades)
print(score_grid)
ap.AddMessage(score_grid)

ap.AddField_management(city, "vulnerability", "DOUBLE")
with ap.da.UpdateCursor(city, ["vulnerability"]) as cursor:
    n = 1
    for row in cursor:
        row[0] = score_grid[n-1]
        cursor.updateRow(row)
        n += 1
ap.SetParameterAsText(2, city)

ap.analysis.SpatialJoin(grid, city, "gridSJvulnerability",
                        "JOIN_ONE_TO_ONE", "KEEP_ALL")
ap.management.JoinField(grid, "OBJECTID",
                        "gridSJvulnerability", "OBJECTID", "vulnerability")
ap.management.Delete("gridSJvulnerability")

ap.AddMessage("危险性已写入行政区图层")
