# 布隆过滤器简易实现
### 安装
```shell script
pip install blmfilter
```

### 使用
```
from blmfilter import BloomFilter

demo = [i for i in "abcdefghigklmnopqrstuvwxyz"]
demo_upper = [i for i in "abcdefghigklmnopqrstuvwxyz".upper()]

bf = BloomFilter(1024 * 1024)

for key in demo:
    bf.add(key)

for key in demo:
    assert bf.check(key) == True  # 值均存在

for key in demo_upper:
    assert bf.check(key) == False  # 值均不存在
```
