import json
import sqlite3
from rest_framework.views import APIView
from django.http import JsonResponse
from io import StringIO

class genericJsonServiceTest(APIView):

    def get(self, request):

        # http://localhost:8000/json?user=stephan&table=grocery_list

        requestQueryParams = request.query_params
        requestTable = requestQueryParams["table"]
        requestUser = requestQueryParams["user"]

        conn = sqlite3.connect('db.sqlite3')
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

        conn = sqlite3.connect('db.sqlite3')
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

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        cursor.execute("create table grocery_list (user TEXT, item TEXT)")
        conn.commit()

        cursor.execute("""insert into grocery_list values('stephan', '{"buyGroceryItems": [], "boughtGroceryItems":[]}""");
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse(json.loads("""{ "op": "getsetup" }"""), safe=False)

