from flask import Flask, request, jsonify
import json
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Chargement des données
with open("championFull.json", "r", encoding="utf-8") as f:
    data_raw = f.readlines()

d = {}
p = 0

for Text in data_raw:
    for index, Value in enumerate(Text):
        if p == 0:
            if "i" in Value and Text[index + 1] == "d" and Text[index + 2] == '"':
                name = []
                name_tmp = []
                k = 5
                while Text[index + k] != '"':
                    name_tmp.append(Text[index + k])
                    k += 1
                name.append(str(''.join(name_tmp)))
                p += 1

        if "c" in Value:
            if Text[index + 1] == "o" and Text[index + 2] == "o" and Text[index + 8] == '"':
                k = 11
                cd_tmp = []
                cd = []
                while Text[index + k] != "]":
                    if Text[index + k] != ",":
                        cd_tmp.append(Text[index + k])
                        k += 1
                    else:
                        cd.append(''.join(cd_tmp))
                        cd_tmp = []
                        k += 1

                if p == 1:
                    d[name[0] + " q"] = cd
                if p == 2:
                    d[name[0] + " z"] = cd
                if p == 3:
                    d[name[0] + " e"] = cd
                if p == 4:
                    d[name[0] + " r"] = cd
                p += 1

        if p == 5:
            p = 0

# Stock temporaire pour le sort affiché
current = {"sort": "", "cd": ""}

@app.route("/get-random", methods=["GET"])
def get_random():
    key = random.choice(list(d.keys()))
    cd = d[key][0]
    current["sort"] = key
    current["cd"] = cd
    return jsonify({"sort": key})

@app.route("/check", methods=["POST"])
def check():
    user_cd = request.json.get("cd")
    correct = current["cd"]
    is_correct = (user_cd == correct)
    return jsonify({"correct": is_correct, "answer": correct})

if __name__ == "__main__":
    app.run(debug=True)
