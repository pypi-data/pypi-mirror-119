- create a venv (py > 3.5 ish)
- install dependencies
- in the `python/` folder, run:
```shell
python ./compileProto.py
```
- output should be in the `log_service_proto/` folder

packaging process:
https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

python -m pip install --user --upgrade setuptools wheel build
python -m pip install --user --upgrade twine

test publish:
    `python3 -m twine upload --repository testpypi dist/*`
    and for a new revision, you might have to add the flag:
        `--skip-existing`
    install: pip install -i https://test.pypi.org/simple/ jocampo-log-service-proto
    use: xyz 
for realsies: 
