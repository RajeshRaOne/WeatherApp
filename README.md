# Weather App  setup
### Step 1: Install Python 3
 
```
https://www.python.org/downloads/
```

### Step 2: Intall Virtual Environment and Activate 

```
pip install --user virtualenv
python3 -m venv env

mac/linux 
source env/bin/activate

windows
.\env\Scripts\activate
```
 

### Step 3: Install dependencies Module
1. please use requirnment.txt file to install dependencies 

```
pip install -r requirements.txt
```

### Step 4: Run Django Project using below command

```
python manage.py runserver
```

Open browser and access below URL. /add used to add cities

```
http://127.0.0.1:8000/
http://127.0.0.1:8000/add

```

### step 5: Run docker image

```
docker build -t weatherapp .
docker run -p 8000:8000 weatherapp
```
