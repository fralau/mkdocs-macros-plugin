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
package_version=v$($setup --version) # add a 'v' in front (git convention) 

warn "UPDATE PACKAGE $package_name ($package_version) ON PYPI:"
warn "Cleaning up..."
rm -rf dist
rm -rf build
warn "Recreating wheels..."
$setup sdist bdist_wheel  1>/dev/null
# update version (just in case):
package_version=v$($setup --version) # add a 'v' in front (git convention) 
warn "---"
warn "Upload to Pypi..."
if twine upload --repository-url https://upload.pypi.org/legacy/ dist/* ; then
    warn "... create tag $package_version, and push to remote git repo..."
    git tag $package_version
    git push --tags
    warn "Done ($package_version)!"
else
    warn "Failed ($package_version)!"
fi
