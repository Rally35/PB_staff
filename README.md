Stock project created for Jenkins test

--------------------------------------

Stock_data/
├── docker-compose.yml        # Orchestrates the app and database containers
├── tickers.json              # List of stock tickers to fetch
├── fetcher/
│   ├── Dockerfile            # Docker setup for the fetcher
│   ├── main.py               # Python script to fetch and insert data
│   ├── run.sh                # Entrypoint to run the fetcher
│   └── requirements.txt      # Python dependencies
└── database/
    └── init.sql              # SQL to initialize the database schema



Running with Docker
-------------------

- The `fetcher` service is built using Python 3.11 (slim image) and installs dependencies from `requirements.txt` in a virtual environment.
- No environment variables are required by default. If needed, you can add a `.env` file in the `fetcher/` directory and uncomment the `env_file` line in `docker-compose.yml`.
- No ports are exposed by default, as the fetcher service does not run a web server.
- No persistent volumes or external services are configured by default. If you need a database, add it as a service in `docker-compose.yml` and update the `depends_on` section.

To build and run the project:

```sh
# From the project root directory
$ docker compose up --build
```

This will build the `python-fetcher` service and start it. The service runs as a non-root user and executes `run.sh` inside the container.

No additional configuration is required for the default setup.