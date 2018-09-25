#!/usr/bin/env bash

pushd ../

docker-compose -f .docker/docker-compose_test_env.yml down

sudo rm -rf .docker/tests/profiles/


docker-compose -f .docker/docker-compose_test_env.yml build

popd
