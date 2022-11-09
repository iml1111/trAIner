FROM python:3.9 as base

COPY ./trAIner/ /home/trAIner/
WORKDIR /home/trAIner/
COPY ./trAIner/requirements.txt /home/trAIner/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5001

CMD ["gunicorn", "-w", "2", \
    "--bind", "0.0.0.0:5000", \
    "manage:application"]