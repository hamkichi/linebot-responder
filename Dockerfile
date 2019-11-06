FROM k8sinfo/alpine-python-responder:numpy-3.7.5

ARG user="responder"

RUN adduser -D $user
WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py .
RUN chown -R $user:$user /app

USER $user
WORKDIR /app
ENV PYTHONUSERBASE=/app
ENV PATH="/app/bin:${PATH}"
RUN pip install --user -r requirements.txt && rm -f requirements.txt
