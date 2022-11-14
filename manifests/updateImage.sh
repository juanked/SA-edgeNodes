#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit
filename="kustomize/deployment.yaml"
search="image: sanoderegistry.azurecr.io/receiver:latest"
replace="image: sanoderegistry.azurecr.io/receiver:$BUILD_BUILDID"

sed -i "s@$search@$replace@" $filename

username="juanked"
git config --global user.name "David Cristóbal"
git config --global user.email "david@juanked.es"

tmpDir="$(mktemp -d)"
echo "$tmpDir"
cd "$tmpDir" || exit
git clone "https://$username:$GITHUBKEY@github.com/juanked/SA-DevOps.git"
repoDir="$tmpDir/SA-DevOps"
cd "$repoDir" || exit
cp "$SCRIPT_DIR/$filename" kustomize/deployment.yaml

git add kustomize/deployment.yaml
git commit -m "Nuevo manifest $BUILD_BUILDID"
git push "https://$username:$GITHUBKEY@github.com/juanked/SA-DevOps.git"
trap 'rm -rf -- "$tmpDir"' EXIT