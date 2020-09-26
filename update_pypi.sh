# -------------------------------------------------------------
# update the package on pypi
#
# Tip: if you don't want to retype pypi's username every time
#      define it as an environement variable (TWINE_USERNAME)
# -------------------------------------------------------------
function warn {
    GREEN='\033[0;32m'
    NORMAL='\033[0m'
    echo -e "${GREEN}$1${NORMAL}"
}

setup="python3 setup.py"
package_name=$($setup --name)
package_version=$($setup --version)

warn "UPDATE PACKAGE $package_name ($package_version) ON PYPI:"
warn "Cleaning up..."
rm -rf dist
rm -rf build
warn "Recreating wheels..."
$setup sdist bdist_wheel  1>/dev/null
warn "---"
warn "Upload to Pypi..."
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
warn "Done ($package_version)!"
