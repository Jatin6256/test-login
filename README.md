# test-login


## Local set Up With docker-compose

```
git clone https://github.com/Jatin6256/test-login.git
source venv/bin/activate
pip install -r requirements.txt
docker pull postgres
docker pull adminer
docker-compose -f docker-compose.yaml up
export DATABASE_URL="postgres://example:example@localhost:5432/userDB"
python login.py
```
