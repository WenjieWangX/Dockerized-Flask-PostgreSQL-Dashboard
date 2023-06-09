# Simple Web-Based dashboard

## Introduction

A simple web-based dashboard to visualize data. This project is used a Flask, postgresql, and docker containers. The `plotly` package were used for creating a dashboard an visualization.

## Technical Details

In this directory, you'll find a `Dockerfile` that defines the image your code will be copied into and installed in. Specifically, your source code will be installed into a Python 3.10 virtual environment as a package via pip, along with any dependencies you've specified in a `requirements.txt` file.

You'll also find a `compose.yaml` file that defines the container that'll be used to run your code. Specifically, to serve your web-based dashboard in a local browser at http://localhost:8888/, Docker is configured to start the container by executing `run-app`, the expected [entrypoint](https://setuptools.pypa.io/en/latest/userguide/entry_point.html) for your application.

### The database

The data you'll be visualizing will be in a Postgres database, also configured in `compose.yaml`. Credentials to access this database will be provided in the following environment variables:

- `POSTGRES_HOST` provides the host
- `POSTGRES_PORT` provides the port
- `POSTGRES_USER` provides the user
- `POSTGRES_PASSWORD` provides the password
- `POSTGRES_DB` provides the database

An example can be found in `local.env`. Note that these will be subject to change, so make sure not to hard code these.

### The data

The tables in the database:

```
brx1=# \dt
                      List of relations
 Schema |           Name           | Type  |      Owner
--------+--------------------------+-------+------------------
 public | CM_HAM_DO_AI1/Temp_value | table | process_trending
 public | CM_HAM_PH_AI1/pH_value   | table | process_trending
 public | CM_PID_DO/Process_DO     | table | process_trending
 public | CM_PRESSURE/Output       | table | process_trending
```

Each table has the same schema, like so:

```
brx1=# \d public."CM_HAM_DO_AI1/Temp_value"
                Table "public.CM_HAM_DO_AI1/Temp_value"
 Column |            Type             | Collation | Nullable | Default
--------+-----------------------------+-----------+----------+---------
 time   | timestamp without time zone |           |          |
 value  | double precision            |           |          |
```

Each table contains the following data:
| Table | Name | Units |
|--------------------------|------------------|---------|
| CM_HAM_DO_AI1/Temp_value | Temperature | Celsius |
| CM_HAM_PH_AI1/pH_value | pH | n/a |
| CM_PID_DO/Process_DO | Distilled Oxygen | % |
| CM_PRESSURE/Output | Pressure | psi |

Note that this database is only contains a data for temperature, pH, Distilled Oxygen, and Pressure at April 19. Feel free to add more data.

### How to test your code

Run `docker compose up` and navigate your browser to http://localhost:8888/. That's it!
