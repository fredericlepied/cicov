import os
import unittest

from api import junit_parser


class JunitParserCase(unittest.TestCase):
    def test_parse_junit_file(self):
        xmlfile = open(
            os.path.join(os.path.dirname(__file__), "tempest-results-full.1.xml")
        )
        tests = junit_parser.parse_tests(xmlfile)
        self.assertEqual(len(tests), 1197)
        self.assertDictEqual(
            tests[0],
            {
                "name": "tempest.api.compute.admin.test_simple_tenant_usage_negative.TenantUsagesNegativeTestJSON.test_get_usage_tenant_with_empty_tenant_id",
                "status": "success",
            },
        )
