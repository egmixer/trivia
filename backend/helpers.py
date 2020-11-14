from flask import request, abort
from constants import QUESTIONS_PER_PAGE

def get_questions_paginated(request, selection):

    page = request.args.get('page', 1, type=int)

    if page < 1: 
        return abort(422)
    
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]

    return formatted_questions[start:end]

    