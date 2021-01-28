import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        url = "/register"
        data = {
            "username": "steve",
            "password": "admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gametype = GameType()
        gametype.label = "Board Game"
        gametype.save()

    def test_create_game(self):
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["skill_level"], 5)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "skillLevel": 2,
            "title": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["maker"], "Hasbro")
        self.assertEqual(json_response["skill_level"], 2)
        self.assertEqual(json_response["number_of_players"], 4)
