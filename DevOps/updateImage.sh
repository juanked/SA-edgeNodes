#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit
filename="receiver/deployment.yaml"
search="image:.*"
replace="image: sanoderegistry.azurecr.io/receiver:$BUILD_BUILDID"


username="juanked"
git config --global user.name "David Cristóbal"
git config --global user.email "david@juanked.es"

tmpDir="$(mktemp -d)"
echo "$tmpDir"
echo "$GITHUBKEY"
cd "$tmpDir" || exit
git clone "https://$username:$GITHUBKEY@github.com/juanked/SA-DevOps.git"
repoDir="$tmpDir/SA-DevOps"
cd "$repoDir" || exit
sed -i "s@$search@$replace@" $filename
# sed -i "s@$search@$replace@" $filename
# cp "$SCRIPT_DIR/$filename" receiver/deployment.yaml
git add receiver/deployment.yaml
git commit -m "Nuevo manifest $BUILD_BUILDID"
git push "https://$username:$GITHUBKEY@github.com/juanked/SA-DevOps.git"
trap 'rm -rf -- "$tmpDir"' EXIT