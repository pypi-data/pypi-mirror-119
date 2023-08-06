# OmHelper
[python.org](https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects)

## Dependence
```bash
nothing
```

## Build
```bash
python -m build --no-isolation
```

## Upload
```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

## OM.helper
- md5() -> hash
- rstr() -> random string
- rone() -> random one from list
- ip_to_int() -> convert ip string to int
- int_to_ip() -> convert int ip to ip string
- SingletonBase -> base singleton class
- async_loop() -> return a asyncio loop
- to_async() -> warp a sync func to async func
- SuperDict -> warp dict, more funcions

