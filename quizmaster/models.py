from django.db import models

# Create your models here.
class QuizQuestion(models.Model):
    statement = models.TextField()
    points = models.IntegerField()
    time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.CharField(max_length=100, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])

    def __str__(self):
        return self.statement

class Option(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion,related_name='options',on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class QuestionTopicMapping(models.Model):
    question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question','topic')

