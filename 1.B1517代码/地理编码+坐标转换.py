import math
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlencode  # 编码 URL 字符串


# 高德CJ-02坐标系
def geoCoding(tblCompanyList):
    # 查询返回的形式+多个查询+Url头
    paras = {
        'output': 'json',
        'batch': 'true',
        'address': tblCompanyList,
        'key': "b4997590639f13530c08f841f4373a19"
    }
    url = 'https://restapi.amap.com/v3/geocode/geo?' + \
        urlencode(paras)

    # 提交+返回+解析Json
    response = requests.get(url)
    answer = response.json()

    # 用来存放地理编码结果的空序列
    resultList = []

    if answer['status'] == '1' and answer['info'] == 'OK':
        # 4.1-请求和返回都成功，则进行解析
        # 获取所有结果坐标点
        tmpList = answer['geocodes']
        for i in range(0, len(tmpList)):
            try:
                # 解析','分隔的经纬度
                coordString = tmpList[i]['location']
                coordList = coordString.split(',')
                # 放入结果序列
                resultList.append((float(coordList[0]), float(coordList[1])))
            except:
                # 如果发生错误则存入None
                resultList.append(None)
        return resultList
    elif answer['info'] == 'DAILY_QUERY_OVER_LIMIT':
        return -1  # 额度不足
    else:
        return -2  # 其他错误


# gcj02 -> wgs84
pi = 3.141592653589793234  # π
r_pi = pi * 3000.0 / 180.0
la = 6378245.0  # 长半轴
ob = 0.00669342162296594323  # 扁率


def transformLat(lon, lat):
    r = -100.0 + 2.0 * lon + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lon * lat + 0.2 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 *
          math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lat * pi) + 40.0 *
          math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
          math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return r


def transformLng(lon, lat):
    r = 300.0 + lon + 2.0 * lat + 0.1 * lon * lon + \
        0.1 * lon * lat + 0.1 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 *
          math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lon * pi) + 40.0 *
          math.sin(lon / 3.0 * pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(lon / 12.0 * pi) + 300.0 *
          math.sin(lon / 30.0 * pi)) * 2.0 / 3.0
    return r


def gcj02_wgs84(lon_gcj02, lat_gcj02):

    tlat = transformLat(lon_gcj02 - 105.0, lat_gcj02 - 35.0)
    tlng = transformLng(lon_gcj02 - 105.0, lat_gcj02 - 35.0)
    rlat = lat_gcj02 / 180.0 * pi
    m = math.sin(rlat)
    m = 1 - ob * m * m
    sm = math.sqrt(m)
    tlat = (tlat * 180.0) / ((la * (1 - ob)) / (m * sm) * pi)
    tlng = (tlng * 180.0) / (la / sm * math.cos(rlat) * pi)
    lat_wgs84 = 2 * lat_gcj02 - (lat_gcj02 + tlat)
    lon_wgs84 = 2 * lon_gcj02 - (lon_gcj02 + tlng)
    return [lon_wgs84, lat_wgs84]


def countPage(html):
    # 获取循环次数
    bs2 = BeautifulSoup(html, 'lxml')
    findNum = bs2.find_all('div', class_='public_tltie_one')[5]
    bs3 = BeautifulSoup(str(findNum), 'lxml')
    dataCount = bs3.find('strong').get_text()
    print("当前时间内有"+dataCount+'条数据')
    frequency = math.ceil(int(dataCount)/20)
    # frequency = int(int(dataCount)/20)+1
    print('需要循环'+str(frequency)+'次\n')
    return frequency


# 保存字段内容到本地
def writeToCSV(table, date, header):
    if(header == 0):
        table.to_csv(path_or_buf=r'C:\Users\Necko_Z\Desktop'+date+'.csv',
                     mode='a', encoding='GBK', index=False)
    else:
        table.to_csv(path_or_buf=r'C:\Users\Necko_Z\Desktop'+date+'.csv',
                     mode='a', encoding='GBK', index=False, header=False)  # 追加模式、国标、首列序号、重复表头


if __name__ == '__main__':
    # endTimes = ['2021-12-01']
    # for j in range(len(endTimes)):
    #     print('开始爬取'+endTimes[j]+'的数据')
    #     page = countPage(html)
    #     sTime = time.time()  # 计算程序运行时间
    #     for i in range(1, page+1):  # 分次爬取需要更改起始页码
    #         html = getPage(i, endTimes[j])  # 获取网页源代码
    #         companyDetail = analyzePage(html)  # 解析网页源代码
    #         if(i > 1):
    #             writeToCSV(companyDetail, endTimes[j], 1)  # 去header
    #         else:
    #             writeToCSV(companyDetail, endTimes[j], 0)

    #     eTime = time.time()-sTime
    #     print(endTimes[j]+'的数据爬取结束，用时%.2f秒\n' % eTime)