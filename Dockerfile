# @intract.v1 scope:container intent:package:intract_cli priority:2 domain:runtime input:source_tree output:oci_image effect:build forbid:secret_leak,root_user,latest_tag validate:no_forbidden_effect meaning:"package Intract CLI as a safe container"
FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
USER 10001
ENTRYPOINT ["intract"]
CMD ["--help"]
