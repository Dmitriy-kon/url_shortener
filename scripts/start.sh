#!/bin/bash

alembic -c conf/alembic.ini upgrade head
uvicorn --factory app.main.web_api:create_app --reload --host 0.0.0.0 --port 8008
# poetry run start
# alembic -c conf/alembic.ini upgrade head
# tail -f /dev/null
