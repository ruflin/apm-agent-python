import boto3
import mock

import elasticapm
import elasticapm.instrumentation.control
from elasticapm.traces import trace
from tests.helpers import get_tempstoreclient
from tests.utils.compat import TestCase


class InstrumentBotocoreTest(TestCase):
    def setUp(self):
        self.client = get_tempstoreclient()
        elasticapm.instrumentation.control.instrument()

    @mock.patch("botocore.endpoint.Endpoint.make_request")
    def test_botocore_instrumentation(self, mock_make_request):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = (mock_response, {})

        self.client.begin_transaction("transaction.test")
        with trace("test_pipeline", "test"):
            session = boto3.Session(aws_access_key_id='foo',
                                    aws_secret_access_key='bar',
                                    region_name='us-west-2')
            ec2 = session.client('ec2')
            ec2.describe_instances()
        self.client.end_transaction("MyView")

        transactions = self.client.instrumentation_store.get_all()
        traces = transactions[0]['traces']
        self.assertIn('ec2:DescribeInstances', map(lambda x: x['name'], traces))
