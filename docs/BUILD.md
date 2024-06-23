```shell
black .
isort . --profile black
```

# update version

```shell
$ bumpver update --patch

# or
$ bumpver update --minor

# or
$ bumpver update --major
```


# publish package

```shell
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

python3 -m build

# fake
python3 -m twine upload --repository testpypi dist/*

# real
python3 -m twine upload dist/*
```

