### Install and Run


1. Create and activate virtual environment 

```buildoutcfg
python3.6 -m venv $TMPDIR/online_courses_api
source $TMPDIR/online_courses_api/bin/activate
```

2. Install `online_courses_api` package

```buildoutcfg
pip install git+https://github.com/sheh/online_courses_api
```

3. Run

```buildoutcfg
run_app.py 
```

run options:
```buildoutcfg
    --port: port default:5000
    --db: path to sqlite file, default:$TMPDIR/online_courses_api.db>
    --drop-db: drop database before start
```

### Run test 


```buildoutcfg
python3.6 -m venv $TMPDIR/online_courses_api
source $TMPDIR/online_courses_api/bin/activate
git clone https://github.com/sheh/online_courses_api 
cd online_courses_api
pip install .
pip install pytest pytest-flask
pytest

...
collected 57 items

online_courses_api/tests/test_classes_specific.py ........
online_courses_api/tests/test_endpoints_common.py ...........................................
online_courses_api/tests/test_students_specific.py ......

=========================================================================== 57 passed in 0.89 seconds ============================================================================
(online_courses_api) ➜  online_courses_api git:(master)
```

### Assumptions:

* sqlite is used
* there are no verbose message about the cause of request error, just http code
* only on param can be use for filtration
* filtration by `class` and `teacher` support arrays
* complete data structure should be `PUT` for update, partial update is not supported

### The schema

**/teacher**

* `POST /teacher` - create
* `GET /teacher?param=val` - filter by param
* `GET /teacher/<id>` - get
* `PUT /teacher/<id>` - update
* `DELETE /teacher/<id>` - delete


**/students**

* `POST /students` - create
* `GET /students?param=val` - filter by param
* `GET /students?class=<id>&class=<id>` - filter by classes
* `GET /students/<id>` - get
* `PUT /students/<id>` - update
* `DELETE /students/<id>` - delete
* `PUT /students/<sid>/classes/<cid>` - add student `sid` to class `cid`
* `DELETE /students/<sid>/classes/<cid>` - delete student `sid` to class `cid`


**/classes**

* `POST /classes` - create
* `GET /classes?param=val` - filter by param
* `GET /classes?teacher=<id>&teacher=<id>` - filter by teachers
* `GET /classes/<id>` - get
* `PUT /classes/<id>` - update
* `DELETE /classes/<id>` - delete
* `PUT /classes/<cid>/teacher/<tid>` - bind class `cid` to teacher `tid`
* `DELETE /classes/<cid>/teacher/<tid>` - unbind class `cid` from teacher `tid`


### How it works


(command `http` below is `httpie` tool `pip install httpie`)

1. Create a teacher:

`http POST http://localhost:5000/teachers first_name=Joe last_name=Moon specs:='["math", "physics"]'`

response:

```buildoutcfg
{
    "first_name": "Joe",
    "id": 1,
    "last_name": "Moon",
    "specs": [
        "math",
        "physics"
    ]
}
```

2. Get the teacher:

`http GET http://localhost:5000/teachers/1`

response:

```buildoutcfg
{
    "first_name": "Joe",
    "id": 1,
    "last_name": "Moon",
    "specs": [
        "math",
        "physics"
    ]
}
```

3. Filter teachers by a parameter:

`http GET 'http://localhost:5000/teachers?first_name=Joe'`

response:

```buildoutcfg
{
    "first_name": "Joe",
    "id": 1,
    "last_name": "Moon",
    "specs": [
        "math",
        "physics"
    ]
}
```

4. Update a teacher

`http PUT http://localhost:5000/teachers/1 first_name=Joseph last_name=Moon specs:='["math"]'`

response:

```buildoutcfg
{
    "first_name": "Joseph",
    "id": 1,
    "last_name": "Moon",
    "specs": [
        "math"
    ]
}
```


5. Delete the teacher:

`http DELETE 'http://localhost:5000/teachers/1'`

response:

```buildoutcfg
{}
```


6. Create class:

`http POST http://localhost:5000/classes name=math description='A math class' spec=math`

response:

```buildoutcfg
{
    "description": "A math class",
    "id": 1,
    "name": "math",
    "spec": "math"
}
```

7. Bind class and teacher:

`http PUT http://localhost:5000/classes/1/teacher/1`

response:

```buildoutcfg
{}
```

8. Filter classes by teacher:


`http GET http://localhost:5000/classes?teacher=1`

response:

```buildoutcfg
[
    {
        "description": "A math class",
        "id": 1,
        "name": "math",
        "spec": "math"
    }
]
```

9. Create a student:

`http POST http://localhost:5000/students first_name=Kelly last_name=Williams`

response:

```buildoutcfg
{
    "first_name": "Kelly",
    "id": 1,
    "last_name": "Williams"
}
```

10. Add a student to class:

`http PUT http://localhost:5000/students/1/classes/1`

response:

```buildoutcfg
{}
```

11. Filter students by class:

`http GET http://localhost:5000/students?class=1`

response:

```buildoutcfg
[
    {
        "first_name": "Kelly",
        "id": 1,
        "last_name": "Williams"
    }
]
```