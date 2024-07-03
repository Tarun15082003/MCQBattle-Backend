from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizQuestionSerializer
from .models import QuizQuestion,Topic,QuestionTopicMapping
from django.shortcuts import get_object_or_404
from django.db import transaction
import random


# Create your views here.

class QuizQuestionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = QuizQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Question added successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,*args,**kwargs):
        topic_name = request.query_params.get('topic',None)
        
        if topic_name:
            topic = Topic.objects.filter(name=topic_name).first()
            if not topic:
                return Response({"detail": "Topic not found"},status=status.HTTP_404_NOT_FOUND)
            
            question_mappings = QuestionTopicMapping.objects.filter(topic=topic)
            questions = QuizQuestion.objects.filter(id__in=question_mappings.values('question'))
        else:
            questions = QuizQuestion.objects.all()
        
        if not questions.exists():
            return Response({"detail": "No questions available"},status=status.HTTP_404_NOT_FOUND)
        
        selected_questions = random.sample(list(questions),min(len(questions),20))

        question_ids = [question.id for question in selected_questions]

        return Response({"question_ids": question_ids},status=status.HTTP_200_OK)

    
    @transaction.atomic
    def put(self,request,*args,**kwargs):
        question_id = kwargs.get('question_id')
        quiz_question = QuizQuestion.objects.filter(id=question_id).first()
        if not quiz_question:
            return Response({"detail":"Question not found"},status = status.HTTP_404_NOT_FOUND)

        serializer = QuizQuestionSerializer(quiz_question,data = request.data)
        if serializer.is_valid():
            serializer.save()
            self.delete_orphaned_topics()
            return Response({"detail":"Question updated successfully"},status = status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    
    @transaction.atomic
    def delete(self,request,*args,**kwargs):
        question_id = kwargs.get('question_id')
        quiz_question = get_object_or_404(QuizQuestion,id=question_id)

        quiz_question.delete()
        self.delete_orphaned_topics()
        return Response("Question deleted Successfully",status=status.HTTP_204_NO_CONTENT)


    def delete_orphaned_topics(self):

        all_topics = Topic.object.all()
        for topic in all_topics:
            question_count = QuestionTopicMapping.object.filter(topic=topic).count()
            if question_count == 0:
                topic.delete()

