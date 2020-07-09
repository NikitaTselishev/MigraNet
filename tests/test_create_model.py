from unittest import TestCase

import config
import models
import database
import constants


class TestModels(TestCase):
    def test_get_user_model(self):
        db = database.Database(
            config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
        )
        user = models.User.create_from_database(db, 1)

    def test_write_user_model(self):
        db = database.Database(
            config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
        )
        user = models.User.create_in_database(
            db,
            "Testov",
            "Александр",
            123,
            "ficus",
            "89111234455",
            "testov@migra.net",
            constants.Roles.User,
            100,
            constants.Status.Active,
        )
