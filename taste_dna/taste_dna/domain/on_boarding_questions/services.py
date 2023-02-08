# Python imports
from typing import Type

# Django imports
from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager

# App imports
from taste_dna.domain.on_boarding_questions.models import (
    QuestionAnswer,QuestionOption,OnboardingQuestion,QuestionAnswerFactory,QuestionOptionFactory,OnboardingQuestionFactory
)

class OnBoardingQuestionsServices:#--
    
    
    def get_on_boarding_question_factory(
        self,
    ) -> Type[OnboardingQuestionFactory]:#--
        return OnboardingQuestionFactory
    
    
    def get_on_boarding_question_repo(self) -> BaseManager[OnboardingQuestion]:#--
        return OnboardingQuestion.objects
    
    
    def delete_on_boarding_question(self,result):
        return OnboardingQuestion.delete(result)
    
    @staticmethod
    def get_on_boarding_question_by_id(OnboardingQuestion_id) -> Type[OnboardingQuestion]:#--
        return OnboardingQuestion.objects.get(id=OnboardingQuestion_id)
    
    
    
    # def get_default_on_boarding_question(self) -> QuerySet[OnboardingQuestion]:
    #     default_on_boarding_question = self.get_on_boarding_question_repo().filter(
    #         is_default=True)
    #     return default_on_boarding_question


class QuestionAnswerServices:#--
    
    
    def get_Question_Answer_factory(
        self,
    ) -> Type[QuestionAnswerFactory]:#--
        return QuestionAnswerFactory
    
    
    def get_Question_Answer_repo(self) -> BaseManager[QuestionAnswer]:#--
        return QuestionAnswer.objects
    
    
    @staticmethod
    def get_Question_Answer_by_id(QuestionAnswer_id) -> Type[QuestionAnswer]:#--
        return QuestionAnswer.objects.get(id=QuestionAnswer_id)
    
    
    
     
    # def get_default_Question_Answer(self) -> QuerySet[QuestionAnswer]:
    #     default_Question_Answer = self.get_Question_Answer_repo().filter(
    #         is_default=True)
    #     return default_Question_Answer
    

class QuestionOptionServices:#--
    
    
    def get_Question_Option_factory(
        self,
    ) -> Type[QuestionOptionFactory]:#--
        return QuestionOptionFactory
    
    
    def get_Question_Option_repo(self) -> BaseManager[QuestionOption]:#--
        return QuestionOption.objects
    
    
    @staticmethod
    def get_Question_Option_by_id(QuestionOption_id) -> Type[QuestionOption]:#--
        return QuestionOption.objects.get(id=QuestionOption_id)

