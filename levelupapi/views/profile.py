from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer, Game


class Profile(ViewSet):

    def list(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(registrations__gamer=gamer)

        events = EventSerializer(events, many=True, context={'request': request})
        gamer = GamerSerializer(gamer, many=False, context={'request': request})

        profile = {}
        profile["gamer"] = gamer.data 
        profile["events"] = events.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('first_name', 'last_name', 'username')

class GamerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Gamer
        fields = ('user', 'bio')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(view_name='game', lookup_field='id')
        fields = ('title',)

class EventSerializer(serializers.HyperlinkedModelSerializer):
    game = GameSerializer(many=False)
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(view_name='event', lookup_field='id')
        fields = ('id', 'url', 'game', 'description', 'date', 'time')
