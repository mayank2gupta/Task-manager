from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
import tasks.utils as utils
from datetime import datetime

# reading in memory database stored in json format
dbpath = "./tasks_db.json"


# Create your views here.
@api_view(["GET", "POST"])
def tasks(request):

    if request.method == "GET":
        try:
            with open(dbpath, "r+") as task_json:
                task_list = json.load(task_json)
                sortedTaskList = sorted(task_list["tasks"], key=lambda x: datetime.strptime(x["creation_date"], "%d/%m/%Y"))
                if utils.is_null_empty_space(request.query_params.get("completed")):
                    return Response({"tasks": sortedTaskList}, status=status.HTTP_200_OK)
                else:
                    comTasks = []
                    for task in sortedTaskList:
                        if str(task["completed"]) == request.query_params.get("completed"):
                            comTasks.append(task)
                    return Response(
                        {"completed_tasks": comTasks}, status=status.HTTP_200_OK
                    )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == "POST":
        data = request.data
        if (
            utils.is_null_empty_space(data["title"])
            or utils.is_null_empty_space(data["description"])
            or not isinstance(data["completed"], bool)
        ):
            return Response(
                {"message": "invalid input"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            with open(dbpath, "r+") as task_json:
                task_list = json.load(task_json)
                task_json.seek(0)
                task_list["tasks"].append(data)
                json.dump(task_list, task_json, indent=4)
                task_json.truncate()
                return Response({"tasks": task_list}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["GET", "DELETE", "PUT"])
def single_task(request, pk):

    if request.method == "GET":
        with open(dbpath, "r+") as task_json:
            task_list = json.load(task_json)
            for task in task_list["tasks"]:
                if task["id"] == pk:
                    return Response(task, status=status.HTTP_302_FOUND)
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data
        if (
            utils.is_null_empty_space(data["title"])
            or utils.is_null_empty_space(data["description"])
            or not isinstance(data["completed"], bool)
        ):
            return Response(
                {"message": "invalid input"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            with open(dbpath, "r+") as task_json:
                task_list = json.load(task_json)
                for task in task_list["tasks"]:
                    if task["id"] == pk:
                        task["title"] = data["title"]
                        task["description"] = data["description"]
                        task["completed"] = data["completed"]
                        task["creation_date"] = data["creation_date"]
                        task["priority"] = data["priority"]
                        task_json.seek(0)
                        json.dump(task_list, task_json, indent=4)
                        task_json.truncate()
                        task_json.close()
                        return Response(task, status=status.HTTP_200_OK)
                return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == "DELETE":
        try:
            with open(dbpath, "r+") as task_json:
                task_list = json.load(task_json)
                for task in task_list["tasks"]:
                    if task["id"] == pk:
                        temp_task = task
                        task_list["tasks"].remove(task)
                        task_json.seek(0)
                        json.dump(task_list, task_json, indent=4)
                        task_json.truncate()
                        return Response(temp_task, status=status.HTTP_200_OK)
                return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["GET"])
def priority_task(request,level):

    if request.method == "GET":

        try:
            with open(dbpath, "r") as task_json:
                task_list = json.load(task_json)
                tasks = []
                for task in task_list["tasks"]:
                    if task["priority"] == level:
                        tasks.append(task)
                return Response(
                        {"tasks": tasks}, status=status.HTTP_200_OK
                    )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )