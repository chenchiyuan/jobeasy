# -*- coding: utf-8 -*-
# __author__ = chenchiyuan
# 通过POI名来判重, 必须内网跑

from __future__ import division, unicode_literals, print_function
import requests
import json
import base64


class ExcelHelper(object):
    @classmethod
    def write(cls, path, data, encoding="utf-8"):
        import xlwt
        workbook = xlwt.Workbook(encoding)
        worksheet = workbook.add_sheet('sheet1')

        for i, line in enumerate(data):
            for j, text in enumerate(line):
                worksheet.write(i, j, label=text)
        workbook.save(path)

    @classmethod
    def read(cls, path):
        import xlrd
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheets()[0]
        for row in range(1, sheet.nrows):
            yield sheet.cell(row, 0).value, sheet.cell(row, 1).value.strip()


def get_data(url):
    headers = {
        "host": "place.map.baidu.com",
    }
    r = requests.get(url, headers=headers)
    return r.content


def name_to_bid(name):
    url = "http://api.map.baidu.com/?qt=s&wd=%s&rn=10&ie=utf-8&oue=1&res=api&c=131" % name
    data = json.loads(get_data(url))
    try:
        result = data['content'][0]['primary_uid']
    except Exception:
        try:
            hot_city = data['content'][0]['code']
        except:
            print(url)
            raise Exception()
        url = "http://api.map.baidu.com/?qt=s&wd=%s&rn=10&ie=utf-8&oue=1&res=api&c=%s" % (name, hot_city)
        data = json.loads(get_data(url))
        try:
            result = data['content'][0]['primary_uid']
        except:
            print(url)
            raise Exception()
    return result


def call_curl(url):
    import subprocess
    proc = subprocess.Popen(["curl", "--header", 'Host: place.map.baidu.com', url], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out


def get_poi(x, y):
    url = "http://api.map.baidu.com/ag/coord/convert?from=5&to=2&x=%s&y=%s" % (x, y)
    json_data = json.loads(get_data(url))
    return base64.decodestring(json_data['x']), base64.decodestring(json_data['y'])


def gen_info(bid):
    url = "http://cq01-map-place00.cq01.baidu.com:8881/1/di/0/get.json?qt=13&nc=1&uid_list=%s" % bid
    json_data = json.loads(call_curl(url))
    data = json_data['data'][bid]
    name = data['name']
    address = data['address']
    phone = data['phone']
    city_name = data['city_name']
    x, y = get_poi(data['point_x'], data['point_y'])
    return {
        "name": name,
        "address": address,
        "phone": phone,
        "point_x": x,
        "point_y": y,
        "city_name": city_name
    }


def parse_name(name):
    bid = name_to_bid(name)
    return gen_info(bid)


def parse_names(path, names):
    data = []
    for data_id, name in names:
        try:
            info = parse_name(name)
            line = [data_id, info['name'], info['city_name'], info['address'], info['phone'], info['point_y'], info['point_x'], ]
        except Exception, err:
            line = [data_id, name, "", "", "", "", ""]
        data.append(line)
    ExcelHelper.write(path, data)

if __name__ == "__main__":
    from_path = "/Users/shadow/Desktop/imax.xlsx"
    to_path = "//Users/shadow/Desktop/result.xlsx"

    names = ExcelHelper.read(from_path)
    parse_names(to_path, names)
