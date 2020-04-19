from flask import Flask, request, render_template
from work import GetTagPosition
import csv

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def root():
    if request.method == "POST":
        url = request.form.get('get_url').strip()
        GetTagPosition(url) 
        print(url)
        results = []
        with open('templates/file.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            # print(data)
            for row in data:
                if row:
                    results.append({
                          "tag": row[0],
                          "title": row[1],
                          "position": row[2],
                          "page": row[3],
                          "total_page": row[4]
                        })
        # data = csv.DictReader("templates/file.csv").split("\n")
        
        fieldnames = [key for key in results[0].keys()]

        return render_template("index.html", results=results, fieldnames=fieldnames, len=len)
                
    elif request.method == "GET":
        return render_template("index.html")

if __name__ == "__main__":
    app.debug = True 
    app.run()