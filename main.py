import json

from sanic import Sanic
from sanic import response

from src.clients.grade import GradeClient
from src.factory.grade import GradeFactory


app = Sanic()


@app.route("/api/v1/query_grade", methods=['POST', ])
async def course_grades(request):
    data = {
        'ID': '',
        'password': '',
        'year': '',
        'term': '',
    }

    body = json.loads(str(request.body, 'utf-8'))

    for key in data:
        data[key] = body.get(key)

    ID = data.get('ID')
    if not ID:
        print("error")
        return response.json("ID error", status=500)

    password = data.get('password')
    if not password:
        print("error")
        return response.json("error", status=500)

    course_data = GradeClient(ID, password).get_all_course()
    res = GradeFactory(course_data).parse_course()
    return response.json(res, status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)