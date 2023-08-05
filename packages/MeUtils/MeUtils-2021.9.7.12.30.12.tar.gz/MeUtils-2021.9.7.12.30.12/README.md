[![Downloads](http://pepy.tech/badge/meutils)](http://pepy.tech/project/meutils)

<h1 align = "center">:rocket: 常用工具类 :facepunch:</h1>

## Install
```bash
pip install -U meutils
```

## Usages
### CLI
```bash
mecli pkg
```

### Tools
```python
from meutils.pipe import *

for i in range(5) | xtqdm:
    logger.info("这是一个进度条")

with timer('LOG'):
    logger.info("打印一条log所花费的时间")
```

### Notice
```python
from meutils.pipe import *
from meutils.log_utils import logger4wecom
from meutils.decorators.catch import wecom_catch, wecom_hook

@wecom_catch()
def wecom_catch_test():
    1/0

@wecom_hook('wecom_hook_test', 'Sleeping 3s')
def wecom_hook_test():
    time.sleep(3)

logger4wecom()
wecom_catch_test()
wecom_hook_test()
```

---
## TODO

pyspark https://wiki.n.miui.com/pages/viewpage.action?pageId=477643956

---
![刷题](https://tva1.sinaimg.cn/large/008eGmZEly1gopa6fzuwwj30xj0u0ado.jpg)
![git规范](https://tva1.sinaimg.cn/large/008eGmZEly1gn22tnx04dj312t0qpq6k.jpg)