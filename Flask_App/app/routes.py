from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
from app import advqflag, advq2items, advq1items, search_flag, search_item

@app.route("/delete/<int:course>", methods=['POST'])
def delete(course):
    try:
        db_helper.remove_course(course)
        result = {'success': True, 'response': 'Removed Course'}
    except:
        result = {'success': False, 'response': 'Error'}
    
    return jsonify(result)

@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    db_helper.insert_course(data['description'])
    result = {'success': True, 'response': 'Added'}
    return jsonify(result)

@app.route("/search/course", methods=['POST'])
def search():
    global search_flag
    search_flag = 1
    data = request.get_json()
    global search_item
    search_item = db_helper.search_course(int(data['description']))
    result = {'success': True, 'response': 'Added'}
    return jsonify(result)

@app.route("/advq1", methods=['POST'])
def advq1():
    global advq1items
    advq1items = db_helper.find_general_best_courses()
    # print(advq1items)
    result = {'success': True, 'response': 'Added'}
    # print(advq1items)
    global advqflag
    advqflag = 1
    # homepage(advq1items)
    # print("yay")
    return jsonify(result)
    # return render_template("index.html", items=advq1items)

@app.route("/advq2", methods=['POST'])
def advq2():
    # print(Subject)
    global advq2items
    advq2items = db_helper.find_recom_course()
    print(advq2items)
    result = {'success': True, 'response': 'Added'}
    global advqflag
    advqflag = 2
    # homepage(advq2items)
    return jsonify(result)

@app.route("/")
def homepage():
    # print(advitems)
    # if advitems == []:
    #     print("here")
    #     return
    # advitems = advitems
    # print(advitems)
    global advqflag
    global advq1items
    global advq2items
    global search_flag
    global search_item
    if advqflag == 1:
        items = advq1items
    elif advqflag == 2:
        items = advq2items
    elif search_flag == 1:
        items = search_item
    else:
        items = db_helper.fetch_courses()
        # items = []
        # print("there")
    advqflag = None
    search_flag = None
    return render_template("index.html", items = items)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """
    data = request.get_json()
    try:
        db_helper.update_course(task_id, float(data['description']))
        result = {'success': True, 'response': 'Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)
