Stock project created for Jenkins test

--------------------------------------

gpw_alert_system/
├── docker-compose.yml
├── tickers.json
├── fetcher/
│   ├── main.py              # Yahoo fetch + DB insert
│   └── requirements.txt
├── db/
│   ├── init.sql             # Schema + trigger setup
├── scheduler/
│   └── run.sh               # Cron or shell-based runner
└── README.md

