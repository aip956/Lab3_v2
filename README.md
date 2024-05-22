Create env:
python3 -m venv env
activate env:
source env/bin/activate
Install dependencies:
pip install fastapi sqlalchemy psycopg2-binary
connection port to connect postgres to alchemy

Chose FastAPI
Endpoints / instances: 
 - Get warrior by id
 - Get warrior by search term
 - Count warriors
 - Post/create warriors
To Uvicorn web server (originally)
PostgreSQL database


For v2:
Change webserver from uvicorn to gunicorn
Added limits to resources (in docker-compose)
Increased file descriptor limits (in docker-compose)
Adjusted number of threads (docker-compose)
91% KO to this point

Increased gunicorn workers; 89% KO

Corrected HTTP responses
configure pool-size (database.py)
84% KO

Added drop table if exists; corrected get date format: 85%KO

Added validator for skill type and name must be chars and spaces

Added validation preventing duplicate skill objects from saving; 67% KO

Improve speed of operation
Postman; currently ~20m;
changed return on get by id, modified uuid

Fixed HTTP status code from 201 to 200, fixed search for id; 20% KO
Validate data prior to saving (had validation in the wrong class)
Increased pool to 2000; 8%

Postgres improvements (docker-compose): 2%-4% KO
- listen_addresses='*': Accept connections on all network interfaces
- max_connections=1100: Set max concurrent connections
- shared_buffers=512MB: Set the amount of memory to caching database blocks in memory
- work_mem=64MB: Set amount of memory to be used by internal sort operations
- maintenance_work_mem=512MB: Set the max memory for maintenance operations
- wal_buffers=16MB: Set the amount of memory for Write-Ahead-Logging buffers
- 
  

Added redis: 11%
Redis: established a connection instead of instance: 16%
Add async? = changed to aioredis for async/await
20%

To do:
Optimize redis asynch
adding nginx
redundancy; 
use key words








adding scoped sessions middleware in SQLAlchemy so same session is not used across muliple requests; already done




resources: 500 payload for warriors, generate payload scripts, reduce numbers
check FastAPI docs on payload
Timeout: log on docker; which routes are timing out
reduce payload size


To run API:
Install uvicorn: pip install uvicorn 
Run the API: uvicorn main:app --reload

To POST (add):
Start the API using uvicorn main:app --reload

curl -X POST "http://127.0.0.1:8000/warrior" -H "Content-Type: application/json" -d '{
    "name": "Master Yoda",
    "dob": "1970-01-01",
    "fight_skills": "BJJ, KungFu, Judo"
}'
To add to the container's database:
Change database.py: SQLALCHEMY_DATABASE_URL = "postgresql://postgres:local@db:5432/EngLab3"

go to localhost:8080/docs to enable Swagger

curl -X POST "http://172.18.0.3:8000/warrior" -H "Content-Type: application/json" -d '{
    "name": "Master Yoda",
    "dob": "1970-01-01",
    "fight_skills": "BJJ, KungFu, Judo"
}'
curl -X POST "http://englab3-web-1:8000/warrior" -H "Content-Type: application/json" -d '{
    "name": "Master Yoda",
    "dob": "1970-01-01",
    "fight_skills": "BJJ, KungFu, Judo"
}'

Select all warriors:
curl -X GET "http://127.0.0.1:8000/warrior"


GET /warrior/[:id] 
curl -X GET "http://127.0.0.1:8000/warrior/{id}"
curl -X GET "http://127.0.0.1:8000/warrior/{1}" returns the Yoda entry


GET /warrior?t=[:search term] – search warrior attributes 
curl -X GET "http://127.0.0.1:8000/warrior?t=search_term"
curl -X GET "http://127.0.0.1:8000/warrior?t=Yoda" returns Yoda


GET /counting-warriors – count registered warriors;
curl -X GET "http://127.0.0.1:8000/counting-warriors"

Docker: Added postgres to Docker (docker-compose.yaml file). 
To rebuild the Docker containers: docker-compose up --build
For status: docker-compose ps

Uvicorn creates server / load balances; no need for NGINX

need to change server to junicorn
add to requirements, add to docker-compose
Consider the restrictions on memory, etc.