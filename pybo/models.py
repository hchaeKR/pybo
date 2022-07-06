from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField()
    last_upd = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField()
    last_upd = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):        
        return str(self.question) + ' - ' + self.content[0:5] + '...'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField()
    last_upd = models.DateTimeField()

    def __str__(self):
        # return self.objects.order_by('-last_upd')
        return self.content