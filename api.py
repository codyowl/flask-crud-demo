from flask import Flask 
from flask import request


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method=="GET":
		return "Its a get call"
	else:
		return "its a post call"	


if __name__ == "__main__":
	app.run()		