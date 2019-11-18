rm -rf build/
rm -rf dist/
rm -rf mahjongpy.egg-info/
python3 setup.py bdist_wheel
twine upload --repository pypi dist/*
