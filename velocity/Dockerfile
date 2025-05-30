FROM eclipse-temurin:21-jre

WORKDIR /app
COPY \
	forwarding.secret \
	server-icon.png \
	start.sh \
	velocity.jar \
	velocity.toml \
	.

EXPOSE 25565
ENTRYPOINT ["sh", "/app/start.sh"]
