import unittest
from unittest.mock import patch, MagicMock

import requests

import huawei_api


class TestHuaweiApi(unittest.TestCase):
    def test_init_defaults(self):
        ha = huawei_api.HuaweiAPI()
        self.assertEqual(ha.api_url, 'http://192.168.8.1/api/')

    def test_init(self):
        ha = huawei_api.HuaweiAPI(host='modem.local')
        self.assertEqual(ha.api_url, 'http://modem.local/api/')

    @patch.object(huawei_api.HuaweiAPI, 'ping')
    @patch.object(huawei_api.HuaweiAPI, '_HuaweiAPI__login', return_value=None)
    def test_login(self, mock_login, mock_ping):
        ha = huawei_api.HuaweiAPI(host='192.168.9.2')
        ha.login('admin', 'secret')
        mock_login.assert_called_with('admin', 'secret')
        # mock_ping.assert_called_once()

    @patch.object(huawei_api.HuaweiAPI, '_HuaweiAPI__get_token')
    def test_api_post_err(self, mock_token):
        mock_token.return_value = '1234'
        ha = huawei_api.HuaweiAPI(host='192.168.9.2')
        mock_session = MagicMock(side_effect=requests.exceptions.RequestException())
        with self.assertRaises(huawei_api.HuaweiAPIException):
            rsp = ha._HuaweiAPI__api_post('/foo', None)

    @patch.object(huawei_api.HuaweiAPI, '_HuaweiAPI__get_token')
    def test_api_post(self, mock_token):
        mock_token.return_value = '1234'

        data = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
        <foo>bar</foo>
</response>
'''
        mock_response = MagicMock(status_code=200, text=data, content=data)

        ha = huawei_api.HuaweiAPI(host='192.168.9.2')
        mock_session = MagicMock()
        mock_session.post.return_value = mock_response

        ha.session = mock_session
        rsp = ha._HuaweiAPI__api_post('foo', None)
        mock_session.post.assert_called_with(url='http://192.168.9.2/api/foo', data=u'<?xml version="1.0" encoding="utf-8"?>\n<request></request>',
                                        headers={'__RequestVerificationToken': '1234'},
                                        timeout=(1.5, 1.5))

    def test_get_token(self):
        ha = huawei_api.HuaweiAPI(host='192.168.9.2')
        mock_session = MagicMock()
        data='<?xml version="1.0" encoding="UTF-8"?><response><TokInfo>C6k8T0Qrk8igZAfEZvhGnBldijSo06WcxF8JW3ZBKgSp0UVBy0YtM278vVF6Lgt3</TokInfo></response>'
        mock_response = MagicMock(status_code=200, text=data)
        mock_session.get.return_value = mock_response

        ha.session = mock_session
        token = ha._HuaweiAPI__get_token()
        mock_session.get.assert_called_with(url='http://192.168.9.2/api/webserver/SesTokInfo',
                                            allow_redirects=False,
                                            timeout=(1.5, 1.5))
        self.assertEqual(token, 'C6k8T0Qrk8igZAfEZvhGnBldijSo06WcxF8JW3ZBKgSp0UVBy0YtM278vVF6Lgt3')

    def test_client_proof(self):
        ha = huawei_api.HuaweiAPI(host='192.168.9.2')
        proof = ha._HuaweiAPI__get_client_proof('1234',
                                        '252ada06446f5d8421fca709a245e08304fceee621ab39e5aa27d3928564fb952gmWtqQ7ja3I0g8xmTTSBGxCvbBhZBuI',
                                        'secret',
                                        '6728e00f4a0fb30ed1aef3ae5ed62dabe9ce928835ce51b0fd68b7a78293b000',
                                        500)
        self.assertEqual(proof, '90c1042f07aeda10037c7a99b45cfba6da263e70699c1ae62113009a20ee8c67')


    challenge_login = '''<?xml version="1.0" encoding="UTF-8"?><response><servernonce>252ada06446f5d8421fca709a245e08304fceee621ab39e5aa27d3928564fb952gmWtqQ7ja3I0g8xmTTSBGxCvbBhZBuI</servernonce><modeselected>1</modeselected><salt>6728e00f4a0fb30ed1aef3ae5ed62dabe9ce928835ce51b0fd68b7a78293b000</salt><iterations>500</iterations></response>'''
