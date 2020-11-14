import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from helpers import get_questions_paginated
from constants import QUESTIONS_PER_PAGE 
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    #todo1
    CORS(app, resources={'/': {'origins': '*'}})
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET, PUT, POST, DELETE, OPTIONS')
        return response

    #todo2
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        formatted_questions = get_questions_paginated(request, questions)

        if formatted_questions == []:
            return abort(400)

        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions_count': len(questions),
            'categories': categories_dict,
        })

    #todo3
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(formatted_categories)
        })

    #todo4
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except:
            if question is None: 
                abort(404)
            else:
                abort(422)

    #todo6
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        
        try:
            category = Category.query.filter_by(id=id).one_or_none()
            questions = Question.query.filter_by(category=category.id).all()

            # paginate the selection
            formatted_questions = get_questions_paginated(request, questions)

            # return the results
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'current_category': category.type
            })
        except:
            abort(404)


    
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        #todo7
        if 'search_term' in body.keys():
            questions = Question.query.filter(Question.question.ilike('%'+body['search_term']+'%')).all()
            formatted_questions = [question.format() for question in questions]
            return jsonify(formatted_questions)
        #todo5
        try: 
            question = Question(
            question=body['question'],
            answer=body['answer'],
            difficulty=body['difficulty'],
            category=body['category'],
            )
        
            question.insert()
        except: 
            return abort(400)

        return jsonify({
            "success": True,
            "created": question.format(),
        })


    #todo8

    @app.route('/quiz', methods=['POST'])
    def get_next_question():
        body = request.get_json()

        if body == None or 'category' not in body.keys():
            return abort(422)

        previous_questions = []
        if 'previous_questions' in body.keys():
            previous_questions = body['previous_questions']

        question = Question.query.filter(Question.id.notin_(previous_questions), Question.category == body['category']).first()
        formatted_question = question.format() if question != None else None

        return jsonify({
            "success": True,
            "question": formatted_question 
        })




    
    #todo9
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request error"
        }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found error"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable error"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        }), 500



    return app

