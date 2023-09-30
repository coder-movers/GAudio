from functools import cached_property


class CacheData:
    @cached_property
    def cached_data(self):
        return {'data': 'cached'}

# obj = CacheData()
# print(obj.cached_data) # {'data': 'cached'}
#
# del obj # 对象被销毁
#
# obj = CacheData() # 新的对象缓存已清除
# print(obj.cached_data) # {'data': 'cached'}
