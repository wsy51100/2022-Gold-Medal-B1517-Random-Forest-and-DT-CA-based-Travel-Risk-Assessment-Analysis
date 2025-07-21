from ast import alias
import requests
import datetime
from lxml import etree

# if __name__ == '__main__':
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
#     }
#     url_listSHA = ['http://sh.bendibao.com/news/2022624/254430.shtm', 'http://sh.bendibao.com/news/2022623/254323.shtm', 'http://sh.bendibao.com/news/2022622/254257.shtm', 'http://sh.bendibao.com/news/2022621/254182.shtm', 'http://sh.bendibao.com/news/2022620/254089.shtm', 'http://sh.bendibao.com/news/2022619/254080.shtm', 'http://sh.bendibao.com/news/2022618/254070.shtm', 'http://sh.bendibao.com/news/2022617/253997.shtm', 'http://sh.bendibao.com/news/2022616/253912.shtm', 'http://sh.bendibao.com/news/2022615/253837.shtm', 'http://sh.bendibao.com/news/2022614/253732.shtm', 'http://sh.bendibao.com/news/2022613/253653.shtm', 'http://sh.bendibao.com/news/2022612/253626.shtm', 'http://sh.bendibao.com/news/2022612/253632.shtm', 'http://sh.bendibao.com/news/2022610/253545.shtm', 'http://sh.bendibao.com/news/202269/253454.shtm', 'http://sh.bendibao.com/news/202268/253392.shtm', 'http://sh.bendibao.com/news/202267/253323.shtm', 'http://sh.bendibao.com/news/202266/253254.shtm', 'http://sh.bendibao.com/news/202266/253228.shtm', 'http://sh.bendibao.com/news/202265/253216.shtm', 'http://sh.bendibao.com/news/202265/253215.shtm', 'http://sh.bendibao.com/news/202262/253147.shtm', 'http://sh.bendibao.com/news/202261/253045.shtm', 'http://sh.bendibao.com/news/2022531/252973.shtm', 'http://sh.bendibao.com/news/2022530/252870.shtm', 'http://sh.bendibao.com/news/2022529/252856.shtm', 'http://sh.bendibao.com/news/2022529/252849.shtm', 'http://sh.bendibao.com/news/2022527/252812.shtm', 'http://sh.bendibao.com/news/2022526/252752.shtm', 'http://sh.bendibao.com/news/2022526/252752.shtm', 'http://sh.bendibao.com/news/2022525/252673.shtm', 'http://sh.bendibao.com/news/2022524/252605.shtm', 'http://sh.bendibao.com/news/2022523/252554.shtm', 'http://sh.bendibao.com/news/2022523/252529.shtm', 'http://sh.bendibao.com/news/2022522/252518.shtm', 'http://sh.bendibao.com/news/2022520/252466.shtm', 'http://sh.bendibao.com/news/2022519/252409.shtm', 'http://sh.bendibao.com/news/2022518/252345.shtm', 'http://sh.bendibao.com/news/2022518/252345.shtm', 'http://sh.bendibao.com/news/2022517/252314.shtm', 'http://sh.bendibao.com/news/2022516/252276.shtm', 'http://sh.bendibao.com/news/2022516/252276.shtm', 'http://sh.bendibao.com/news/2022515/252260.shtm', 'http://sh.bendibao.com/news/2022514/252256.shtm', 'http://m.sh.bendibao.com/news/252218.html', 'http://m.sh.bendibao.com/news/252157.html', 'http://sh.bendibao.com/news/2022511/252093.shtm',
#                 'http://m.sh.bendibao.com/news/252025.html', 'http://sh.bendibao.com/news/202259/251979.shtm', 'http://m.sh.bendibao.com/news/251966.html', 'http://sh.bendibao.com/news/202257/251913.shtm', 'http://sh.bendibao.com/news/202256/251847.shtm', 'http://sh.bendibao.com/news/202255/251747.shtm', 'http://sh.bendibao.com/news/202254/251725.shtm', 'http://sh.bendibao.com/news/202253/251722.shtm', 'http://sh.bendibao.com/news/202252/251718.shtm', 'http://sh.bendibao.com/news/202251/251711.shtm', 'http://sh.bendibao.com/news/2022430/251705.shtm', 'http://sh.bendibao.com/news/2022429/251668.shtm', 'http://sh.bendibao.com/news/2022428/251570.shtm', 'http://sh.bendibao.com/news/2022427/251522.shtm', 'http://sh.bendibao.com/news/2022426/251483.shtm', 'http://sh.bendibao.com/news/2022425/251427.shtm', 'http://sh.bendibao.com/news/2022424/251365.shtm', 'http://sh.bendibao.com/news/2022423/251358.shtm', 'http://sh.bendibao.com/news/2022422/251322.shtm', 'http://sh.bendibao.com/news/2022421/251262.shtm', 'http://sh.bendibao.com/news/2022420/251224.shtm', 'http://sh.bendibao.com/news/2022419/251160.shtm', 'http://sh.bendibao.com/news/2022418/251098.shtm', 'http://sh.bendibao.com/news/2022418/251082.shtm', 'http://sh.bendibao.com/news/2022416/251076.shtm', 'http://sh.bendibao.com/news/2022415/251002.shtm', 'http://sh.bendibao.com/news/2022414/250929.shtm', 'http://sh.bendibao.com/news/2022413/250859.shtm', 'http://sh.bendibao.com/news/2022412/250825.shtm', 'http://sh.bendibao.com/news/2022411/250787.shtm', 'http://sh.bendibao.com/news/2022411/250789.shtm', 'http://sh.bendibao.com/news/2022411/250790.shtm', 'http://sh.bendibao.com/news/202248/250732.shtm', 'http://sh.bendibao.com/news/202247/250665.shtm', 'http://sh.bendibao.com/news/202241/250451.shtm', 'http://sh.bendibao.com/news/2022331/250395.shtm', 'http://sh.bendibao.com/news/2022330/250337.shtm', 'http://sh.bendibao.com/news/2022329/250291.shtm', 'http://sh.bendibao.com/news/2022328/250240.shtm', 'http://sh.bendibao.com/news/2022327/250213.shtm', 'http://sh.bendibao.com/news/2022326/250197.shtm', 'http://sh.bendibao.com/news/2022325/250141.shtm', 'http://sh.bendibao.com/news/2022324/250089.shtm', 'http://sh.bendibao.com/news/2022323/250043.shtm', 'http://sh.bendibao.com/news/2022322/249994.shtm', 'http://sh.bendibao.com/news/2022321/249948.shtm', 'http://sh.bendibao.com/news/2022320/249923.shtm', 'http://sh.bendibao.com/news/2022319/249914.shtm']

#     tmp_date = "20220624"#上海
#     # 前任意天

#     for i in range(len(url_listSHA)):
#         date = (datetime.datetime.strptime(tmp_date, "%Y%m%d") -
#                     datetime.timedelta(days=i+1)).strftime("%Y%m%d")

#         page_text = requests.get(
#             url=url_listSHA[i], headers=headers).content.decode('utf-8')
#         tree = etree.HTML(page_text)
#         a_list = tree.xpath('//div[@class="content"]/p')
#         fp = open('./病例地址上海/'+str(date)+'上海.txt', 'w', encoding='utf-8')

#         for a in a_list:
#             text = a.xpath('.//text()')
#             pText = '\u3000'.join(text).strip()

#             if pText[-1:] == "区" or pText[2:3] == "区" or pText[2:4] == "新区":
#                 fp.write('\n'+pText+'\n')
#                 continue
#             if pText[-3:] == "如下。" or pText[-3:] == "一览表" or pText[:3] == "已对相" or pText[:3] == "ps：" or pText[-4:] == "居住于：" or pText[-3:] == "居住于":
#                 continue
#             if pText[:6] == "上海市卫健委":
#                 pText = pText[6:11]
#                 fp.write(pText+'\n')
#                 continue
#             if pText == "相关推荐：" or pText == "手机访问　 　上海本地宝首页" or pText == "上海新增病例居住地汇总表(持续更新)":
#                 continue
#             else:
#                 fp.write(pText+'\n')
#         print('爬取'+str(date)+'成功')


# if __name__ == '__main__':
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
#     }
#     url_listPEK = ['http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220619_2745238.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220618_2745085.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220617_2743440.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220616_2741925.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220615_2740433.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220614_2739116.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220613_2737964.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220612_2737849.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220611_2735215.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220610_2733539.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220609_2732640.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220608_2731699.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220607_2730742.html',
#                    'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220606_2729410.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220605_2729261.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220604_2729079.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220430_2696329.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220602_2727106.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202206/t20220601_2725888.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220531_2724819.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220530_2723712.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220529_2723580.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220528_2723366.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220527_2722161.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220526_2721143.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220525_2720038.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220524_2719044.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220523_2718194.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220522_2718043.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220521_2717868.html',
#                    'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220520_2716756.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220519_2715938.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220518_2715057.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220517_2711647.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220516_2710750.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220515_2710080.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220514_2709812.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220513_2708903.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220512_2707726.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220511_2706802.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220510_2705803.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220509_2704752.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220508_2704488.html',
#                    'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220507_2703271.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220506_2702173.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220505_2700124.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220504_2699885.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220503_2699681.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220502_2699521.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202205/t20220501_2699140.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220430_2698894.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220429_2696329.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220428_2694913.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220427_2693371.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220426_2691803.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220425_2688777.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220424_2686947.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220423_2686701.html', 'http://wjw.beijing.gov.cn/xwzx_20031/rdxws/202204/t20220422_2685239.html']

#     tmp_date = "20220618"  # 北京
#     #0429需手动复制
#     #0602无疫情
#     for i in range(len(url_listPEK)):

#         date = (datetime.datetime.strptime(tmp_date, "%Y%m%d") -
#                 datetime.timedelta(days=i)).strftime("%Y%m%d")
#         # if date=='20220602':
#         #     date = (datetime.datetime.strptime(tmp_date, "%Y%m%d") -
#         #         datetime.timedelta(days=i+1)).strftime("%Y%m%d")
#         #     tmp_date = "20220617"

#         page_text = requests.get(
#             url=url_listPEK[i], headers=headers).content.decode('utf-8')
#         tree = etree.HTML(page_text)
#         a_list = tree.xpath('//div[@class="view TRS_UEDITOR trs_paper_default trs_word trs_key4format"]/p | //div[@class="view TRS_UEDITOR trs_paper_default trs_web trs_key4format trs_word"]/p | //div[@class="view TRS_UEDITOR trs_paper_default trs_word trs_web trs_key4format"]/p | //div[@class="view TRS_UEDITOR trs_paper_default trs_word trs_key4format trs_web"]/p | //div[@class="article"]/div/p')
#         fp = open('./病例地址北京/'+str(date)+'北京.txt', 'w', encoding='utf-8')

#         del a_list[-2:]

        # for a in a_list:
        #     text = a.xpath('.//text()')
        #     pText = '\u3000'.join(text).strip()

        #     if pText[-6:] == "输入疫情以来" or pText[-5:] == "防控措施。":
        #         continue
        #     if pText[:6] == "上述病例均已" or pText[-6:] == "病例天数情况":
        #         # pText = pText[6:11]
        #         # fp.write(pText+'\n')
        #         continue
        #     if pText == "境外输入确诊病例来源国（地区）情况" or pText == "上海新增病例居住地汇总表(持续更新)":
        #         continue
        #     else:
        #         fp.write(pText+'\n')
        #     print('爬取第'+str(len(url_listPEK)-i)+'天'+str(date)+'成功')
        # print('爬取完成')

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    url_listCAN = ['http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8274677.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8258320.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8232210.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8230186.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8228466.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8227896.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8226601.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8224702.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8222694.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8221991.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8221862.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8221797.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8221673.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8221526.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8218991.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8216801.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8215010.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8213057.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8211205.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8209178.html',
                   'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8208886.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8207223.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8205373.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8202553.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8200796.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8192299.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8191668.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8191370.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8187971.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8185645.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8182642.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8179813.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8177800.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8176931.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8176571.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8174641.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8172638.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8170880.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8170246.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8170121.html', 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/content/post_8169953.html']

    tmp_date = "20220512"  # 广州
    #0406 0427无本土病例
    for i in range(len(url_listCAN)):

        date = (datetime.datetime.strptime(tmp_date, "%Y%m%d") -
                datetime.timedelta(days=i)).strftime("%Y%m%d")

        page_text = requests.get(
            url=url_listCAN[i], headers=headers).content.decode('utf-8')
        tree = etree.HTML(page_text)
        a_list = tree.xpath('//div[@class="zoom_box"]/p')
        fp = open('./病例地址广州/'+str(date)+'广州.txt', 'w', encoding='utf-8')

        a_list.pop(0)
        a_list.pop()

        for a in a_list:
            text = a.xpath('.//text()') 
            pText = '\u3000'.join(text).strip()

            if pText[-12:] == "境外输入无症状感染者情况" or pText[:10] == "境外输入无症状感染者" or pText[:8] == "境外输入确诊病例":
                continue
            if pText[:6] == "上述确诊病例" or pText[:6] == "上述境外输入" or pText[:4] == "境外输入":
                continue
            if pText[:2] == "截至":
                continue
            else:
                fp.write(pText+'\n')

        print('爬取第'+str(len(url_listCAN)-i)+'天'+str(date)+'成功')
    print('爬取完成')
