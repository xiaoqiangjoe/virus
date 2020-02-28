import urlfetch
import json


import requests
import json
# 抓取数据

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts'
res = requests.get(url).json()




# 解析JSON数据
data = res['data']
data2 = json.loads(data)


# 数据根据日期排序
data2.sort(key=lambda x: x['date'])
# 构造数据集 （日期，确诊，疑似，死亡，治愈）
outall = ''
for i in range(0, len(data2)):
    if i != (len(data2) - 1):
        outstr = '\t\t\t\t\t[\'' + str(data2[i]['date']) + '\', ' + str(data2[i]['confirm']) + ', ' + str(
            data2[i]['suspect']) + ', ' + str(data2[i]['dead']) + ', ' + str(data2[i]['heal']) + '],\n'
    else:
        outstr = ''
        # 当天的数据通常不准确，暂时不绘制在图中
        # outstr = '\t\t\t\t\t[\''+ str(data2[i]['date']) + '\', '+str(data2[i]['confirm'])+', '+str(data2[i]['suspect'])+', '+str(data2[i]['dead'])+', '+str(data2[i]['heal'])+']\n'
    outall = outall + outstr

# 获取确诊、疑似数据的最大值
maxOne1 = sorted(data2, key=lambda x: int(x['confirm']), reverse=True)
maxOne2 = sorted(data2, key=lambda x: int(x['suspect']), reverse=True)
maxOne = max([int(maxOne1[0]['confirm']), int(maxOne2[0]['suspect'])])
# 获取死亡、治愈数据的最大值
maxTwo1 = sorted(data2, key=lambda x: int(x['dead']), reverse=True)
maxTwo2 = sorted(data2, key=lambda x: int(x['heal']), reverse=True)
maxTwo = max([int(maxTwo1[0]['dead']), int(maxTwo2[0]['heal'])])

# 读取模板HTML
fid = open('Temp.html', 'rb')
oriStr = fid.read().decode('utf-8')
fid.close()
# 写入数据集
modifiedStr = oriStr.replace('//dataInsert//', outall)

# 写入线图和柱图的Y轴最大值和分隔区间
interval1 = int(int(maxOne) / 1000) + 1
interval2 = int(float(maxTwo) / (interval1)) + 1
modifiedStr = modifiedStr.replace('//maxOne//', str(int(interval1 * 1000)))
modifiedStr = modifiedStr.replace('//intervalOne//', '1000')
modifiedStr = modifiedStr.replace('//maxTwo//', str(int(interval2 * interval1)))
modifiedStr = modifiedStr.replace('//intervalTwo//', str(interval2))
# 输出更新后的HTML
fid = open('Modified.html', 'wb')
fid.write(modifiedStr.encode('utf-8'))
fid.close()
