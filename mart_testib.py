from md5 import vra_range_generator
from md5 import vra_md5
import time
import vra_http_request_helper

__author__ = 'Mart'


i = 65
while i <= 70:
    print("Char " + str(i) + " = " + chr(i))
    i += 1

i = 0
while i < 200:
    print("i = " + str(i) + " and result: " + str(vra_range_generator.get_range(i,"?")))
    i += 1

a = ["a"]
b = ["b"]
c = a + b
print(str(c))
a = vra_http_request_helper.get_my_ip()

print("get_ranges(10,20): " + str(vra_range_generator.get_ranges(3,7,"_")))

print(str(time.localtime()))
i = 0
#while i < 2:
# vra_md5.md5_crack("f1bdb130b442c9bc665bcfdb36caba20","???")
# print(str(time.localtime()))
#while i < 2:

print("Testing break")

def test():
    i = 0
    while i < 10:
        if i is 4:
            break
        print("i=" + str(i))
        i += 1
    print("Reached the end of the test")

test()

import vra_query

queries = {}


print("Socket info: " + str(a))

def testin_taas():
    global queries


