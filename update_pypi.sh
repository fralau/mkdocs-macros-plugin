# update the package on pypi
echo "Cleaning up..."
rm -rf dist
rm -rf build
echo "Recreating wheels..."
python3 setup.py sdist bdist_wheel
echo "---"
echo "UPLOAD..."
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
