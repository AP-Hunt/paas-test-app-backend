import os
from flask import Flask
from flask_restful import Resource, Api

import psycopg2

app = Flask(__name__)
api = Api(app)

DATABASE_URL = os.getenv("DATABASE_URL", None)
PORT = os.getenv("PORT", 5000)
DEBUG = os.getenv("DEBUG", "false")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


@api.resource("/tables")
class GetTables(Resource):
    def get(self):
        cur.execute("select * from information_schema.tables")
        tables = cur.fetchall()
        tmp = []
        for table in tables:
            tmp.append({"db": table[1], "name": table[2]})
        return tmp


@api.resource("/")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


if __name__ == "__main__":
    debug = False if DEBUG == "false" else True
    app.run(debug=debug, port=PORT)
