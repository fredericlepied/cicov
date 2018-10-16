from junitparser import JUnitXml


def _get_status(testcase):
    if testcase.result:
        return testcase.result._elem.tag
    return "success"


def _get_name(testcase):
    idx = testcase.name.find("[")
    if idx == -1:
        return testcase.classname + "." + testcase.name
    return testcase.classname + "." + testcase.name[:idx]


def parse_tests(xml_file_object):
    xml = JUnitXml.fromfile(xml_file_object)
    tests = []
    for testcase in xml:
        testcase_status = _get_status(testcase)
        if testcase.classname != "" and testcase_status != "skipped":
            tests.append({"name": _get_name(testcase), "status": testcase_status})
    return tests
