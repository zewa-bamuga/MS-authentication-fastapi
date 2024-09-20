#!/bin/bash

set -o errexit
set -o nounset


celery -A app.celery beat -l INFO
