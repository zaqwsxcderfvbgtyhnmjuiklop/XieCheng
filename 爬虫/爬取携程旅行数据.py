import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing import Pool, Manager
from hdfs import InsecureClient
from lxml import etree


# 爬取携程旅行数据
class XieCheng:
    # 初始化全局变量
    def __init__(self):
        # 省份列表
        self.urls = []
        # 所有url
        self.urls_all = []


    def a(self):
        path = './data/urls.txt'
        if not os.path.exists(path):
            print('未找到文件，正在获取~')
            self.b()
            for i in self.urls:
                self.c(i, path)
        with open(path, "r", encoding="utf-8") as file:
            self.urls_all = [line.strip() for line in file.readlines()]

    def b(self):
        # 读取全国省份
        shengfen = pd.read_csv("./data/全国省份.txt")
        # 遍历拼接，获取具体网址
        for i in shengfen.values:
            url = 'https://vacations.ctrip.com/list/whole/sc206.html?st=%s&startcity=206&sv=%s' % (i[0], i[0])
            self.urls.append([url, i[0]])

    # url = [['https://vacations.ctrip.com/list/whole/sc2.html?st=湖北&startcity=2&sv=湖北', '湖北'], ['https://vacations.ctrip.com/list/whole/sc2.html?st=广东&startcity=2&sv=广东', '广东'], ['https://vacations.ctrip.com/list/whole/sc2.html?st=河南&startcity=2&sv=河南', '河南']]
    def c(self, url, path):
        ch_options = Options()
        ch_options.add_argument("--headless")
        ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        ch_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=ch_options)
        driver.implicitly_wait(20)
        while True:
            try:
                driver.get(url[0])
                break
            except:
                pass
        url1 = driver.current_url
        pages = driver.find_elements(by=By.XPATH, value='//div[@class="paging_item"]')[-1].text
        with open(path, 'a', encoding='utf-8') as f:
            f.write(url1 + ',' + url[1] + '\n')
            for i in range(2, int(pages) + 1):
                url2 = url1 + "&p=" + str(i)
                f.write(url2 + ',' + url[1] + '\n')
        driver.quit()

    # 一页爬取完毕后删除该页URL
    def d(self, url, lock):
        path = './data/urls.txt'
        with lock:
            with open(path, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                for line in lines:
                    if line.strip() != url:
                        file.write(line)

    # 打开网页
    def get_url(self, url, output_file, lock):
        ch_options = Options()
        ch_options.add_argument("--headless")
        ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        ch_options.add_experimental_option('useAutomationExtension', False)
        ch_options.add_argument("--disable-features=NetworkService")
        driver = webdriver.Chrome(options=ch_options)
        driver.implicitly_wait(20)

        for i in url:
            url2 = i.split(",")
            while True:
                try:
                    driver.get(url2[0])
                    time.sleep(2)
                    break
                except:
                    pass

            url3 = "https://verify.ctrip.com/static/ctripVerify.html"
            current_url = driver.current_url
            if current_url[:len(url3)] == url3:
                break

            print(current_url, url2[1])
            html = driver.page_source
            source = etree.HTML(html)
            self.jiexi(source, url2[1], output_file)
            time.sleep(1)
            self.d(i.strip(), lock)

    # 解析网页
    def jiexi(self, source, shengfen, output_file):
        data_all_list = source.xpath('//div[@class="list_product_right"]')
        for i in data_all_list:
            self.jiexi2(i, shengfen, output_file)

    # 解析
    def jiexi2(self, source, shengfen, output_file):
        # 标题
        title = source.xpath('.//p[@class="list_product_title"]/@title')[0]

        # 星级
        x = source.xpath('.//img/@alt')
        if len(x) == 0:
            xingji = "暂无星级"
        else:
            xingji = x[0]

        # 简介
        f = source.xpath('.//p[@class="list_product_subtitle"]/@title')
        if len(f) == 0:
            jianjie = "暂无简介"
        else:
            jianjie = f[0]
        jianjie = jianjie.replace("\n","")

        # 标签
        biaoqian = ""
        biaoqian_list = source.xpath('.//div[@class="list_label_box"]/span//text()')
        for j in biaoqian_list:
            biaoqian = biaoqian + ' ' + j
        if len(biaoqian_list) == 0:
            biaoqian = "暂无标签"
        biaoqian = biaoqian.strip()

        # 供应商
        e = source.xpath('.//p[@class="list_product_retail"]//text()')
        if len(e) == 0:
            gongyingshang = "暂无供应商"
        else:
            gongyingshang = e[-1].replace("供应商：", "")

        # 评分
        a = source.xpath('.//span[@class="list_product_score"]//text()')
        if len(a) == 0:
            pingfen = "暂无评分"
        else:
            pingfen = a[0]

        # 销售
        b = source.xpath('.//span[@class="list_product_travel"]/text()')
        if len(b) == 0:
            xiaoshou = "暂无销售"
        else:
            xiaoshou = b[0]

        # 评论
        c = source.xpath('.//span[@class="list_product_comment"]/text()')
        if len(c) == 0:
            pinglun = "暂无评论"
        else:
            pinglun = c[0]

        # 价格
        jiage = source.xpath('.//div[@class="list_sr_price"]//strong/text()')[0]

        data_all = [title, xingji, jianjie, biaoqian, gongyingshang, pingfen, xiaoshou, pinglun, jiage, shengfen]
        self.save_hdfs(data_all, output_file)

    def save_hdfs(self, data, output_file):
        data_str = "~-~-~".join(data) + "\n"
        # print(data_str)
        hdfs_client = InsecureClient('http://bigdata1:9870', user='root')
        hdfs_path = f'/sss/{output_file}'

        if not hdfs_client.status(hdfs_path, strict=False):
            # 如果文件不存在，创建一个新文件并写入数据
            with hdfs_client.write(hdfs_path, overwrite=False) as writer:
                writer.write(data_str.encode('utf-8'))
        else:
            # 如果文件已经存在，打开文件并追加写入数据
            with hdfs_client.write(hdfs_path, overwrite=False, append=True) as writer:
                writer.write(data_str.encode('utf-8'))

    # 运行函数
    def run(self):
        self.a()
        # 创建进程池
        num_processes = 16
        if len(self.urls_all) < num_processes:
            num_processes = len(self.urls_all)
        pool = Pool(processes=num_processes)

        # 将URL列表均匀分配给各个进程
        chunk_size = len(self.urls_all) // num_processes
        url_chunks = [self.urls_all[i:i + chunk_size] for i in range(0, len(self.urls_all), chunk_size)]

        with Manager() as manager:
            lock = manager.Lock()

            for i, url_chunk in enumerate(url_chunks):
                # 为每个进程分配唯一的文件名
                output_file = f'data_{i}.txt'
                pool.apply_async(self.get_url, args=(url_chunk, output_file, lock))

            pool.close()
            pool.join()

if __name__ == "__main__":
    x = XieCheng()
    x.run()
