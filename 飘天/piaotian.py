import requests
import re
from bs4 import BeautifulSoup
def getHtml(url):
    try:
        request = requests.get(url)
        html = request.text
    except:
        html = ""
    return html

def getDirectory(baseUrl):

    html = getHtml(baseUrl)
    pattern = "<li><a href=\"(.*)\">(.*)</a>"
    result = re.findall(pattern,html)

    directory = {}
    for tumple in result:
        url = baseUrl+tumple[0]
        directory[tumple[1]] = url

    return directory

def getContent(url):
    html = getHtml(url)
    if html == "":
        return ""
    soup = BeautifulSoup(html,'lxml')
    result = soup.find_all(text=re.compile("[\u4e00-\u9fa5]"))
    return result

def main():
    baseUrl = "https://www.piaotian.com/html/5/5623/"
    directory = getDirectory(baseUrl)
    file = open("永夜君王.txt","w")
    count = 0
    for item in directory.items():
        if count < 4 :
            count += 1
            continue
        file.write(item[0])
        print(item[0])
        content = getContent(item[1])[20:-23]
        for line in content:
            file.write(line+"\n")
    file.close()

if __name__ == '__main__':

    main()
