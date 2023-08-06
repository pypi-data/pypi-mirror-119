import os
from os import environ
from typing import List, Dict, Any

from _pytest.config import Config, ExitCode
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item
from _pytest.terminal import TerminalReporter

from pytest_xray.constant import (
    JIRA_XRAY_FLAG,
    XRAY_PLUGIN,
    XRAY_TEST_PLAN_ID,
    XRAY_EXECUTION_ID,
    JIRA_CLOUD
)
from pytest_xray.helper import (
    associate_marker_metadata_for,
    get_test_key_for,
    Status,
    TestCase,
    TestExecution,
    StatusBuilder,
    CloudStatus
)
from pytest_xray.xray_publisher import XrayPublisher, BearerAuth, XrayError


def get_request_options() -> Dict[str, Any]:
    """Read configuration from environment variables."""
    options = {}
    jira_url = environ['XRAY_API_BASE_URL']
    user = environ.get('XRAY_API_USER', '')
    password = environ.get('XRAY_API_PASSWORD', '')
    client_id = environ.get('XRAY_CLIENT_ID', '')
    client_secret = environ.get('XRAY_CLIENT_SECRET', '')
    verify = os.environ.get('XRAY_API_VERIFY_SSL', 'True')

    if verify.upper() == 'TRUE':
        verify = True
    elif verify.upper() == 'FALSE':
        verify = False
    else:
        if not os.path.exists(verify):
            raise FileNotFoundError(f'Cannot find certificate file "{verify}"')

    options['BASE_URL'] = jira_url
    options['USER'] = user
    options['PASSWORD'] = password
    options['VERIFY'] = verify
    options['CLIENT_ID'] = client_id
    options['CLIENT_SECRET'] = client_secret

    return options


def pytest_configure(config: Config) -> None:
    if not config.getoption(JIRA_XRAY_FLAG):
        return

    options = get_request_options()
    if config.getoption(JIRA_CLOUD):
        auth = BearerAuth(
            options['BASE_URL'],
            options['CLIENT_ID'],
            options['CLIENT_SECRET']
        )
    else:
        auth = (options['USER'], options['PASSWORD'])

    plugin = XrayPublisher(
        base_url=options['BASE_URL'],
        auth=auth,
        verify=options['VERIFY']
    )

    config.pluginmanager.register(plugin, XRAY_PLUGIN)
    config.addinivalue_line(
        'markers', 'xray(JIRA_ID): mark test with JIRA XRAY test case ID'
    )


def pytest_addoption(parser: Parser):
    xray = parser.getgroup('Jira Xray report')
    xray.addoption(
        JIRA_XRAY_FLAG,
        action='store_true',
        default=False,
        help='Upload test results to JIRA XRAY'
    )
    xray.addoption(
        JIRA_CLOUD,
        action='store_true',
        default=False,
        help='Upload test results to JIRA XRAY could server'
    )
    xray.addoption(
        XRAY_EXECUTION_ID,
        action='store',
        default=None,
        help='XRAY Test Execution ID'
    )
    xray.addoption(
        XRAY_TEST_PLAN_ID,
        action='store',
        default=None,
        help='XRAY Test Plan ID'
    )


def pytest_collection_modifyitems(config: Config, items: List[Item]) -> None:
    if not config.getoption(JIRA_XRAY_FLAG):
        return

    for item in items:
        associate_marker_metadata_for(item)


def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: ExitCode, config: Config) -> None:
    if not config.getoption(JIRA_XRAY_FLAG):
        return

    test_execution_id = terminalreporter.config.getoption(XRAY_EXECUTION_ID)
    test_plan_id = terminalreporter.config.getoption(XRAY_TEST_PLAN_ID)
    is_cloud_server = terminalreporter.config.getoption(JIRA_CLOUD)

    if is_cloud_server:
        status_builder = StatusBuilder(CloudStatus)
    else:
        status_builder = StatusBuilder(Status)

    test_execution = TestExecution(
        test_execution_key=test_execution_id,
        test_plan_key=test_plan_id
    )

    stats = terminalreporter.stats
    if 'passed' in stats:
        for item in stats['passed']:
            test_key = get_test_key_for(item)
            if test_key:
                tc = TestCase(test_key, status_builder('PASS'))
                test_execution.append(tc)
    if 'failed' in stats:
        for item in stats['failed']:
            test_key = get_test_key_for(item)
            if test_key:
                tc = TestCase(test_key, status_builder('FAIL'), item.longreprtext)
                test_execution.append(tc)
    if 'skipped' in stats:
        for item in stats['skipped']:
            test_key = get_test_key_for(item)
            if test_key:
                tc = TestCase(test_key, status_builder('ABORTED'), item.longreprtext)
                test_execution.append(tc)

    xray_publisher = terminalreporter.config.pluginmanager.get_plugin(XRAY_PLUGIN)
    try:
        issue_id = xray_publisher.publish(test_execution)
    except XrayError as exc:
        terminalreporter.ensure_newline()
        terminalreporter.section('Jira XRAY', sep='-', red=True, bold=True)
        terminalreporter.write_line('Could not publish results to Jira XRAY!')
        if exc.message:
            terminalreporter.write_line(exc.message)
    else:
        if issue_id:
            terminalreporter.write_sep('-', f'Uploaded results to JIRA XRAY. Test Execution Id: {issue_id}')
