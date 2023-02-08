from rest_framework import serializers
from taste_dna.domain.on_boarding_questions.models import OnboardingQuestion, QuestionOption,QuestionAnswer


class OnboardingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestion
        fields = ['id','statement','order']

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id','question_id','option']
        
class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = "__all__"
        
        
class QuestionAndOptionSerializer(serializers.Serializer):
    
    
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multiple_choice"
    MULTIPLE_ANSWER= "multiple_answer"
    
    QUESTION_CHOICES = [
        (SINGLE_CHOICE, "single_choice"),
        (MULTI_CHOICE, "multiple_choice"),
        (MULTIPLE_ANSWER, "multiple_answer"),
    ]
    statement = serializers.CharField(max_length=200,required=True)
    question_type= serializers.ChoiceField(choices=QUESTION_CHOICES)
    order = serializers.IntegerField(required=True)
    option = serializers.ListField(max_length=250,required=True)
    
class QuestionOptionsRetriveSerializer(serializers.ModelSerializer):
    question_id = OnboardingQuestionSerializer()
    class Meta:
        model = QuestionOption
        fields = '__all__'
