import requests
import csv
from lxml import html

is_test = False

#模拟浏览器请求头
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
#要补充的根网址
TOP_URL = "https://cyber.nankai.edu.cn"
#所有要遍历的网址
URLS = ["https://cyber.nankai.edu.cn/jswyjy/list.htm","https://cyber.nankai.edu.cn/fjswfyjy/list.htm","https://cyber.nankai.edu.cn/js/list.htm"]

def get_info(teacher_information_url):
                #teacher_info_response是教师单人介绍网址返回的信息
    teacher_info_response = requests.get(teacher_information_url,headers=HEADERS,timeout=60)
    teacher_info_response.encoding = "utf-8"
        #teacher_info_document是教师单人介绍网址xpath文档树
    teacher_info_document = html.fromstring(teacher_info_response.text)
        #teacher_basic_info_list是老师基本信息中每一小项的所有xpath文档树
    teacher_basic_info_list = teacher_info_document.xpath("//div[@class='form col-md-7']/p")
        #teacher_personal_profile中存储的是老师个人简介的所有信息的xpath文档树
    teacher_personal_profile = teacher_info_document.xpath("//div[@class='introduce-form' and @id='PersonalProfile']//div[@class='text']")[0]
        #teacher_personal_profile_full_text中储存的是老师个人简介文档树中的所有文本（纯文本）
    teacher_personal_profile_full_text = teacher_personal_profile.text_content().strip()

        #teacher_info_list存储的是老师的基本信息的每一项和个人简介文本
    teacher_info_list = []
    teacher_info_dict = {}
        #teacher_basic_info中存储的是老师基本信息中某一小项的xpath文档树
    for teacher_basic_info in teacher_basic_info_list:
        teacher_info_list.append(teacher_basic_info.xpath("./span[2]")[0].text_content().strip())

    teacher_info_list.append(teacher_personal_profile_full_text)

    #测试
    if is_test:
        print(teacher_info_list)

    return teacher_info_list

def save_csv(all_teachers_info_list):

    csv_header = ["姓名","性别","所属部门","行政职务","职称","学历","所学专业","办公电话","电子邮件","研究方向","个人简介"]

    with open("D:/zjh/python/导师信息网络爬虫/教师信息.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(all_teachers_info_list)

    print("保存成功")

#主函数
def main():
    #all_teachers_info_list存储的是所有老师信息列表的列表
    all_teachers_info_list = []
    #0.遍历所有网址（URL表示现在正在发送请求的网址）
    for URL in URLS:

        #1.发送请求，获取教师数据

        print("正在请求：" + URL)

            #response表示请求网页返回的结果
        response = requests.get(URL,headers=HEADERS,timeout=60)

        #2.解析数据，获得教师列表
            #response_document是经过解析后的xpath文档树
            #response.text是网页返回结果的原始html文本
        response_document = html.fromstring(response.text)
            #teacher_list是所有老师信息的xpath文档树的列表
        teacher_list = response_document.xpath("//div[@class='img-card']")

        teacher_num = len(teacher_list)

        print("该网址共有" + str(teacher_num) + "位老师")

        #3.遍历教师列表，获取教师信息
            #teacher是每一个老师信息的xpath文档树
        for teacher in teacher_list:

            current_teacher_num = teacher_list.index(teacher) + 1 

            print("正在请求第" + str(current_teacher_num) + "/" + str(teacher_num) + "位老师信息")

            teacher_url = teacher.xpath(".//a/@href")
                #teacher_information_url是每个老师专属介绍界面的url网址
            teacher_information_url = TOP_URL + teacher_url[0] if (("http://cyber-backend.nankai.edu.cn" not in teacher_url[0]) and teacher_url) else teacher_url[0]
            
            #测试
            if is_test:
                print(teacher_information_url)

            teacher_info_list = get_info(teacher_information_url)

            all_teachers_info_list.append(teacher_info_list)

    #4.保存在csv中

    print("保存数据中...")

    save_csv(all_teachers_info_list)

if __name__ == "__main__":
    main()