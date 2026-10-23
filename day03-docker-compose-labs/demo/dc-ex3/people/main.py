from flask import Flask, jsonify

app = Flask("my app")


people = [
  dict(id=1, name="Vinod", city="Bangalore", email="vinod@vinod.co"),
  dict(id=2, name="John Doe", city="Dallas", email="johndoe@xmpl.com")
]


@app.get("/api/people")
def get_people():
   return jsonify(people)

@app.get("/api/people/<int:person_id>")
def get_person(person_id):
   result = [p for p in people if p["id"]==person_id]
   if len(result) == 0:
      return jsonify(dict(message=f"No data found for person id {person_id}"))

   return result[0]


if __name__ == "__main__":
   app.run(port=5000, host="0.0.0.0")


