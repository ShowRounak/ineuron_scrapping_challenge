from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
#import aspose.words as aw
import json
import logging

logging.basicConfig(filename="scrapper.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


class Ineuron_Scrapping:
    url = "https://ineuron.ai/courses"

    def __init__(self):
        url = self.url

    def ineuron_course_data(self):
        """This Method scraps all course data using beautifulsoup and json"""
        try:
            response = requests.get(self.url)
            course_page = response.text
            soup = bs(course_page, 'html.parser')
            script = soup.find_all('script')[25].text.strip()
            self.data = json.loads(script)
            print("Course Data Scrapping Successful")
            logging.info("Course Data Scrapping Successful")
        except Exception as e:
            print("Exception occured", e)
            logging.error("Course data retrieval unsuccessful", e)

    def get_course_categories(self):
        """This methods returns all major course categories"""
        try:
            course_data = self.data['props']['pageProps']['initialState']['init']['categories']
            for i in course_data.keys():
                return course_data[i]['title']
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Course category retrieval unsuccessful", e)
        else:
            print("Course Category Scrapping Successful")
            logging.info("Course category Scrapping Successful")

    def get_instructor_details(self):
        """This method returns instructor details of iNeuron"""
        try:
            instructor_data = self.data['props']['pageProps']['initialState']['init']['instructors']
            for i in instructor_data.keys():
                print(instructor_data[i]['name'])
                if 'description' in instructor_data[i]:
                    print(instructor_data[i]['description'])
                print('\n')
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Course instructor data retrieval unsuccessful", e)
        else:
            print("Course instructor data Scrapping Successful")
            logging.info("Course instructor data Scrapping Successful")

    def get_all_course_titles(self):
        """This method scraps all courses names"""
        try:
            self.all_course_keys = self.data['props']['pageProps']['initialState']['init']['courses'].keys()
            list_of_courses = list(self.all_course_keys)
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Course title data retrieval unsuccessful", e)
        else:
            print("Course title data Scrapping Successful")
            logging.info("Course title data Scrapping Successful")

    def scrap_all_course(self):
        """This method scraps every detail about all courses"""
        try:
            self.courses = {}
            for i in self.all_course_keys:
                self.courses[i] = {}
                self.courses[i]['description'] = self.data['props']['pageProps']['initialState']['init']['courses'][i][
                    'description']
                self.courses[i]['curriculum'] = \
                    self.data['props']['pageProps']['initialState']['init']['courses'][i]['courseMeta'][0]['overview'][
                        'learn'][
                    0:-1]
                self.courses[i]['instructor_details'] = \
                    self.data['props']['pageProps']['initialState']['init']['courses'][i][
                        'instructorsDetails']
                self.courses[i]['requirements'] = \
                    self.data['props']['pageProps']['initialState']['init']['courses'][i]['courseMeta'][0]['overview'][
                        'requirements']
                self.courses[i]['features'] = \
                    self.data['props']['pageProps']['initialState']['init']['courses'][i]['courseMeta'][0]['overview'][
                        'features']
                self.courses[i]['language'] = \
                    self.data['props']['pageProps']['initialState']['init']['courses'][i]['courseMeta'][0]['overview'][
                        'language']
                self.courses[i]['price_INR'] = \
                    list(self.data['props']['pageProps']['initialState']['init']['courses'][i]['pricing'].values())[0]
            print("All Courses scrapping successful")
            list_of_all_course_details = []
            for i in self.all_course_keys:
                title = i
                description = self.courses[i]['description']
                curriculum = self.courses[i]['curriculum']
                instructors = self.courses[i]['instructor_details']
                requirements = self.courses[i]['requirements']
                features = self.courses[i]['features']
                language = self.courses[i]['language']
                price = self.courses[i]['price_INR']
                mydict = {"TITLE": title, "DESCRIPTION": description, "CURRICULUM": curriculum,
                          "INSTRUCTOR_DETAILS": instructors, "FEATURES": features,
                          "REQUIREMENTS": requirements, "LANGUAGE": language, "PRICE_INR": price}
                list_of_all_course_details.append(mydict)
            print("Scraping of all course data Successful")
            logging.info("Scraping of all course data Successful")
            return list_of_all_course_details
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Scraping of all course data unsuccessful", e)

    def scrap_one_course(self, course_name):
        """This method only scraps the course provided as parameter"""
        try:
            course_details = self.courses[course_name]
            description = self.courses[course_name]['description']
            curriculum = self.courses[course_name]['curriculum']
            instructors = self.courses[course_name]['instructor_details']
            requirements = self.courses[course_name]['requirements']
            features = self.courses[course_name]['features']
            language = self.courses[course_name]['language']
            price = self.courses[course_name]['price_INR']
            self.cd = {"DESCRIPTION": description, "CURRICULUM": curriculum,
                       "INSTRUCTOR_DETAILS": instructors, "FEATURES": features,
                       "REQUIREMENTS": requirements, "LANGUAGE": language, "PRICE_INR": price}
            print("Scraping of one course data Successful")
            logging.info("Scraping of one course data Successful")
            return self.cd
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Scraping of one course data unsuccessful", e)

    def txt_file_maker(self):
        """This method create separate text files of each course"""
        try:
            for i in range(len(self.cd)):
                for k in self.cd[i].items():
                    with open(f"{self.ll[i]['TITLE']}_copy.txt", 'a', encoding='utf-8') as f:
                        f.write(str(k))
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred while creating text files", e)
        else:
            print("Text files created successfully")
            logging.info("Text files created successfully")

    def pdf_maker(self):
        """This method create separate PDF files of each course"""
        try:
            for i in range(len(self.cd)):
                doc = aw.Document(f"{self.cd[i]['TITLE']}_copy.txt")
                doc.save(f"{self.cd[i]['TITLE']}_copy.pdf", aw.SaveFormat.PDF)
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred while creating PDF files", e)
        else:
            print("PDF files created successfully")
            logging.info("PDF files created successfully")






