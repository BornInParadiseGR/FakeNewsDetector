FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --force-reinstall scipy==1.7.3
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["index.py"]
