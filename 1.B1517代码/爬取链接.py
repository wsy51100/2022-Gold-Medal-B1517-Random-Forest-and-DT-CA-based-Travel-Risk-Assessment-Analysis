import requests
from lxml import etree

if __name__ == '__main__':
    url = 'http://wjw.sz.gov.cn/yqxx/index_17.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    page_text = requests.get(url=url, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page_text)
    a_list = tree.xpath('//div[@class="newsListRigth AllListCon"]/ul')
    fp = open('./temp.txt', 'w', encoding='utf-8')

    for a in a_list:
        text = a.xpath('//li/a/text()')
        pText = '\u3000'.join(text).strip()

        # if text[-11:]=="深圳市新冠肺炎疫情情况":


        date_href = a.xpath('//li/a/@href')
        pHref = '\u3000'.join(date_href).strip()
        fp.write(pText+'\n'+ pHref+'\n')

        # else:
        #     continue

    print('爬取成功')

