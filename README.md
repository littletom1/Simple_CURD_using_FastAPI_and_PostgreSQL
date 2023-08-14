just simple curl using fastapi and postgreSQL
to learn postgreSQL
HOW TO RUN
1. install docker-compose version 1.29.2 and docker version 23.0.3
2. After insall docker run the following command: docker network create mynetwork
3. run docker-compose build
4. run docker-compose up
5. create database: docker exec -it api bash -> alembic upgrade head
6. go to http://localhost:8022/docs
7. ENJOY!!
