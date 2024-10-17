# -------------------------------------------------------------
# update the package on pypi
# 2024-10-12
#
# Tip: if you don't want to retype pypi's username every time
#      define it as an environment variable (TWINE_USERNAME)
#
# -------------------------------------------------------------
function warn {
    GREEN='\033[0;32m'
    NORMAL='\033[0m'
    echo -e "${GREEN}$1${NORMAL}"
}

function get_value {
    # get the value from the config file (requires the Python toml package)
    toml get --toml-path pyproject.toml $1
}

# Clean the subdirs, for safety and to guarantee integrity
# ./cleanup.sh

# Check for changes in the files compared to the repository
if ! git diff --quiet; then
  warn "Won't do it: there are changes in the repository. Please commit first!"
  exit 1
fi

# get the project inform
package_name=$(get_value project.name)
package_version=v$(get_value project.version) # add a 'v' in front (git convention) 

# update Pypi
warn "Rebuilding $package_name..."
rm -rf build dist *.egg-info # necessary to guarantee integrity
python3 -m build
if twine upload dist/* ; then
    git push # just in case
    warn "... create tag $package_version, and push to remote git repo..."
    git tag $package_version
    git push --tags
    warn "Done ($package_version)!"
else
    warn "Failed ($package_version)!"
    exit 1
fi   