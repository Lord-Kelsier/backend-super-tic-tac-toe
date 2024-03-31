# Super Tic Tac Toe API

## Installation

### Requirements

This project requires docker and a pre-existing psql database.

### Steps

1. Clone the repository and navigate to the project directory

  ```bash
  git clone https://github.com/Lord-Kelsier/backend-super-tic-tac-toe.git
  cd backend-super-tic-tac-toe
  ```

2. Create a `.env` file in the project root directory and add the following environment variables

  ```env
  DB_NAME=<Your DB name>
  DB_PASSWORD=<Your DB ultra secret password>
  DB_USER=<Your DB user>
  DB_HOST=<Your DB host>
  DB_PORT=<Your DB port>
  SECRET=<Your secret>
  ```

3. Compose the project

  ```bash
  docker compose up -d
  ```

And that's it! The project should be running on http://localhost:5318/api-docs/. In case you dont have a database, before running the project, you follow the next steps to create a database:

1. Create a new docker network

```bash
docker network create backend-network
```

2. Create a new directory to store the database data

```bash
mkdir database
cd database
```

3. Crea un archivo `docker-compose.yml` en el directorio y agrega el siguiente contenido

```yml
version: '3.9'

services:
  db:
    container_name: psqldb
    image: postgres:14-alpine
    ports:
      - '5433:5432'
    volumes:
      - ./data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=MyAwesomePassword
    networks:
      - db

networks:
  db:
    name: backend-network
    external: true
```

4. Compose the project

```bash
docker compose -f docker-compose.yml up -d
```

5. Create the database

```bash
docker exec -it psqldb bash
psql -U postgres
```

```sql
CREATE DATABASE super_tic_tac_toe;
```

Now you can run the project with the first steps.
Remember to change the database credentials in the `.env` file, in this case the values are:

```env
DB_NAME=super_tic_tac_toe
DB_PASSWORD=MyAwesomePassword
DB_USER=postgres # This is the default user
DB_HOST=psqldb # This is the name of the container
DB_PORT=5432 # This is the port of the container
```

Also, in this case you should change 3rd step of the proyect installation to:

```bash
docker compose -f docker-compose-dev.yml up -d
```

## Testing

### lobby

- [x] `GET /api-v1/lobby` - get all lobbies
- [ ] `POST /api-v1/lobby` - create a new lobby - Authenticated users only
- [ ] `GET /api-v1/lobby/:id` - get a lobby by id
- [ ] `PUT /api-v1/lobby/:id` - update a lobby by id - Owner only
- [ ] `PATCH /api-v1/lobby/:id` - partially update a lobby by id - Owner only
- [ ] `DELETE /api-v1/lobby/:id` - delete a lobby by id - Owner only

- [ ] `PATCH /api-v1/lobby/enter_lobby/` - enter a lobby - Authenticated users and without any lobby
- [ ] `PATCH /api-v1/lobby/leave_lobby/` - leave a lobby - Users in lobby only
- [ ] `PATCH /api-v1/lobby/start_game/` - start a game - Owner only

#### Not implemented

- [ ] `PATCH /api-v1/lobby/end_game/` - end a game - Owner only
- [ ] `PATCH /api-v1/lobby/kick_user/` - remove a user from a lobby - Owner only