#!/bin/bash

set -o errexit
set -o nounset


celery -A app.celery worker -l info -Q $1 -c $2
