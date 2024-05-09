Create env:
python3 -m venv env
activate env:
source env/bin/activate
Install dependencies:
pip install fastapi sqlalchemy psycopg2-binary
connection port to connect postgres to alchemy

For v2:
Change webserver from uvicorn to gunicorn
Validate data prior to saving
Add limits to resources
Increased file descriptor limits
Adjusted number of threads (docker-compose)
91% KO to this point

Increased gunicorn workers; 89% KO

Corrected HTTP responses
configure pool-size (database.py)
84% KO

Added drop table if exists; corrected get date format: 85%KO

Added validator for skill type and name must be chars and spaces

Added validation preventing duplicate skill objects from saving; 67% KO

To do:
adding scoped sessions middleware in SQLAlchemy so same session is not used across muliple requests
adding indexing on name
adding more asynch to the routes
adding nginx





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