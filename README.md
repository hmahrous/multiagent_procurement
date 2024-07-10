

# UBS Procurement GenAI 


### Local setup with Docker

```bash
git@github.com:Bain/aag-d5ym.git
cd aag-d5ym
cp api/.env api/.env
```

Make sure to add `OPEN_AI_CONFIG__OPENAI_API_KEY` to `.env`.


```bash
docker-compose up --build
```

The docker compose file will spin up two containers `api` and `postres_db`. 

NOTE: In case of database connection error, please set the HOST as `postres_db` container IP address.

The swagger documentation can be found at http://127.0.0.1:8080/docs

