import django_filters
from taste_dna.domain.on_boarding_questions.models import QuestionAnswer,QuestionOption,OnboardingQuestion

from django_filters import Filter

class ArrayFilter(Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{f'{self.field_name}__contains': value})
        # print(qs.filter(**{f'{self.field_name}__contains': value}),"qs is")
        return qs
        
class QuestionOptionFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionOption
        fields = ['option']
    
    statement = django_filters.CharFilter(field_name='question_id__statement', lookup_expr='icontains')
    option =  ArrayFilter(field_name='option')