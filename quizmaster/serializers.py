from rest_framework import serializers
from .models import QuizQuestion, Option, Topic, QuestionTopicMapping
from django.db import transaction

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('text','is_correct')
    
    def validate(self,data):
        if 'text' not in data or data['text'].strip() =='':
            raise serializers.ValidationError("Option cannot be empty.")
        
        return data
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

    def validate(self,data):
        if 'name' not in data or data['name'].strip() =='':
            raise serializers.ValidationError("Topic cannot be empty.")

        return data
    
class QuizQuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    topics = TopicSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = '__all__'

    def validate(self,data):
        if 'statement' not in data or data['statement'].strip()=='':
             raise serializers.ValidationError("Statement cannot be empty.")

        return data

    def create(self,validated_data):
        statement = validated_data['statement']

        if QuizQuestion.objects.filter(statement=statement).exists():
            raise serializers.ValidationError("A question with this statement already exists.")

        options_data = validated_data.pop('options')
        topics_data = validated_data.pop('topics')

        try:
            with transaction.atomic():
                # Create the quiz question
                quiz_question = QuizQuestion.objects.create(**validated_data)
                print(quiz_question)

                # Create options for the quiz question
                for option_data in options_data:
                    Option.objects.create(quiz_question=quiz_question, **option_data)

                # Create or retrieve topics and map them to the quiz question
                for topic_data in topics_data:
                    topic, _ = Topic.objects.get_or_create(name=topic_data['name'])
                    QuestionTopicMapping.objects.create(question=quiz_question, topic=topic)
                
                return quiz_question
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def update(self,instance,data):
        options_data = data.pop('options')
        topics_data = data.pop('topics')

        try:
            with transaction.atomic():

                instance.statement = data.get('statement',instance.statement)
                instance.points = data.get('points',instance.points)
                instance.time = data.get('time',instance.time)
                instance.difficulty = data.get('statement',instance.difficulty)
                instance.save()
                

                instance.options.all().delete()
                for option_data in options_data:
                    Option.objects.create(quiz_question=instance,**option_data)

                instance.questiontopicmapping_set.all().delete()
                for topic_data in topics_data:
                    topic , _ = Topic.objects.get_or_create(name = topic_data['name'])
                    QuestionTopicMapping.objects.create(question=instance,topic = topic)

            return instance
        except Exception as e:
            raise serializers.ValidationError(str(e))


        
