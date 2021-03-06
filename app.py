# Tozny imports
import e3db
from e3db.types import Search

#Flask
from flask import Flask
from flask import jsonify
from flask import request
from markupsafe import escape


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Tonzny Python Example</p>"

@app.route("/status/<user>/<string:round>")
def status(user,round):
    print(user,round)
    client = e3db.Client(e3db.Config.load(user))
    query = Search(include_data=True,include_all_writers = True).match(condition="AND", record_types=['outcome'], plain={'round':round})   
    results = client.search(query)
    if len(results)==0 :
        return "record not found"
    else:
        record = results.records[0]
        return jsonify(record.to_json())


# post the winner's name for the round.
#
@app.route("/winner/<judge>/<user>/<string:round>", methods=['POST'])
def winner(judge,user,round):
    client = e3db.Client(e3db.Config.load(judge))
    record_id = client.write('outcome', data={'winner':user}, plain={'round':round})
    return jsonify(record_id.data)

@app.route("/move/all/<user>")
def moves_all(user):
    client = e3db.Client(e3db.Config.load(user))
    query=Search(include_data=True,
    include_all_writers = True ).match(record_types=['moves'])
    results = client.search(query)
    if len(results) == 0 :
            return( f'<p>no records found for {escape(round)}')
    else :
        record = results.records[0]
        return jsonify([x.to_json() for x in results])

@app.route("/move/<user>/<string:round>/<move>",methods=['POST'])
def post_move(user,round,move):
    print("move/usr/round/move", user, round, move)
    client = e3db.Client(e3db.Config.load(user))
    # write the users move for the round
    record_id = client.write('moves',
        data={'move':move},
        plain={'round':round,'user':user})
    return jsonify(record_id.to_json())


@app.route("/move/<user>/<string:round>",methods=['GET'])
def get_move(user,round):
    client = e3db.Client(e3db.Config.load(user))
    query=Search(include_data=True,
    include_all_writers = True ).match(record_types=['moves'], plain={'round':round})
    results = client.search(query)
    if len(results) == 0 :
            return( f'<p>no records found for {escape(round)}')
    else :
        record = results.records[0]
        return jsonify(record.to_json())




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)