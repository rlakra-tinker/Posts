#
# Author: Rohtash Lakra
#
from framework.http import HTTPMethod, HTTPStatus, HTTPUtils
from tests.framework.base import AbstractTestCase


class HttpTest(AbstractTestCase):

    def test_http_method(self):
        print("test_http_method()")
        http_method = HTTPMethod.GET
        print(f"http_method={http_method}")
        self.assertEqual(HTTPMethod.GET, http_method)
        self.assertNotEqual(HTTPMethod.POST, http_method)

        expected = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
        self.assertEqual("<enum 'HTTPMethod'>", str(HTTPMethod))
        self.assertEqual(expected, HTTPMethod.names())
        self.assertEqual(expected, HTTPMethod.values())
        text = 'get'
        expected = 'HTTPMethod <GET=GET>'
        print(f"{text} of_name={HTTPMethod.of_name(text)}")
        self.assertEqual(expected, str(HTTPMethod.of_name(text)))
        self.assertTrue(HTTPMethod.equals(HTTPMethod.GET, text))

        text = 'post'
        print(f"{text} of_value={HTTPMethod.of_value(text)}")
        self.assertIsNone(HTTPMethod.of_value(text))
        print()

    def test_is_post(self):
        print("test_is_post()")
        self.assertTrue(HTTPMethod.is_post("post"))
        self.assertTrue(HTTPMethod.is_post("Post"))
        self.assertTrue(HTTPMethod.is_post("POST"))
        self.assertTrue(HTTPMethod.is_post("PoST"))
        self.assertFalse(HTTPMethod.is_post("get"))
        print()

    def test_http_status(self):
        print("test_http_status()")
        http_status = HTTPStatus.CREATED
        print(f"http_status={http_status}")
        self.assertEqual(HTTPStatus.CREATED, http_status)
        self.assertNotEqual(HTTPStatus.OK, http_status)
        expected = "HTTPStatus <CREATED=(201, 'Created')>"
        self.assertEqual(expected, str(http_status))

        self.assertEqual("<enum 'HTTPStatus'>", str(HTTPStatus))
        self.assertEqual(('OK', 'CREATED', 'ACCEPTED', 'NO_CONTENT', 'BAD_REQUEST', 'UNAUTHORIZED', 'NOT_FOUND', 'UNSUPPORTED_MEDIA_TYPE', 'INVALID_DATA', 'TOO_MANY_REQUESTS', 'INTERNAL_SERVER_ERROR'), HTTPStatus.names())
        self.assertEqual(((200, 'OK'), (201, 'Created'), (202, 'Accepted'), (204, 'No Content'), (400, 'Bad Request'), (401, 'Unauthorized'), (404, 'Not Found'), (415, 'Unsupported Media Type'), (422, 'Unprocessable Entity'), (429, 'Too Many Requests'), (500, 'Internal Server Error')), HTTPStatus.values())
        text = 'ok'
        expected = "HTTPStatus <OK=(200, 'OK')>"
        print(f"{text} of_name={HTTPStatus.of_name(text)}")
        self.assertEqual(expected, str(HTTPStatus.of_name(text)))
        self.assertTrue(HTTPStatus.equals(HTTPStatus.OK, text))
        print()

    def test_by_status(self):
        print("test_by_status()")
        self.assertEqual(HTTPStatus.OK, HTTPStatus.by_status(200))
        self.assertEqual(HTTPStatus.CREATED, HTTPStatus.by_status(201))
        self.assertEqual(HTTPStatus.BAD_REQUEST, HTTPStatus.by_status(400))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, HTTPStatus.by_status(401))
        self.assertEqual(HTTPStatus.NOT_FOUND, HTTPStatus.by_status(404))
        self.assertEqual(HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.by_status(429))
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.by_status(500))
        print()

    def test_get_success_statuses(self):
        print("test_get_success_statuses()")
        expected = '[OK <200, OK>, CREATED <201, Created>, ACCEPTED <202, Accepted>, NO_CONTENT <204, No Content>]'
        success_statuses = HTTPStatus.get_success_statuses()
        print(f"success_statuses={success_statuses}")
        self.assertEqual(expected, str(success_statuses))
        self.assertNotEqual(['UNAUTHORIZED <401, Unauthorized>'], str(success_statuses))
        print()

    def test_is_success_status(self):
        print("test_is_success_status()")
        self.assertTrue(HTTPStatus.is_success_status(HTTPStatus.OK))
        self.assertTrue(HTTPStatus.is_success_status(HTTPStatus.CREATED))
        self.assertTrue(HTTPStatus.is_success_status(HTTPStatus.ACCEPTED))
        self.assertTrue(HTTPStatus.is_success_status(HTTPStatus.NO_CONTENT))
        self.assertFalse(HTTPStatus.is_success_status(HTTPStatus.BAD_REQUEST))
        print()

    def test_get_uuid(self):
        print("test_get_uuid()")
        uuid = HTTPUtils.get_uuid()
        print(f"uuid={uuid}")
        self.assertIsNotNone(uuid)
        print()

    def test_get(self):
        print("test_get()")
        http = HTTPUtils()
        print(f"http={http}")
        url = http.get("/posts")
        print(f"url={url}")
        self.assertIsNotNone(url)
        self.assertEqual('GET /posts', url)
        print()

    def test_post(self):
        print("test_post()")
        http = HTTPUtils()
        print(f"http={http}")
        url = http.post("/posts")
        print(f"url={url}")
        self.assertIsNotNone(url)
        self.assertEqual('POST /posts', url)
        print()
