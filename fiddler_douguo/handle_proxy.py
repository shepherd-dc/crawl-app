import requests

# {"ip":"47.75.45.253","locale":""}
url = 'http://ip.hahado.cn/ip'
proxy = {'http':'http://163.204.247.172:9999'}
response = requests.get(url=url, proxies=proxy)
print(response.text)
