from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import QuestionAnswerSerializer,QuestionOptionSerializer,OnboardingQuestionSerializer,QuestionAndOptionSerializer,QuestionOptionsRetriveSerializer
from rest_framework.renderers import JSONRenderer
from taste_dna.application.on_boarding_questions.exceptions import OnboardingQuestionException,QuestionAnswerException,QuestionOptionException
from taste_dna.application.on_boarding_questions.services import (
    OnboardingQuestionAppServices ,
    QuestionOptionAppServices ,
    QuestionAnswerAppServices
)
import django_filters
from taste_dna.interface.on_boarding_questions.filter import QuestionOptionFilter
from taste_dna.interface.on_boarding_questions.pagination import CustomPagination


from taste_dna.domain.on_boarding_questions.models import QuestionAnswer,QuestionOption,OnboardingQuestion
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination




class onboardingquestionViewSet(viewsets.ViewSet):
    
    def get_queryset(self):
        on_boarding_question_app_services = OnboardingQuestionAppServices()
        return on_boarding_question_app_services.On_Boarding_Questions_queryset
    
    
    def get_serializer_class(self):
        if self.action == 'create_question_option':
            return QuestionAndOptionSerializer
        return OnboardingQuestionSerializer

    def list(self,request):
        question_options_app_service = QuestionOptionAppServices()
        question_option_query_set = question_options_app_service.Question_Option_queryset
        # print('question_option_query_set',question_option_query_set)
        filter=QuestionOptionFilter(request.GET,queryset=question_option_query_set)
        question_option_query_set=filter.qs
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(question_option_query_set, request)
        if result_page is not None:
            serializer = QuestionOptionsRetriveSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = QuestionOptionsRetriveSerializer(question_option_query_set,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            result = self.get_queryset().get(id=pk)
            serializer = OnboardingQuestionSerializer(result)
            print(serializer.data,"data is =========>>>>>>>>>>>>>")
            return Response(serializer.data)
        
        
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], name='create_question_option')
    def create_question_option(self, request):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)   
        if serializer.is_valid():
            try:
                on_boarding_question_app_services = OnboardingQuestionAppServices()
                on_boarding_question,Question_Option = on_boarding_question_app_services.create_on_boarding_question_option(serializer.data)
                print("question====",on_boarding_question,"option===",Question_Option)
                
                
                
                on_boarding_question_serializer=OnboardingQuestionSerializer(on_boarding_question)
                Question_Option_serializer=QuestionOptionSerializer(Question_Option)
                data_of_all={'question': on_boarding_question_serializer.data, 'option': Question_Option_serializer.data}
                return Response(data_of_all)
            except OnboardingQuestionException as oqe:
                print(oqe)
                
        else:
            print(serializer.error_messages,'JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ')
      
    def create(self, request):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                on_boarding_question_app_services = OnboardingQuestionAppServices()
                on_boarding_question = on_boarding_question_app_services.create_On_Boarding_Questions_from_dict(
                    serializer.data
                )
                serialized_data = OnboardingQuestionSerializer(on_boarding_question)
                return Response(serialized_data.data, status=200)
            
            except OnboardingQuestionException as e:
                print(e.message,"messhahirtgs")
                return Response(e.message, status=400)
        return Response(serializer.error_messages, status=400)

                
    def destroy(self,request,pk):
        print("*********************")
        try:
            result = self.get_queryset().get(id=pk)
            gtas_instance = OnboardingQuestionAppServices()
            gui_theme_instance = gtas_instance._delete_On_Boarding_Questions_list(result)
            return Response({'msg':'data deleted'})

            
        except Exception as e:
            print(e)
            
            
             
    def update(self, request, pk):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        try:
            gtas_instance = OnboardingQuestionAppServices()
            gui_theme_instance = gtas_instance.get_On_Boarding_Questions_by_pk(pk)
        except Exception as e:
            print(e)
            
        if serializer.is_valid():
            try:
                response = gtas_instance.update_On_Boarding_Questions_by_id_from_dict(
                        instance=gui_theme_instance, data=serializer.data
                    )
                serialized_data = get_serializer(response)
                return Response(serialized_data.data, status=200)
            except Exception as e:
                print(e)
        else:
            print(serializer.error_messages,"sfsdfsdf")
    
print("===============question answer view=======================")
    
class QuestionAnswerViewSet(viewsets.ViewSet):
    
    def get_queryset(self):
        Question_Answer_app_services = QuestionAnswerAppServices()
        return Question_Answer_app_services._get_Question_Answer_by_role()
    
    
    def get_serializer_class(self):
        return QuestionAnswerSerializer

    
    
    
    def list(self,request):
        result = self.get_queryset().all()
        serializer = QuestionAnswerSerializer(result,many=True)
        # print(serializer.data,"list of da ")
        id_questio=[]
        for i in serializer.data:
            for j in i:
                if j=='question_id':
                    id_questio.append(i[j])
                    print(f'{j} = {i[j]}')       
                # print(serializer.data[i])

            # print(i[0],"data is ansewr")
        print(id_questio,"list of id is=================>>>>.")
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            result = self.get_queryset().get(id=pk)
            serializer = QuestionAnswerSerializer(result)
            print(serializer.data,"data is =========>>>>>>>>>>>>>")
            return Response(serializer.data)
        
        
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
      
    def create(self, request):
        print("******************* post answer")
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                print(serializer.data,"data of ansert is ")
                Question_Answer_app_services = QuestionAnswerAppServices()
                Question_Answer = Question_Answer_app_services.create_Question_Answer_from_dict(
                    serializer.data
                )
                serialized_data = QuestionAnswerSerializer(Question_Answer)
                return Response(serialized_data.data, status=200)
            
            except QuestionAnswerException as e:
                print(e.message,"messhahirtgs")
                return Response(e.message, status=400)
        else:
            return Response(serializer.error_messages, status=400)
        
        
                 
    def update(self, request, pk):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        try:
            gtas_instance = QuestionAnswerAppServices()
            gui_theme_instance = gtas_instance.get_Question_Answer_by_pk(pk)
        except Exception as e:
            print(e)
            
        if serializer.is_valid():
            try:
                response = gtas_instance.update_Question_Answer_by_id_from_dict(
                        instance=gui_theme_instance, data=serializer.data
                    )
                serialized_data = get_serializer(response)
                return Response(serialized_data.data, status=200)
            except Exception as e:
                print(e)
        else:
            print(serializer.error_messages,"sfsdfsdf")
                
                
print("===============question option view=======================")





class QuestionOptionViewSet(viewsets.ViewSet):
    
    def get_queryset(self):
        Question_Option_app_services = QuestionOptionAppServices()
        return Question_Option_app_services._get_Question_Option_by_role()
    
    
    def get_serializer_class(self):
        return QuestionOptionSerializer

    
    
    
    def list(self,request):
        result = self.get_queryset().all()
        serializer = QuestionOptionSerializer(result,many=True)
        print(serializer.data,"list of da ")
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            result = self.get_queryset().get(id=pk)
            serializer = QuestionOptionSerializer(result)
            print(serializer.data,"data is =========>>>>>>>>>>>>>")
            return Response(serializer.data)
        
        
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
      
    def create(self, request):
        print("******option")
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)

        if serializer.is_valid():
            print("fsdf")
            try:
                Question_Option_app_services = QuestionOptionAppServices()
                Question_Option = Question_Option_app_services.create_Question_Option_from_dict(
                    serializer.data
                )
                serialized_data = QuestionOptionSerializer(Question_Option)
                return Response(serialized_data.data, status=200)
            
            except Exception as e:
                print(e)
        else:
            return Response(serializer.error_messages, status=400)
        
        
        
        
                       
    def update(self, request, pk):
        get_serializer = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        try:
            gtas_instance = QuestionOptionAppServices()
            gui_theme_instance = gtas_instance.get_Question_Option_by_pk(pk)
        except Exception as e:
            print(e)
            
        if serializer.is_valid():
            try:
                response = gtas_instance.update_Question_Option_by_id_from_dict(
                        instance=gui_theme_instance, data=serializer.data
                    )
                serialized_data = get_serializer(response)
                return Response(serialized_data.data, status=200)
            except Exception as e:
                print(e)
        else:
            print(serializer.error_messages,"error is==>")