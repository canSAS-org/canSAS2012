#! /bin/sh

set -e

( cd examples && mkdir hdf5 && mkdir xml && python fakecansas.py )

cd docs 
rm -rf build
make html 
cd build/html 
mkdir examples
cp -r ../../../examples/hdf5 examples
cp -r ../../../examples/xml examples

git init

# inside this git repo we'll pretend to be a new user
git config user.name "Travis CI"
git config user.email "tobias.richter@esss.se"

# The first and only commit to this new Git repo contains all the
# files present with the commit message "Deploy to GitHub Pages".
chmod -R a+r .
git add .
git commit -m "Deploy to GitHub Pages"

echo pushing to github
# Force push from the current repo's master branch to the remote
# repo's gh-pages branch. (All previous history on the gh-pages branch
# will be lost, since we are overwriting it.) We redirect any output to
# /dev/null to hide any sensitive credential data that might otherwise be exposed.
git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1 && echo pushed with no error 
echo end of script
