from dataclasses import dataclass

@dataclass(frozen=True)
class OnboardingQuestionException(Exception):
    item: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.item, self.message)
    
    
    
@dataclass(frozen=True)
class QuestionOptionException(Exception):
    item: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.item, self.message)
    
    

    
@dataclass(frozen=True)
class QuestionAnswerException(Exception):
    item: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.item, self.message)