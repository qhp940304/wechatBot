# import sys
# argv = sys.argv[1:]
# i = input('请输入')
# print(argv)
# print(i)
# input()
import time
for item in list(range(10))[::-1]:
    time.sleep(1)
    print(f'\r为了安全，休眠{item}秒后添加下一个群',flush=True,end='')

#
# from tqdm import tqdm
# import requests
# from contextlib import closing
# import hashlib
#
#
# def download(url, file_path):
#     m = hashlib.md5()
#     with open(file_path, 'wb') as code:
#         with closing(requests.get(url, stream=True)) as res:
#             file_size_str = res.headers.get('Content-Length')
#             with tqdm(total=int(file_size_str)) as pbar:
#                 for chunk in res.iter_content(chunk_size=10240):
#                     code.write(chunk)
#                     m.update(chunk)
#                     pbar.set_description("下载进度")
#                     pbar.update(len(chunk))
#
#
# class WithTest():
#     def __init__(self, _len: int):
#         self.max:range = range(_len)
#         self.now = 0
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, e_t, e_v, t_b):
#         pass
#
#     def myrange(self):
#         for i in self.max:
#             time.sleep(0.1)
#             yield i
#             # return self.now
# print("**********")
# _len = 100
# last = 0
# # with WithTest(_len) as res:
# #     with tqdm(total=_len,unit='人') as pbar:
# #         myrange = res.myrange()
# #         for item in myrange:
# #             pbar.set_description("进度")
# #             pbar.update(item-last)
# #             last = item
# #         pbar.update(_len - item)
# # print("结束")
#
# max = 10
# def myrange(max):
#     for i in range(max):
#         time.sleep(0.1)
#         yield i
# with tqdm(total=max,unit='人') as pbar:
#     myrang = myrange(max)
#     for item in myrang:
#         pbar.set_description("进度"+str(last))
#         pbar.update(item-last)
#         last = item
#     pbar.update(max - item)
#
#
#
#
#
# print("结束")