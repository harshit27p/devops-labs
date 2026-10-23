from flask import Flask, jsonify
import requests
import os

app = Flask("book app")

people_host = os.environ.get("PEOPLE_HOST")
people_port = os.environ.get("PEOPLE_PORT")

print(f"{people_host = }")
print(f"{people_port = }")


books = [
   dict(id=1021, title="DevOps for CDAC", price=599.9, author_id=1),
   dict(id=1022, title="Python for CDAC", price=299.9, author_id=1),
   dict(id=2211, title="DevOps for Dummies", price=1599.9, author_id=2),
]

@app.get("/api/books/<int:book_id>")
def get_book(book_id):
   filtered_books = [b for b in books if b["id"]==book_id]
   if len(filtered_books) == 0:
      return jsonify(dict(message=f"No book found for id {book_id}"))

   b = filtered_books[0]
   author_id = b["author_id"]
   url = f"http://{people_host}:{people_port}/api/people/{author_id}"
   print(f"{url = }")
   resp = requests.get(url)
   b["author"] = resp.json()
   return jsonify(b)


if __name__ == "__main__":
   app.run(port=5000, host="0.0.0.0")


