FROM k8sinfo/alpine-python-responder:numpy-3.7.4

ARG user="responder"

RUN adduser -D $user
WORKDIR /home/$user

COPY requirements.txt requirements.txt
COPY app.py .
RUN chown -R $user:$user /home/$user

USER $user
WORKDIR /home/$user
ENV PATH="~/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt && rm -f requirements.txt
