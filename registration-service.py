import json
import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_api import status
import sqlite3
import requests

app = Flask(__name__)
api = Api()
client = app.test_client()
app.config['JSON_AS_ASCII'] = False

"""
Подключение к базе данных c курсами, если её нет - она создается
столбцы:
    id: int
    name: text - название курса 
    author: text - автор курса 
    body: text - содержимое курса, является корректным json
"""
try:
    DATABASE_courses = sqlite3.connect('file:courses.db?mode=rw', uri=True)
except:
    DATABASE_courses = sqlite3.connect("courses.db")
    cur = DATABASE_courses.cursor()
    cur.execute("""
                    CREATE TABLE courses
                    (
                    id bigint PRIMARY KEY,
                    name varchar(100) NOT NULL,
                    author varchar(100) NOT NULL,
                    body text NOT NULL
                    );
                """)
    cur.execute("INSERT INTO courses VALUES(?,?,?,?)", [1, "nikita", "test", "{}"])
    DATABASE_courses.commit()


@app.route("/send-test-json-to-create/", methods=['GET'])
def send_test_json_to_create():
    r = requests.post('http://127.0.0.1:3000/course/create', json=json.dumps({"name": "fdfd",
                                                                              "author": "fdfdfdfd",
                                                                              "body": {"1": 1, "ds": 45}}))
    print(r.status_code)
    #print(r.json())
    return str(r.status_code) + "  " + str(r.text)

@app.route("/send-test-json-to-update/<ind>", methods=['GET'])
def send_test_json_to_update(ind):
    try:
        ind = int(ind)
    except:
        return "id is empty or not in INT type", status.HTTP_400_BAD_REQUEST

    r = requests.post('http://127.0.0.1:3000/course/update/'+str(ind), json=json.dumps({"name": "ddsd",
                                                                              "author": "oxoxoxo",
                                                                              "body": {"2": 1}}))
    print(r.status_code)
    #print(r.json())
    return str(r.status_code)+ "  " + str(r.text)


@app.route("/course/create", methods=['POST'])
def course_create():
    req = request.get_json(silent=True)

    if req is None:
        return "the file sent is in the wrong format", status.HTTP_400_BAD_REQUEST
    try:
        js = json.loads(req)
    except:
        return "json is not correct", status.HTTP_400_BAD_REQUEST

    #print(js)
    if 'name' not in req or 'author' not in req or 'body' not in req:
        return "json does not contain some of the required fields", status.HTTP_400_BAD_REQUEST

    try:
        with sqlite3.connect("courses.db") as con:
            cur = con.cursor()

            res = cur.execute('SELECT max(id) FROM courses')
            max_id = res.fetchone()[0]

            data = [max_id + 1, str(js['name']), str(js['author']), str(js['body'])]
            cur.execute("INSERT INTO courses VALUES(?,?,?,?)", data)
            con.commit()
        return jsonify(max_id + 1)
    except:
        return "the format of the fields does not match the template", status.HTTP_400_BAD_REQUEST


@app.route("/course/update/<ind>", methods=['POST'])
def course_update(ind):
    try:
        ind = int(ind)
    except:
        return "id is empty or not in INT type", status.HTTP_400_BAD_REQUEST

    req = request.get_json(silent=True)

    if req is None:
        return "the file sent is in the wrong format", status.HTTP_400_BAD_REQUEST
    try:
        js = json.loads(req)
    except:
        return "json is not correct", status.HTTP_400_BAD_REQUEST

    if 'name' not in req or 'author' not in req or 'body' not in req:
        return "json does not contain some of the required fields", status.HTTP_400_BAD_REQUEST

    try:
        with sqlite3.connect("courses.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from courses WHERE id = ?", [ind])
            res = cur.fetchone()
            if not res:
                return "an entry with this id was not found", status.HTTP_204_NO_CONTENT
            else:
                data = [str(js['name']), str(js['author']), str(js['body']), ind]
                cur.execute("UPDATE courses SET name = ?, author = ?, body = ? WHERE id = ?", data)
                con.commit()
        return "Ok. Updated", status.HTTP_200_OK
    except:
        return "the format of the fields does not match the template", status.HTTP_400_BAD_REQUEST


@app.route("/course/get-all", methods=['GET'])
def courses_all():
    try:
        s = []
        with sqlite3.connect("courses.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from courses")
            res = cur.fetchall()

            for row in res:
                new_row = {"id": row[0], "name": row[1], "author": row[2], "body": row[3]}
                s.append(new_row)

        return jsonify(s, )
    except:
        return "internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route("/course/get-by-id/<id>", methods=['GET'])
def course_get_by_id(id):
    try:
        ind = int(id)
    except:
        return "id is empty or not in INT type", status.HTTP_400_BAD_REQUEST
    try:
        with sqlite3.connect("courses.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from courses WHERE id = ?", [ind])
            res = cur.fetchone()
            if res:
                return jsonify(res)
            return "an entry with this id was not found", status.HTTP_204_NO_CONTENT
    except:
        return "", status.HTTP_400_BAD_REQUEST


@app.route("/course/remove/<id>", methods=['GET'])
def remove_course_by_id(id):
    try:
        ind = int(id)
    except:
        return "id is empty or not in INT type", status.HTTP_400_BAD_REQUEST
    try:
        with sqlite3.connect("courses.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from courses WHERE id = ?", [ind])
            res = cur.fetchone()

            if not res:
                return "Ok. Record not found", status.HTTP_200_OK
            else:
                cur.execute("DELETE FROM courses WHERE id = ?", [ind])
                con.commit()
                return "Ok. Deleted", status.HTTP_200_OK
    except:
        return "something went wrong :/", status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
