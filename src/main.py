from sanic import Sanic
from sanic.response import json

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

    for key in data:
        data[key] = request.args.get(key)

    course_data = GradeClient(data.get('ID'), data.get('password')).get_all_course()
    res = GradeFactory(course_data).parse_course()
    return json(res, status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)