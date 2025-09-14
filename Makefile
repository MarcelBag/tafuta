.PHONY: dev prod stop logs

dev:
	cd backend/docker && docker compose -p tafuta -f docker-compose.yml down --remove-orphans
	cd backend/docker && docker compose -p tafuta -f docker-compose.yml up --build

prod:
	docker build -f backend/docker/Dockerfile --build-arg ENV=prod -t tafuta:latest .
	docker run -d --name tafuta_app --env-file .env.prod -p 5000:5000 tafuta:latest

stop:
	docker stop tafuta_app || true && docker rm tafuta_app || true

logs:
	docker logs -f tafuta_app
