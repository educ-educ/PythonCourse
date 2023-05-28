import json
import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api()
client = app.test_client()

problems = {
    1: {"title": "a + b", "statement": "Give two integer <b>a</b>, <b>b</b>. Print sum a + b."},
    2: {"title": "Min(a, b)", "statement": "Give two integer <b>a</b>, <b>b</b>. Print min(a, b)."}
}

parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("videos", type=int)

# @app.route('/api/testcode', methods=['GET'])
# def get_test_json_file():
#     f = open("11.txt", 'r')
#     s = f.readlines()
#     f.close()
#     return jsonify(s)


@app.route('/api/allproblems', methods=['GET'])
def get_all_problem():
    return jsonify(problems)

@app.route('/api/problems/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    return jsonify(problems[int(problem_id)])

@app.route("/api/tests/<problem_id>/<test_id>", methods=['GET'])
def get_test(problem_id, test_id):
    f = open("problems/"+str(problem_id)+"/tests/"+str(test_id)+'.txt')
    s = f.readlines()
    f.close()
    return jsonify(s)

@app.route("/api/answers/<problem_id>/<test_id>", methods=['GET'])
def get_answer(problem_id, test_id):
    f = open("problems/"+str(problem_id)+"/answers/"+str(test_id)+'.txt')
    s = f.readlines()
    f.close()
    return jsonify(s)

@app.route("/api/check/<problem_id>/<user_id>", methods=['POST'])
def check_solution(problem_id, user_id):
    solution = str(request.get_data(as_text=True))
    f = open("reader/" + user_id + ".txt", "w")
    f.write(solution)
    f.close()

    try:
        solution_code = open("reader/" + user_id + ".txt", "r").readlines()
    except:
        print("ERROR")
        return jsonify("PE")

    # Project/
    # os.chdir("userdata")
    # # Project/userdata
    # if not os.path.isdir(user_id):
    #     os.mkdir(user_id)
    # os.chdir(user_id)
    # # Project/userdata/{user_id}
    # os.chdir("..")
    # os.chdir("..")
    # Project/

    # from distutils.dir_util import copy_tree

    # copy_tree("problems/" + problem_id, "userdata/" + user_id + "/")
    # # Project/
    # os.chdir("userdata")
    # # Project/userdata
    # os.chdir(user_id)
    # Project/userdata/{user_id}

    # Project/userdata/{user_id}
    # ...solution.py
    # ...{problem_id}
    #       ...tests
    #           ...1in
    #           ...2in
    #       ...answers
    #           ...1out
    #           ...2out

    os.system(user_id + ".py")
    content = os.listdir("problems/" + str(problem_id) +"/tests")

    import sys, io

    f = open(user_id, "w")
    f.writelines(solution_code)
    f.close()

    for test_n in range(len(content)):
        correct_answer = "".join(open("problems/" + str(problem_id)+"/answers/" + str((1 + test_n)) + ".txt").readlines())
        input_data = "".join(open("problems/" + str(problem_id) +"/tests/" + str((1 + test_n)) + ".txt").readlines())

        input_stream = io.StringIO()
        output_stream = io.StringIO()
        input_stream.write(input_data)
        input_stream.seek(0)
        saved_in = sys.stdin
        saved_out = sys.stdout
        sys.stdin = input_stream
        sys.stdout = output_stream
        try:
            with open(user_id, "r", encoding="utf-8") as file:
                exec(file.read())
        except:
            sys.stdin = saved_in
            sys.stdout = saved_out
            output_stream.seek(0)
            print("WA")
            return jsonify("WA")

        sys.stdin = saved_in
        sys.stdout = saved_out
        output_stream.seek(0)
        result = "".join(output_stream.read())
        if correct_answer != result:
            print("WA")
            return jsonify("WA")
    else:
        print("OK")
        return jsonify("OK")



if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
