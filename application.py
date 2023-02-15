from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import scrapper
import logging

logging.basicConfig(filename="app.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

application = Flask(__name__)
app = application

@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    """Render homepage"""
    logging.info("rendering successfull")
    return render_template('index.html')

@app.route('/course',methods=['POST','GET'])
@cross_origin()
def one_course():
    """Shows one course details on the webpage"""
    if request.method == 'POST':
        try:
            searchcourse = request.form['content']
            obj = scrapper.Ineuron_Scrapping()
            obj.ineuron_course_data()
            obj.get_all_course_titles()
            obj.scrap_all_course()
            detail = obj.scrap_one_course(searchcourse)
            print(detail)
            logging.info("course detail fetch successfully")

            return render_template('result.html', details = detail)

        except Exception as e:
            print("There is an excpetion,", e)
            logging.error("There is an excpetion,", e)
            return "Something is wrong"

    else:
        return render_template("index.html")

@app.route('/allcourse',methods=['POST','GET'])
@cross_origin()
def all_course():
    """Shows all course details on the webpage"""
    if request.method == 'POST':
        try:
            obj = scrapper.Ineuron_Scrapping()
            obj.ineuron_course_data()
            obj.get_all_course_titles()
            all_course_details = obj.scrap_all_course()
            logging.info("course detail fetch successfully")
            return render_template('result.html', details = all_course_details)

        except Exception as e:
            print("There is an excpetion,", e)
            logging.error("There is an excpetion,", e)
            return "Something is wrong"

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)



