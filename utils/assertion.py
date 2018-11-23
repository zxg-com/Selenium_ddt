#coding = utf-8
"""
在这里添加各种自定义的断言，断言失败抛出AssertionError就OK。
"""
from utils.log import logger
import asserts

def assertHTTPCode(response, code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        logger.error('响应code不在列表中！')  # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error

def assertstatus(response):
    res_status=response.json()['responseObject']['responseStatus']
    asserts.assert_equal(res_status,True)



def assertIn(content,res):
    try:
        asserts.assert_in(content,res)
    except Exception as e:
        logger.error(e)


def assertNotIn(content,res):
    try:
        asserts.assert_not_in(content,res)
    except Exception as e:
        logger.error(e)


def assertEqual(content,res):
    try:
        asserts.assert_equal(content,res)
    except Exception as e:
        logger.error(e)


def assertNotEqual(content,res):
    try:
        asserts.assert_not_equal(content,res)
    except Exception as e:
        logger.error(e)


def assertIsNone(res):
    try:
        asserts.assert_is_none(res)
    except Exception as e:
        logger.error(e)


def assertIsNotNone(res):
    try:
        asserts.assert_is_not_none(res)
    except Exception as e:
        logger.error(e)