import os

def check():
    user_id, problem_id = map(str, input().split())

    #os.system("user_id.py")
    try:
        solution_code = open("reader/" + user_id + ".txt", "r").readlines()
    except:
        #print("here")
        return False

    # Project/
    os.chdir("userdata")
    # Project/userdata
    if not os.path.isdir(user_id):
        os.mkdir(user_id)
    os.chdir(user_id)
    # Project/userdata/{user_id}
    os.chdir("..")
    os.chdir("..")
    # Project/

    from distutils.dir_util import copy_tree

    copy_tree("problems/" + problem_id, "userdata/" + user_id + "/")
    # Project/
    os.chdir("userdata")
    # Project/userdata
    os.chdir(user_id)
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
    content = os.listdir("tests")

    import sys, io

    f = open(user_id, "w")
    f.writelines(solution_code)
    f.close()

    for test_n in range(len(content)):
        correct_answer = "".join(open("answers/" + str((1 + test_n)) + "out.txt").readlines())
        input_data = "".join(open("tests/" + str((1 + test_n)) + "in.txt").readlines())

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
            os.chdir("..")
            os.chdir("..")
            #print("WRONG")
            break

        sys.stdin = saved_in
        sys.stdout = saved_out
        output_stream.seek(0)
        result = "".join(output_stream.read())
        if correct_answer != result:
            #print("WRONG")
            os.chdir("..")
            os.chdir("..")
            #break
    else:
        os.chdir("..")
        os.chdir("..")
        #print("Ok")


if __name__ == "__main__":
    check()