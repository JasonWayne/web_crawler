#encoding='utf-8'

import urllib2
import threading
import re

class ProxyIPFinder:
    def __init__(self):
        self.__url = r'''http://cn-proxy.com'''
        self.__file_name = 'ip.txt'
        self.__page = ''
        self.__ips = []

    def open_with_new_thread(self):
        t = threading.Thread(target=self.open, args=())
        t.start()
        t.join()

    def open(self):
        res = urllib2.urlopen(self.__url)
        self.__page = res.read()

    def text_process(self):
        pattern = r'''<tr>\s*<td>(.+?)</td>\s*<td>(\d+?)</td>\s*<td>(.+?)</td>\s*<td>'''
        pattern = re.compile(pattern)
        for ip in pattern.findall(self.__page):
            self.__ips.append(ip)

    def store_in_file(self):
        file = open(self.__file_name, 'w')
        for ip in self.__ips:
            file.write("%-15s\t%-5s\t%-s\n" % (ip[0], ip[1], ip[2]))
        file.close()


if __name__ == "__main__":
    finder = ProxyIPFinder()
    finder.open_with_new_thread()
    finder.text_process()
    finder.store_in_file()
