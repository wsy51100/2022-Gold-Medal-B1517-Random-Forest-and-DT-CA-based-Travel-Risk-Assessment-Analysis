import os
import math
import openpyxl
import pandas as pd
import numpy as np
import arcpy as ap

dignoseLayer = ap.GetParameterAsText(0)  # 病例点图层
girdLayer = ap.GetParameterAsText(1)  # 格网图层
bufferLayer = ap.GetParameterAsText(2)  # 缓冲区图层
workspace = ap.GetParameterAsText(3)  # 储存空间
city = ap.GetParameterAsText(4)  # 行政区图层（注意顺序）
mrate = ap.GetParameterAsText(5)  # 百万确诊比

ap.env.workspace = workspace

# 若在组图层去除"\",用于命名；作为路径则保持不变
cityPathIG = city
if "\\" in city:
    city = city.split("\\")[0]


def GetFieldUniqueValue(inTable):  # 获取字段唯一值
    value_list = []
    rows = ap.da.SearchCursor(inTable, ["timeInt"])
    for row in rows:
        if row[0] not in value_list:
            value_list.append(row[0])
    del row
    del rows
    return value_list


def date(stamp):  # 日期-时间戳
    delta = pd.Timedelta(str(stamp)+'D')
    real_time = pd.to_datetime('1899-12-30', format='%Y-%m-%d') + delta
    return real_time


def cityname(city):
    if str(city) == "SZ":
        return "深圳市"
    if str(city) == "GZ":
        return "广州市"
    if str(city) == "SH":
        return "上海市"
    if str(city) == "BJ":
        return "北京市"


def cityname2(city):
    if str(city) == "SZ":
        return "深圳"
    if str(city) == "GZ":
        return "广州"
    if str(city) == "SH":
        return "上海"
    if str(city) == "BJ":
        return "北京"


def positive_normalization(data_0):  # 归一化
    maxium = np.max(data_0, axis=0)
    minium = np.min(data_0, axis=0)
    data_00 = (data_0-minium)*1.0/(maxium-minium)
    return data_00


def clearSelect(layer):  # 清除选择
    ap.management.SelectLayerByAttribute(layer, "CLEAR_SELECTION")


df = pd.read_csv(mrate, names=None)  # utf8-csv
df_li = df.values.tolist()

clearSelect(dignoseLayer)
timeList = GetFieldUniqueValue(dignoseLayer)

# ap.AddMessage(len(timeList))
ap.AddMessage("共有"+str(math.floor(len(timeList)/10))+"个图层")

# for i in range(1, 2):
for i in range(math.floor(len(timeList)/10)+1):
    if i == 0:
        continue
        ap.AddMessage("开始处理"+city+"总体情况")

    else:
        CTLayer = str(city)+str(timeList[(i-1)*10+9])
        csvFloder = r"csv\\"

        ap.AddMessage("开始写入"+city+str(date(str(timeList[(i-1)*10+9])))+"病例数据")
        # 百万确诊比
        ap.management.CopyFeatures(
            cityPathIG, city+str(timeList[(i-1)*10+9])+"mRate")
        ap.AddField_management(
            city+str(timeList[(i-1)*10+9])+"mRate", "mRate", "DOUBLE")
        # 写入百万确诊比例
        with ap.da.UpdateCursor(city+str(timeList[(i-1)*10+9])+"mRate", ["mRate"]) as cursor:
            n = 1
            ap.AddMessage(df_li)

            for row in cursor:
                ap.AddMessage(row)
                
                row[0] = df_li[(i-1)*10+9][n]
                cursor.updateRow(row)
                n += 1
        ap.analysis.SpatialJoin(girdLayer, city+str(timeList[(i-1)*10+9])+"mRate", str(city) +
                                str(timeList[(i-1)*10+9]), "JOIN_ONE_TO_ONE", "KEEP_ALL")

        # 删除多余字段
        fieldDelete = ["timeInt", "区县", "街道", "省", "市", "地址", "时间", "POINT_X", "Join_Count", "Join_Count", "vulnerability_1"
                       "POINT_Y", "脆弱性", "Shape_Leng", "Shape_Length_1", "Shape_Area_1", "TARGET_FID"]
        for j in range(len(fieldDelete)):
            ap.management.DeleteField(
                CTLayer, fieldDelete[j])

        # 按属性查询10d，从第10日开始
        qr = '"timeInt"='+str(timeList[(i-1)*10-1])+'OR "timeInt"=' + \
            str(timeList[(i-1)*10+9])+'OR "timeInt"='+str(timeList[(i-1)*10+8])+'OR "timeInt"='+str(timeList[(i-1)*10+7])+'OR "timeInt"='+str(timeList[(i-1)*10+6]) + \
            'OR "timeInt"='+str(timeList[(i-1)*10+5])+'OR "timeInt"='+str(timeList[(i-1)*10+4])+'OR "timeInt"='+str(
                timeList[(i-1)*10+3])+'OR "timeInt"='+str(timeList[(i-1)*10+2])+'OR "timeInt"='+str(timeList[(i-1)*10+1])+'OR "timeInt"='+str(timeList[(i-1)*10])
        ap.management.SelectLayerByAttribute(dignoseLayer, "NEW_SELECTION", qr)
        ap.analysis.SpatialJoin(girdLayer, dignoseLayer,
                                CTLayer+"10d", "JOIN_ONE_TO_ONE", "KEEP_ALL")
        # 字段改名、连接字段
        ap.management.AlterField(
            CTLayer+"10d", "Join_Count", "dig10d", "dig10d")
        ap.management.JoinField(CTLayer, "OBJECTID",
                                CTLayer+"10d", "OBJECTID", "dig10d")

        # 缓冲区空间连接病例点
        ap.analysis.SpatialJoin(
            bufferLayer, dignoseLayer, CTLayer+"Buffer", "JOIN_ONE_TO_ONE", "KEEP_ALL")

        ap.analysis.SplitByAttributes(
            CTLayer+"Buffer", workspace, "distance")

        # 单独选择3000/5000进行连接
        ap.management.JoinField(
            CTLayer, "OBJECTID",  "T3000_0", "OBJECTID", "Join_Count")
        ap.management.AlterField(
            CTLayer, "Join_Count", "dig10dB3", "dig10dB3")

        ap.management.JoinField(
            CTLayer, "OBJECTID",  "T5000_0", "OBJECTID", "Join_Count")
        ap.management.AlterField(
            CTLayer, "Join_Count", "dig10dB5", "dig10dB5")

        clearSelect(dignoseLayer)

        # 删除要素
        ap.management.Delete("T3000_0")
        ap.management.Delete("T5000_0")
        ap.management.Delete(CTLayer+"10d")
        ap.management.Delete(CTLayer+"Buffer")
        ap.management.Delete(CTLayer+"mRate")

        ap.AddMessage("病例数据已写入"+city+str(date(str(timeList[(i-1)*10+9]))))

        # 归一化
        vars = ["dig10d", "dig10dB3", "dig10dB5", "mRate", "popDen", "roadDen", "vulnerability", cityname(city)+'旅游景点', cityname(city)+'交通设施', cityname(city)+'酒店住宿',
                cityname(city)+'生活服务', cityname(city)+'购物消费', cityname(city)+'商务住宅', cityname(
                               city)+'休闲娱乐', cityname(city)+'餐饮美食', cityname(city)+'运动健身',
                cityname(city)+'科教文化', cityname(city)+'公司企业', cityname(city)+'金融机构', cityname(city)+'汽车相关', cityname(city)+'医疗保健']
        ap.management.StandardizeField(CTLayer, vars, "MAXABS")

        # 随机森林
        ap.AddMessage("开始随机森林"+city+str(date(str(timeList[(i-1)*10+9]))))
        varsMA = ['dig10dB3_MAX_ABS', 'dig10dB5_MAX_ABS', 'mRate_MAX_ABS', 'popDen_MAX_ABS', 'roadDen_MAX_ABS', 'vulnerability_MAX_ABS', cityname(city) +
                  '旅游景点_MAX_ABS', cityname(city)+'交通设施_MAX_ABS', cityname(city)+'酒店住宿_MAX_ABS', cityname(city) +
                  '生活服务_MAX_ABS', cityname(city)+'购物消费_MAX_ABS', cityname(city)+'商务住宅_MAX_ABS', cityname(city)+'休闲娱乐_MAX_ABS', cityname(city) +
                  '餐饮美食_MAX_ABS', cityname(city)+'运动健身_MAX_ABS', cityname(city)+'科教文化_MAX_ABS', cityname(city)+'公司企业_MAX_ABS', cityname(city) +
                  '金融机构_MAX_ABS', cityname(city)+'汽车相关_MAX_ABS', cityname(city)+'医疗保健_MAX_ABS']
        ap.gapro.Forest("TRAIN", CTLayer, "RF_"+CTLayer, "dig10d", "", varsMA, "",
                        "imp"+CTLayer, "", "", "125", "", "", "100", "", "30")

        ap.AddMessage("随机森林"+city+str(date(str(timeList[(i-1)*10+9])))+"已完成")

        # 导出grid至csv
        if (os.path.exists(csvFloder+CTLayer+'.csv')):  # 检查文件是否存在
            os.remove(csvFloder+CTLayer+'.csv')
        ap.conversion.TableToTable(CTLayer, csvFloder, CTLayer+'.csv')

        # 计算网格风险值
        ap.AddMessage("开始计算"+city+str(date(str(timeList[(i-1)*10+9])))+"网格风险值")
        impTable = "imp"+CTLayer
        df = pd.read_csv(csvFloder+CTLayer+'.csv')

        with ap.da.SearchCursor(impTable, ["Variables", "Importance"]) as cursor:
            for impValue in cursor:  # 读取重要性值表格
                # impValue[0]字段 / impValue[1]重要性值

                for field in range(len(df.columns)):
                    if df.columns[field] == impValue[0]:
                        ap.AddMessage("正在计算"+impValue[0])
                        # ap.AddMessage("在第"+str(i)+"列")  # 第i列是要找的字段

                        for row in range(len(df)):
                            df.iloc[row, field] *= impValue[1]
        ap.AddMessage(df)
        df2 = df.drop(labels=['OID_', 'Shape_Length', 'Shape_Area', "dig10dB3", "dig10dB5", "mRate", "popDen", "roadDen", "vulnerability",
                              #   "vulnerability_1",
                              "vulnerability_MAX_ABS",  cityname(city) + '旅游景点', cityname(city) +
                              '交通设施', cityname(city)+'酒店住宿', cityname(city)+'生活服务', cityname(city) + '购物消费', cityname(city) +
                              '商务住宅', cityname(city)+'休闲娱乐', cityname(city)+'餐饮美食', cityname(city) + '运动健身', cityname(city) +
                              '科教文化', cityname(city)+'公司企业', cityname(city)+'金融机构', cityname(city) + '汽车相关', cityname(city) + '医疗保健'], axis=1)
        # df2 = df.drop(labels=['OID_', 'Shape_Length', 'Shape_Area', "dig10dB3", "dig10dB5", "mRate", "popDen",
        #               "roadDen", "vulnerability", "vulnerability_1", "vulnerability_MAX_ABS", "vulnerability_MAX_ABS1"], axis=1)

        # 每行求和
        df2['Index'] = df2.sum(axis=1)

        df2.to_csv(csvFloder+CTLayer+'Index.csv', encoding='utf-8-sig')

        ap.AddMessage("计算网格风险值"+city +
                      str(date(str(timeList[(i-1)*10+9])))+"已完成")

        ap.conversion.TableToTable(
            # csvFloder+CTLayer+'Index.csv', cityname2(city)+".gdb", CTLayer+'Index')
            csvFloder+CTLayer+'Index.csv', workspace, 'Index'+CTLayer)

        ap.management.JoinField(CTLayer, "OBJECTID",
                                'Index'+CTLayer, "OBJECTID", "Index")
        ap.AddMessage(
            "网格风险值"+city + str(date(str(timeList[(i-1)*10+9])))+"已写入属性表")
        ap.AddMessage("----------------------------------------")

        # 软件内调用UpdateCursor方法报错为乱码，考虑为编码问题
        # with ap.da.UpdateCursor(impTable, [impValue[0]]) as cursor1:
        #     for grid in cursor1:
        #         grid[0] *= impValue[1]
        #         cursor1.updateRow(grid)
