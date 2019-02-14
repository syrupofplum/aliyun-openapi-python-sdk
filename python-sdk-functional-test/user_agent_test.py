# encoding:utf-8

from base import SDKTestBase, MyServer
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkcore.client import AcsClient


class UserAgentTest(SDKTestBase):
    request_class = DescribeRegionsRequest

    @staticmethod
    def joint_default_user_agent():
        import platform
        base = '%s (%s %s;%s) Python/%s Core/%s python-requests/%s' \
               % ('AlibabaCloud',
                  platform.system(),
                  platform.release(),
                  platform.machine(),
                  platform.python_version(),
                  __import__('aliyunsdkcore').__version__,
                  __import__('aliyunsdkcore.vendored.requests').__version__)
        return base

    @staticmethod
    def do_request(client, request):
        with MyServer() as s:
            client.do_action_with_exception(request)
            user_agent = s.headers.get('User-Agent')
            return user_agent

    def init_client(self):
        return AcsClient(self.access_key_id, self.access_key_secret, self.region_id,
                         timeout=120, port=51352)

    def test_default_user_agent(self):
        client = self.init_client()
        request = self.request_class()
        request.set_endpoint("localhost")

        self.assertEqual(self.joint_default_user_agent(), self.do_request(client, request))

    def test_append_user_agent(self):
        client = self.init_client()
        request = self.request_class()
        client.append_user_agent('group', 'ali')
        request.set_endpoint("localhost")
        request.append_user_agent('cli', '1.0.0')

        self.assertEqual(self.joint_default_user_agent() + ' group/ali' + ' cli/1.0.0',
                         self.do_request(client, request))

    def test_request_set_user_agent(self):
        client = self.init_client()
        request = self.request_class()
        client.append_user_agent('group', 'ali')
        request.set_endpoint("localhost")
        request.set_user_agent('ali')
        request.append_user_agent('cli', '1.0.0')

        self.assertEqual(self.joint_default_user_agent() + ' extra/ali',
                         self.do_request(client, request))

    def test_client_set_user_agent(self):
        client = self.init_client()
        request = self.request_class()
        client.set_user_agent('alibaba')
        client.append_user_agent('group', 'ali')
        request.set_endpoint("localhost")
        request.set_user_agent('ali')
        request.append_user_agent('cli', '1.0.0')

        self.assertEqual(self.joint_default_user_agent() + ' extra/alibaba',
                         self.do_request(client, request))
