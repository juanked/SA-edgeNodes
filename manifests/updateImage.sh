#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit
filename="kustomize/deployment.yaml"
search="image: sanoderegistry.azurecr.io/receiver:latest"
replace="image: sanoderegistry.azurecr.io/receiver:$BUILD_BUILDID"

sed -i "s@$search@$replace" $filename
echo "reemplazo realizado"

username="juanked"
git config --global user.name "David Cristóbal"
git config --global user.email "david@juanked.es"

git remote add SA-DevOps https://github.com/juanked/SA-DevOps.git

git add kustomize/deployment.yaml kustomize/kustomization.yaml
git commit -m "Nuevo manifest $BUILD_BUILDID"
git push "https://$username:$GITHUBKEY@github.com/juanked/SA-DevOps.git" master