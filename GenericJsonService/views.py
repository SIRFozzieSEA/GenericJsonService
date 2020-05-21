import json
import sqlite3
from rest_framework.views import APIView
from django.http import JsonResponse
from io import StringIO

class genericJsonServiceTest(APIView):

    def get(self, request):

        # http://localhost:8000/json?user=stephan&table=grocery_list
        # http://localhost:8000/setup

        requestQueryParams = request.query_params
        requestTable = requestQueryParams["table"]
        requestUser = requestQueryParams["user"]

        conn = sqlite3.connect('/home/ubuntu/GenericJsonService/db.sqlite3')
        cursor = conn.cursor()
        t = (requestUser,)
        cursor.execute("SELECT * FROM " + requestTable + " WHERE USER=?", t)
        records = cursor.fetchall()

        buffer = StringIO()
        for row in records:
            buffer.write(row[1])
        cursor.close()
        conn.close()

        print(buffer.getvalue())

        return JsonResponse(json.loads(buffer.getvalue()), safe=False)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        conn = sqlite3.connect('/home/ubuntu/GenericJsonService/db.sqlite3')
        cursor = conn.cursor()

        requestTable = body["tableName"]
        requestUser = body["userName"]

        if 'tableName' in body:
            del body['tableName']

        if 'userName' in body:
            del body['userName']

        t = (json.dumps(body), requestUser)
        cursor.execute("UPDATE " + requestTable + " SET ITEM=? WHERE USER=?", t)

        conn.commit()
        cursor.close()
        conn.close()

        return JsonResponse(json.loads("""{ "op": "post" }"""), safe=False)

class setupGenericJsonServiceTest(APIView):

    def get(self, request):

        conn = sqlite3.connect('/home/ubuntu/GenericJsonService/db.sqlite3')
        cursor = conn.cursor()

        cursor.execute("create table if not exists grocery_list (user TEXT, item TEXT)")
        conn.commit()

        bobo = '{"buyGroceryItems": [], "boughtGroceryItems":[]}'
        t = (bobo,)
        cursor.execute("insert into grocery_list values('stephan', ?)", t);
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse(json.loads("""{ "op": "getsetup" }"""), safe=False)

    # def connect_postgres(self, myColumns, myQuery):
    #     url = 'postgresql://{}:{}@{}:{}/{}'
    #     url = url.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)
    #     engine = sa.create_engine(url, client_encoding='utf8')
    #     session = sessionmaker()
    #     session.configure(bind=engine)
    #     mySession = session()
    #     json_response = self.make_json_response(mySession, myColumns, myQuery)
    #     return json_response
    #
    # def make_json_response(self, mysession, myColumns, myQuery):
    #     resultset = mysession.execute(myQuery)
    #     all_results = resultset.fetchall()
    #     write_record_comma = False
    #
    #     buffer = StringIO()
    #     buffer.write('[')
    #
    #     for row in all_results:
    #         if write_record_comma:
    #             buffer.write(',')
    #         buffer.write('{')
    #         x = 0
    #         for singleColumn in row:
    #             buffer.write(self.quote_char + myColumns[x] + self.quote_char + ": " + self.quote_char + str(
    #                 singleColumn) + self.quote_char)
    #             if x < len(myColumns) - 1:
    #                 buffer.write(", ")
    #             x = x + 1
    #         buffer.write('}')
    #         write_record_comma = True
    #
    #     buffer.write(']')
    #     mysession.close()
    #     return buffer.getvalue()

