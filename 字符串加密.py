'''
```python
import hashlib
midified_str = objs.first().modified.strftime("%Y-%m-%d %H:%M:%S")
formula_id = hashlib.md5((formula_name + midified_str).encode('utf8')).hexdigest()
```
'''