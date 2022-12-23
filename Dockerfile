FROM python:3.8-slim-buster

# Create a working directory.

WORKDIR /Users/henrycastillomelo/Documents/Full stack Bootcamp/Course 7 Ptyhon for Data science, AI and else/Project Pratt copy



# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY . ./

# Finally, run gunicorn.
CMD ["python", "./app.py"]