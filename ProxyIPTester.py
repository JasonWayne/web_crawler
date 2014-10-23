import re
import threading
from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import time

class ProxyIPTester:
    def __init__(self, timeout):
        self.__store = r'verified.txt'
        self.__read = r'ip.txt'
        self.__original_ips = []
        self.__verified_ips = []
        self.__test_url = r'http://www.baidu.com'
        self.__timeout = timeout
        self.__test_str = '030173'
        pass

    def read_ip(self):
        ips = open(self.__read, 'r')
        line = ips.readline()
        pattern = re.compile(r'''(.*?)\s+(.*?)\s+(.*)\n''')
        while len(line) > 0:
            self.__original_ips.extend(pattern.findall(line))
            line = ips.readline()

    def multi_thread_test(self, thread_number=1):
        pool = ThreadPool(thread_number)
        self.__verified_ips = pool.map(self.test, self.__original_ips)

        pool.close()
        pool.join()

    def test(self, ip):
        cookies = urllib2.HTTPCookieProcessor()
        proxy_handler = urllib2.ProxyHandler({"http" : r'http://%s:%s' % (ip[0], ip[1])})
        opener = urllib2.build_opener(cookies, proxy_handler)
        opener.addheaders = [('User-Agent', r'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0
''')]
        urllib2.install_opener(opener)
        try:
            res = urllib2.urlopen(self.__test_url, timeout=self.__timeout)
            result = res.read()
            pos = result.find(self.__test_str)
            if pos > 1:
                return ip
        except Exception, e:
            print e.message


    def get_next_test_ip(self):
        for ip in self.__original_ips:
            yield ip

    def sort(self):
        pass

    def store(self):
        verified = open(self.__store, 'w')
        for ip in self.__verified_ips:
            print 'writing ' + str(ip)
            verified.write("%-15s\t%5s\t%s\n" % (ip[0], ip[1], ip[2]))
        verified.close()

    def remove_nones(self):
        while True:
            try:
                self.__verified_ips.remove(None)
            except Exception, e:
                break


if __name__ == "__main__":
    tester = ProxyIPTester(5)
    tester.read_ip()
    tester.multi_thread_test(10)
    tester.remove_nones()
    tester.sort()
    tester.store()