## Corona Data Chart

## Features:
- Corona cases bar chart of specified date range of country.

1. Create virtual environment to install dependencies.

```shell script
$ virtualenv venv -p python3
``` 

2. Activate virtual environment.

```shell script
$ source venv/bin/activate
```

3. Install all the dependencies using below command.

```shell script
(venv)$ pip install -r requirements.txt
```

4. After creating database apply migrations using below command

```shell script
(venv)$ python manage.py migrate
```

11. Run project on server using below command:
```shell script
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.


### Create account: ###
```
POST http://127.0.0.1:8000/signup/
body={
"email": "testuser@test.com",
"country": "IN",
"password": "Abcd@123123"
}
```
It return:
```
{
    "token": "614eb7baa001af108dfee6e94248da284fe243c0"
}
```
### Get tokens: ###
```
GET http://127.0.0.1:8000/login/
body={
"email": "testuser@test.com",
"country": "IN",
"password": "Abcd@123123"
}
```
It return:
```
{
    "token": "614eb7baa001af108dfee6e94248da284fe243c0"
}
```
### Get Covid data: ###
```
POST http://127.0.0.1:8000/covid-data/
Headers={
"Authorization":"Token 614eb7baa001af108dfee6e94248da284fe243c0",
}
body={
    "country" : "IN",
    "from_date" : "2021-01-01",
    "to_date" : "2021-02-01"   
}
```
It return:
```
	It will retrun graph. 
```
