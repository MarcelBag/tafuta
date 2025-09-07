.PHONY: dev prod stop logs

dev:
	docker-compose up --build

prod:
	docker build -t tafuta:latest .
	docker run -d --name tafuta_app --env-file .env.prod -p 5000:5000 tafuta:latest

stop:
	docker stop tafuta_app || true && docker rm tafuta_app || true

logs:
	docker logs -f tafuta_app
