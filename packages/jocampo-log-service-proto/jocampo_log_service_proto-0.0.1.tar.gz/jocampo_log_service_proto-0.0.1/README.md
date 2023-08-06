- create a venv (py > 3.5 ish)
- install dependencies
- in the `python/` folder, run:
```shell
python ./compileProto.py
```
- output should be in the `log_service_proto/` folder

packaging process:
https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi


python3 -m pip install --upgrade build

python3 -m pip install --upgrade twine

test publish: python3 -m twine upload --repository testpypi dist/*
    install: pip install -i https://test.pypi.org/simple/ jocampo-log-service-proto
    use: 
for realsies: 
