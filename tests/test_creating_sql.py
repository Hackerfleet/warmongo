"""
Changes notice
==============

This file has been changed by the Hackerfleet Community and this notice has
been added in accordance to the Apache License 2.0

"""

import unittest

import warmongo


class TestCreatingSQL(unittest.TestCase):

    def setUp(self):
        self.schema = {
            'name': 'Country',
            'sql': True,
            'id': '#Country',
            'properties': {
                'name': {'type': 'string'},
                'abbreviation': {'type': 'string', 'primary': True},
                'dialcode': {'type': 'integer'}
            },
            'additionalProperties': False,
        }

        # Connect to warmongo_test sql database - hopefully it doesn't exist
        warmongo.connect_sql(":memory:", 'sqlite', '', '', '', 0)
        #warmongo.connect_sql("warmongo_test", 'mysql+mysqldb', 'riot', 'foobar', 'localhost', 3306)
        self.Country = warmongo.model_factory(self.schema)

        # Drop all the data in it
        #self.Country.clear()

        # Create some defaults
        self.Country({
            "name": "Sweden",
            "abbreviation": "SE",
            "dialcode": 46
        }).save()
        self.Country({
            "name": "United States of America",
            "abbreviation": "US",
            "dialcode": 1
        }).save()

    def testNormalCreateSQL(self):
        """ Test with doing things the SQL way """

        canada = self.Country({
            "name": "Canada",
            "abbreviation": "CA",
            "dialcode": 1
        })

        canada.save()

        country = self.Country.find({'dialcode': 1}, skip=1)

        from pprint import pprint
        for item in country:
            pprint(item.serializablefields())

        #canada.delete()

        self.assertEqual("Canada", canada.name)
        self.assertEqual("CA", canada.abbreviation)
        self.assertEqual(1, canada.dialcode)

