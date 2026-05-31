# @intract.v1 scope:artifact intent:deploy:container_image priority:1 domain:devops forbid:latest_tag,root_user validate:no_forbidden_effect meaning:"Production container image"
FROM python:latest
WORKDIR /app
COPY backend/ ./backend/
CMD ["python", "-c", "print('web-app v2 mock')"]
