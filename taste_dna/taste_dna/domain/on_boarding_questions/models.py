from django.db import models
from taste_dna.domain.users.models import User
from dataclasses import dataclass
from django.conf import settings
import uuid
from xmlrpc.client import Boolean

from django.contrib.postgres.fields import ArrayField



@dataclass(frozen=True)
class OnboardingQuestionID:
    """
    This is a value object that should be used to generate and pass the
    OnboardingQuestionID to the OnboardingQuestionFactory
    """

    value: uuid.UUID


@dataclass(frozen=True)
class QuestionOptionID:
    """
    This is a value object that should be used to generate and pass the
    QuestionOptionID to the QuestionOptionFactory
    """

    value: uuid.UUID


@dataclass(frozen=True)
class QuestionAnswerID:
    """
    This is a value object that should be used to generate and pass the
    QuestionAnswerID to the QuestionAnswerFactory
    """

    value: uuid.UUID







class OnboardingQuestion(models.Model):
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multiple_choice"
    MULTIPLE_ANSWER= "multiple_answer"
    
    QUESTION_CHOICES = [
        (SINGLE_CHOICE, "single_choice"),
        (MULTI_CHOICE, "multiple_choice"),
        (MULTIPLE_ANSWER, "multiple_answer"),
    ]
    
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    statement = models.CharField(max_length=200,null=True,blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_CHOICES, default=None)
    order=models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # def __str__(self):
    #     return self.statement
    def update_entity(
        self,
        statement: str,
        question_type: str,
        order: int,
        is_active: Boolean,
    ):
        if statement is not None:
            self.statement = statement
        if question_type is not None:
            self.question_type = question_type
        if order is not None:
            self.order = order
        if is_active is not None:
            self.is_active = is_active
    
class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question_id = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    option = ArrayField(models.CharField(max_length=250,null=True,blank=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    def update_entity(
        self,
        question_id: int,
        option: str,
    ):
        if question_id is not None:
            self.question_id = question_id
        if option is not None:
            self.option = option
      
    
    
    
class QuestionAnswer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question_id = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    answer = ArrayField(models.CharField(max_length=250,null=True,blank=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     print(type(self.question_id))
    #     return self.answer
   
    def update_entity(
        self,
        question_id: OnboardingQuestion,
        user_id: User,
        answer: str
    ):
        if question_id is not None:
            self.question_id = question_id
        if user_id is not None:
            self.user_id = user_id
        if answer is not None:
            self.option = answer
    
    
    
    



class OnboardingQuestionFactory:#--
    @staticmethod
    def build_entity(
         id: OnboardingQuestionID,statement: str, question_type: str, order: int
    ) -> OnboardingQuestion:
        return OnboardingQuestion(
           id=id.value,statement=statement, question_type=question_type, order=order
        )

    @classmethod
    def build_entity_with_id(
        cls,
        statement: str, question_type: str, order: int
    ) -> OnboardingQuestion:
        entity_id = OnboardingQuestionID(uuid.uuid4())

        return cls.build_entity(
            id=entity_id,statement=statement, question_type=question_type, order=order
        )
        








class QuestionOptionFactory:
    @staticmethod
    def build_entity(
        id: QuestionOptionID,question_id: OnboardingQuestion, option: list
    ) -> QuestionOption:
        return QuestionOption(
           id=id.value,question_id=question_id, option=option
        )

    @classmethod
    def build_entity_with_id(
        cls,
        question_id:OnboardingQuestion, option: list
    ) -> QuestionOption:
        entity_id = QuestionOptionID(uuid.uuid4())

        return cls.build_entity(
            id=entity_id,question_id=question_id, option=option
        )






class QuestionAnswerFactory:#--
    @staticmethod
    def build_entity(
        id: QuestionAnswerID,question_id: OnboardingQuestion, user_id: User, answer: list
    ) -> QuestionAnswer:
        return QuestionAnswer(
           id=id.value,question_id=question_id, user_id=user_id , answer=answer
        )

    @classmethod
    def build_entity_with_id(
        cls,
        question_id:OnboardingQuestion,user_id: User, answer: list
    ) -> QuestionAnswer:
        entity_id = QuestionAnswerID(uuid.uuid4())

        return cls.build_entity(
            id=entity_id,question_id=question_id,  user_id=user_id , answer=answer
        )


