#!/usr/bin/env python
# coding: utf-8
# author: taoyang

import struct
from socket import inet_aton, inet_ntoa
import os
import sys

sys.setrecursionlimit(1000000)

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)


class IpTree:
    def __init__(self):
        self.ip_dict = {}
        self.country_codes = {}
        self.china_province_codes = {}
        self.china_city_codes = {}

    def load_country_codes(self, file_name):
        try:
            path = os.path.abspath(file_name)
            with open(path, "rb") as f:
                for line in f.readlines():
                    data = line.split('\t')
                    self.country_codes[data[0]] = data[1]
                    # print self.country_codes
        except Exception as ex:
            print "cannot open file %s: %s" % (file, ex)
            print ex.message
            exit(0)

    def load_china_province_codes(self, file_name):
        try:
            path = os.path.abspath(file_name)
            with open(path, "rb") as f:
                for line in f.readlines():
                    data = line.split('\t')
                    provinces = data[2].split('\r')
                    self.china_province_codes[provinces[0]] = data[0]
                    # print self.china_province_codes
        except Exception as ex:
            print "cannot open file %s: %s" % (file, ex)
            print ex.message
            exit(0)

    def load_china_city_codes(self, file_name):
        try:
            path = os.path.abspath(file_name)
            with open(path, "rb") as f:
                for line in f.readlines():
                    data = line.split('\t')
                    cities = data[3].split('\r')
                    self.china_city_codes[cities[0]] = data[0]
        except Exception as ex:
            print "cannot open file %s: %s" % (file, ex)
            print ex.message
            exit(0)

    def loadfile(self, file_name):
        try:
            ipdot0 = 254
            path = os.path.abspath(file_name)
            with open(path, "rb") as f:
                local_binary0 = f.read()
                local_offset, = _unpack_N(local_binary0[:4])
                local_binary = local_binary0[4:local_offset]
                # 256 nodes
                while ipdot0 >= 0:
                    middle_ip = None
                    middle_content = None
                    lis = []
                    # offset
                    begin_offset = ipdot0 * 4
                    end_offset = (ipdot0 + 1) * 4
                    # index
                    start_index, = _unpack_V(local_binary[begin_offset:begin_offset + 4])
                    start_index = start_index * 8 + 1024
                    end_index, = _unpack_V(local_binary[end_offset:end_offset + 4])
                    end_index = end_index * 8 + 1024
                    while start_index < end_index:
                        content_offset, = _unpack_V(local_binary[start_index + 4: start_index + 7] +
                                                    chr(0).encode('utf-8'))
                        content_length, = _unpack_C(local_binary[start_index + 7])
                        content_offset = local_offset + content_offset - 1024
                        content = local_binary0[content_offset:content_offset + content_length]
                        if middle_content != content and middle_content is not None:
                            contents = middle_content.split('\t')
                            lis.append((middle_ip, (contents[0], self.lookup_country_code(contents[0]),
                                                    contents[1], self.lookup_china_province_code(contents[1]),
                                                    contents[2], self.lookup_china_city_code(contents[2]),
                                                    contents[3], contents[4])))
                        middle_content, = content,
                        middle_ip = inet_ntoa(local_binary[start_index:start_index + 4])
                        start_index += 8
                    self.ip_dict[ipdot0] = self.generate_tree(lis)
                    ipdot0 -= 1
        except Exception as ex:
            print "cannot open file %s: %s" % (file, ex)
            print ex.message
            exit(0)

    def lookup_country(self, country_code):
        try:
            for item_country, item_country_code in self.country_codes.items():
                if country_code == item_country_code:
                    return item_country, item_country_code
            return 'None', 'None'
        except KeyError:
            return 'None', 'None'

    def lookup_country_code(self, country):
        try:
            return self.country_codes[country]
        except KeyError:
            return 'None'

    def lookup_china_province(self, province_code):
        try:
            for item_province, item_province_code, in self.china_province_codes.items():
                if province_code == item_province_code:
                    return item_province, item_province_code
            return 'None', 'None'
        except KeyError:
            return 'None', 'None'

    def lookup_china_province_code(self, province):
        try:
            return self.china_province_codes[province.encode('utf-8')]
        except KeyError:
            return 'None'

    def lookup_china_city(self, city_code):
        try:
            for item_city, item_city_code in self.china_city_codes.items():
                if city_code == item_city_code:
                    return item_city, item_city_code
            return 'None', 'None'
        except KeyError:
            return 'None', 'None'

    def lookup_china_city_code(self, city):
        try:
            return self.china_city_codes[city]
        except KeyError:
            return 'None'

    def lookup(self, ip):
        ipdot = ip.split('.')
        ipdot0 = int(ipdot[0])
        if ipdot0 < 0 or ipdot0 > 255 or len(ipdot) != 4:
            return None
        try:
            d = self.ip_dict[int(ipdot[0])]
        except KeyError:
            return None
        if d is not None:
            return self.lookup1(inet_aton(ip), d)
        else:
            return None

    def lookup1(self, net_ip, (net_ip1, content, lefts, rights)):
        if net_ip < net_ip1:
            if lefts is None:
                return {'country': content[0], 'country_code': content[1],
                        'province': content[2], 'province_code': content[3],
                        'city': content[4], 'city_code': content[5],
                        'organize': content[6], 'carrier': content[7]}
            else:
                return self.lookup1(net_ip, lefts)
        elif net_ip > net_ip1:
            if rights is None:
                return {'country': content[0], 'country_code': content[1],
                        'province': content[2], 'province_code': content[3],
                        'city': content[4], 'city_code': content[5],
                        'organize': content[6], 'carrier': content[7]}
            else:
                return self.lookup1(net_ip, rights)
        else:
            return {'country': content[0], 'country_code': content[1],
                    'province': content[2], 'province_code': content[3],
                    'city': content[4], 'city_code': content[5],
                    'organize': content[6], 'carrier': content[7]}

    def generate_tree(self, ip_list):
        length = len(ip_list)
        if length > 1:
            lefts = ip_list[:length / 2]
            rights = ip_list[length / 2:]
            (ip, content) = lefts[length / 2 - 1]
            return inet_aton(ip), content, self.generate_tree(lefts), self.generate_tree(rights)
        elif length == 1:
            (ip, content) = ip_list[0]
            return inet_aton(ip), content, None, None
        else:
            return

if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    ip_tree = IpTree()
    ip_tree.load_country_codes("doc/country_list.txt")
    ip_tree.load_china_province_codes("doc/china_province_code.txt")
    ip_tree.load_china_city_codes("doc/china_city_code.txt")
    ip_tree.loadfile("doc/mydata4vipday2.dat")
    print ip_tree.lookup('123.12.23.45')

