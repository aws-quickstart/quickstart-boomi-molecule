import requests
import responses
import unittest
from LicenseVerificationAndTokenGenerator import lambda_function
from unittest import mock

class TestLambdaFunction(unittest.TestCase):

    @responses.activate
    def test__verify_boomi_licensing_raise_no_lic(self):
        ACCOUNT='aws-EXAMPLE'
        USER='foobar'
        PASS='blahblah'
        expected_json = {
            "@type" : "Account",
              "licensing" : {
                "@type" : "",
                "standard" : {
                  "@type" : "License",
                  "purchased" : 10,
                  "used" : 9
                },
                "smallBusiness" : {
                  "@type" : "License",
                  "purchased" : 0,
                  "used" : 0
                },
                "enterprise" : {
                  "@type" : "License",
                  "purchased" : 0,
                  "used" : 0
                },
                "tradingPartner" : {
                  "@type" : "License",
                  "purchased" : 3,
                  "used" : 3
                }
              },
              "accountId" : "xyz-A45B82",
              "name" : "XYZ Inc",
              "status" : "active",
              "dateCreated" : "2010-01-01T16:13:11Z",
              "expirationDate" : "2016-03-18T05:00:00Z",
              "suggestionsEnabled" : "true",
              "supportAccess" : True,
              "supportLevel" : "standard"
        }
        responses.add(
            responses.GET,
            f"https://api.boomi.com/api/rest/v1/{ACCOUNT}/Account/{ACCOUNT}",
            json=expected_json,
            status=200
        )
        with self.assertRaises(Exception) as context:
            lambda_function._verify_boomi_licensing(USER, PASS, ACCOUNT)
            self.assertTrue('No enterprise licenses for account aws-EXAMPLE are available. Purchased: 0, Used: 0' in context.exception)

    @responses.activate
    def test__verify_boomi_licensing_pass(self):
        ACCOUNT='aws-EXAMPLE'
        USER='foobar'
        PASS='blahblah'
        expected_json = {
            "@type" : "Account",
              "licensing" : {
                "@type" : "",
                "standard" : {
                  "@type" : "License",
                  "purchased" : 10,
                  "used" : 9
                },
                "smallBusiness" : {
                  "@type" : "License",
                  "purchased" : 0,
                  "used" : 0
                },
                "enterprise" : {
                  "@type" : "License",
                  "purchased" : 5,
                  "used" : 3
                },
                "tradingPartner" : {
                  "@type" : "License",
                  "purchased" : 3,
                  "used" : 3
                }
              },
              "accountId" : "xyz-A45B82",
              "name" : "XYZ Inc",
              "status" : "active",
              "dateCreated" : "2010-01-01T16:13:11Z",
              "expirationDate" : "2016-03-18T05:00:00Z",
              "suggestionsEnabled" : "true",
              "supportAccess" : True,
              "supportLevel" : "standard"
        }
        responses.add(
            responses.GET,
            f"https://api.boomi.com/api/rest/v1/{ACCOUNT}/Account/{ACCOUNT}",
            json=expected_json,
            status=200
        )
        lambda_function._verify_boomi_licensing(USER, PASS, ACCOUNT)

    @responses.activate
    def test__verify_boomi_licensing_raise_used_lic(self):
        ACCOUNT='aws-EXAMPLE'
        USER='foobar'
        PASS='blahblah'
        expected_json = {
            "@type" : "Account",
              "licensing" : {
                "@type" : "",
                "standard" : {
                  "@type" : "License",
                  "purchased" : 10,
                  "used" : 9
                },
                "smallBusiness" : {
                  "@type" : "License",
                  "purchased" : 0,
                  "used" : 0
                },
                "enterprise" : {
                  "@type" : "License",
                  "purchased" : 5,
                  "used" : 5
                },
                "tradingPartner" : {
                  "@type" : "License",
                  "purchased" : 3,
                  "used" : 3
                }
              },
              "accountId" : "xyz-A45B82",
              "name" : "XYZ Inc",
              "status" : "active",
              "dateCreated" : "2010-01-01T16:13:11Z",
              "expirationDate" : "2016-03-18T05:00:00Z",
              "suggestionsEnabled" : "true",
              "supportAccess" : True,
              "supportLevel" : "standard"
        }
        responses.add(
            responses.GET,
            f"https://api.boomi.com/api/rest/v1/{ACCOUNT}/Account/{ACCOUNT}",
            json=expected_json,
            status=200
        )
        with self.assertRaises(Exception) as context:
            lambda_function._verify_boomi_licensing(USER, PASS, ACCOUNT)
            self.assertTrue('No enterprise licenses for account aws-EXAMPLE are available. Purchased: 5, Used: 5' in context.exception)

    @responses.activate
    def test__verify_boomi_licensing_raise_used_lic(self):
        ACCOUNT='aws-EXAMPLE'
        USER='foobar'
        PASS='blahblah'
        expected_json = {
            "@type" : "Account",
              "licensing" : {
                "@type" : "",
                "standard" : {
                  "@type" : "License",
                  "purchased" : 10,
                  "used" : 9
                },
                "smallBusiness" : {
                  "@type" : "License",
                  "purchased" : 0,
                  "used" : 0
                },
                "enterprise" : {
                  "@type" : "License",
                  "purchased" : 5,
                  "used" : 5
                },
                "tradingPartner" : {
                  "@type" : "License",
                  "purchased" : 3,
                  "used" : 3
                }
              },
              "accountId" : "xyz-A45B82",
              "name" : "XYZ Inc",
              "status" : "deleted",
              "dateCreated" : "2010-01-01T16:13:11Z",
              "expirationDate" : "2016-03-18T05:00:00Z",
              "suggestionsEnabled" : "true",
              "supportAccess" : True,
              "supportLevel" : "standard"
        }
        responses.add(
            responses.GET,
            f"https://api.boomi.com/api/rest/v1/{ACCOUNT}/Account/{ACCOUNT}",
            json=expected_json,
            status=200
        )
        with self.assertRaises(Exception) as context:
            lambda_function._verify_boomi_licensing(USER, PASS, ACCOUNT)
            self.assertTrue('Boomi account aws-EXAMPLE is inactive' in context.exception)
if __name__ == '__main__':
    unittest.main()
