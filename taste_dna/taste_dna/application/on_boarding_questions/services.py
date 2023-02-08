from django.db.models.query import QuerySet
# from rest_framework_simplejwt.tokens import RefreshToken
from taste_dna.domain.users.models import User

from taste_dna.domain.users.services import UserServices

from taste_dna.domain.on_boarding_questions.models import (
    QuestionAnswer,QuestionOption,OnboardingQuestion,
)
from taste_dna.application.on_boarding_questions.exceptions import OnboardingQuestionException,QuestionOptionException,QuestionAnswerException

from taste_dna.domain.on_boarding_questions.services import (
    QuestionOptionServices,QuestionAnswerServices,OnBoardingQuestionsServices
)
from taste_dna.application.users.services import UserAppServices

class OnboardingQuestionAppServices:
    

    def __init__(self):
        self.On_Boarding_Questions_services = OnBoardingQuestionsServices()#--
        self.On_Boarding_Questions_queryset = self._get_On_Boarding_Questions_list()
        
        
    def get_On_Boarding_Questions_by_pk(self,On_boarding_Question_id) -> OnboardingQuestion:#--
        return self.On_Boarding_Questions_queryset.get(id=On_boarding_Question_id)   
        
          
    def _get_On_Boarding_Questions_list(self) -> QuerySet[User]:

        return self.On_Boarding_Questions_services.get_on_boarding_question_repo()
    
    
    
    def create_On_Boarding_Questions_from_dict(self, data: dict) -> OnboardingQuestion:#--
     
        statement = data.get("statement", None)
        question_type = data.get("question_type", None)
        order = data.get("order", None)
        
        try:
            on_boarding_question_factory = self.On_Boarding_Questions_services.get_on_boarding_question_factory()
            on_boarding_question = on_boarding_question_factory.build_entity_with_id(
                statement=statement, question_type=question_type, order=order
                )
            on_boarding_question.save()
            return on_boarding_question
        except Exception as e:
            raise OnboardingQuestionException("on-boarding-question-create-exception", str(e))
    
    
    def create_on_boarding_question_option(self,data: dict):
        
        statement = data.get("statement", None)
        question_type = data.get("question_type", None)
        order = data.get("order", None)
        option=data.get("option",None)
        
        try:
            on_boarding_question_factory = self.On_Boarding_Questions_services.get_on_boarding_question_factory()
            on_boarding_question = on_boarding_question_factory.build_entity_with_id(
                statement=statement, question_type=question_type, order=order
                )
            on_boarding_question.save()
     
            option_services=QuestionOptionServices()
            Question_Option_factory = option_services.get_Question_Option_factory()
            Question_Option = Question_Option_factory.build_entity_with_id(
                  question_id=on_boarding_question, option=option
                )
            Question_Option.save()
            
            return on_boarding_question, Question_Option
        except Exception as e:
            raise OnboardingQuestionException("on-boarding-question-create-exception", str(e))
        
    
    
    
    def update_On_Boarding_Questions_by_id_from_dict(
        self, instance: OnboardingQuestion, data: dict
    ) -> OnboardingQuestion:
       
        statement = data.get("statement", None)
        question_type = data.get("question_type", None)
        order = data.get("order", None)
        is_active=data.get("is_active",False)


        try:
            question_repo =self.On_Boarding_Questions_services.get_on_boarding_question_repo()
            active_question = question_repo.filter(is_active=True)
            if active_question and is_active:
                for _question in active_question:
                    _question.is_active = False
                    _question.save()
                    
            instance.update_entity(
                statement=statement,
                question_type=question_type,
                order=order,
                is_active=is_active,
            )
            instance.save()
            return instance
        except Exception as e:
            raise OnboardingQuestionException(
               "on-boarding-question-create-exception", str(e)
            )

    def _delete_On_Boarding_Questions_list(self,result) -> QuerySet[User]:

        return self.On_Boarding_Questions_services.delete_on_boarding_question(result)


print("#############=============QuestionOption==========###########################################")

class QuestionOptionAppServices:
    

    def __init__(self):
        self.Question_Option_services = QuestionOptionServices()#--
        self.Question_Option_queryset = self._get_Question_Option_by_role()
        
        
    def get_Question_Option_by_pk(self,Question_Option_id) -> QuestionOption:#--
        return self.Question_Option_queryset.get(id=Question_Option_id)   
        
          
    def _get_Question_Option_by_role(self) -> QuerySet[User]:

        return self.Question_Option_services.get_Question_Option_repo().all()
    
    
    def create_Question_Option_from_dict(self, data: dict) -> QuestionOption:#--
     
        question_id = data.get("question_id", None)
        option = data.get("option", None)
        

        try:
      
            question_services=OnBoardingQuestionsServices()
            question_obj=question_services.get_on_boarding_question_by_id(OnboardingQuestion_id=question_id)
            Question_Option_factory = self.Question_Option_services.get_Question_Option_factory()
            Question_Option = Question_Option_factory.build_entity_with_id(
                  question_id=question_obj, option=option
                )
            Question_Option.save()
            return Question_Option
        except Exception as e:
            raise QuestionOptionException("on-boarding-question-create-exception", str(e))
    
    
    def update_Question_Option_by_id_from_dict(
        self, instance: QuestionOption, data: dict
    ) -> QuestionOption:
       
        question_id = data.get("question_id", None)
        option = data.get("option", None)


        try:
                    
            instance.update_entity(
                question_id = question_id,
                option = option,
                
            )
            instance.save()
            return instance
        except Exception as e:
            raise OnboardingQuestionException(
               "on-boarding-question-create-exception", str(e)
            )
            
            
            
print("#############=============QuestionAnswer==========###########################################")


class QuestionAnswerAppServices:
    

    def __init__(self):
        self.Question_Answer_services = QuestionAnswerServices()#--
        self.Question_Answer_queryset = self._get_Question_Answer_by_role()
        
        
    def get_Question_Answer_by_pk(self,Question_Answer_id) -> QuestionAnswer:#--
        return self.Question_Answer_queryset.get(id=Question_Answer_id)   
        
          
    def _get_Question_Answer_by_role(self) -> QuerySet[User]:

        return self.Question_Answer_services.get_Question_Answer_repo().all()
    
    
    def create_Question_Answer_from_dict(self, data: dict) -> QuestionAnswer:#--
     
        question_id = data.get("question_id", None)
        user_id=data.get("user_id",None)
        answer = data.get("answer", None)
        

        try:
            user_app_services=UserAppServices()
            question_services=OnBoardingQuestionsServices()
            question_obj=question_services.get_on_boarding_question_by_id(OnboardingQuestion_id=question_id)
            user_obj=user_app_services.get_user_by_pk(pk=user_id)
            Question_Answer_factory = self.Question_Answer_services.get_Question_Answer_factory()
            Question_Answer = Question_Answer_factory.build_entity_with_id(
                  question_id=question_obj, user_id=user_obj , answer=answer
                )
            Question_Answer.save()
            return Question_Answer
        except Exception as e:
            raise QuestionAnswerException("on-boarding-question-create-exception", str(e))
    
    
    def update_Question_Answer_by_id_from_dict(
        self, instance: QuestionAnswer, data: dict
    ) -> QuestionAnswer:
       
        question_id = data.get("question_id", None)
        user_id=data.get("user_id",None)
        answer = data.get("answer", None)
        


        try:
                    
            instance.update_entity(
                question_id = question_id,
                user_id = user_id,
                answer = answer
                
            )
            instance.save()
            return instance
        except Exception as e:
            raise QuestionAnswerException(
               "on-boarding-question-create-exception", str(e)
            )