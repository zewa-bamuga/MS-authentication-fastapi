#!/bin/bash

set -o errexit
set -o pipefail

# Let the DB start
python -m a8t_tools.db.wait_for_db

alembic upgrade head

# Create superuser
if [ -n "${EMAIL}" ]; then
  python manage.py create-superuser "${FIRSTNAME}" "${LASTNAME}" "${EMAIL}" "${PASSWORD}" || true
fi

# Create staff
FIRSTNAMES=("$FIRSTNAME1" "$FIRSTNAME2")
LASTNAMES=("$LASTNAME1" "$LASTNAME2")
QUALIFICATIONS=("$QUALIFICATION1" "$QUALIFICATION2")
POSTS=("$POST1" "$POST2")
EMAILS=("$EMAIL1" "$EMAIL2")
DESCRIPTIONS=("$DESCRIPTION1" "$DESCRIPTION2")
LINK_TO_VKS=("$LINK_TO_VK1" "$LINK_TO_VK2")


for ((i=0; i<${#EMAILS[@]}; i++)); do
  EMAIL="${EMAILS[i]}"
  FIRSTNAME="${FIRSTNAMES[i]}"
  LASTNAME="${LASTNAMES[i]}"
  QUALIFICATION="${QUALIFICATIONS[i]}"
  POST="${POSTS[i]}"
  DESCRIPTION="${DESCRIPTIONS[i]}"
  LINK_TO_VK="${LINK_TO_VKS[i]}"

  if [ -n "${EMAIL}" ]; then
    python manage.py create-staff "${FIRSTNAME}" "${LASTNAME}" "${QUALIFICATION}" "${POST}" "${EMAIL}" "${DESCRIPTION}" "${LINK_TO_VK}" || true
  fi
done


exec "$@"