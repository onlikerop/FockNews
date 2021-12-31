FROM python:latest

MAINTAINER Eugene Karabanov <onlikerop@email.cz>
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/FockNews/
WORKDIR /usr/src/FockNews/

COPY . /usr/src/FockNews/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
