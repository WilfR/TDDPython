from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time
import os

MAX_WAIT_TIME = 10

class FunctionalTest( StaticLiveServerTestCase ) :

    def setUp( self ) :
        self.browser = webdriver.Firefox()
        stagingServer = os.environ.get('STAGING_SERVER')
        ### print(f"Staging Server={stagingServer}")
        if stagingServer:
            self.live_server_url = "http://"+stagingServer

    def tearDown( self ) :
        self.browser.quit()

    def checkForRowTextInTable( self, rowText ) :
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn( rowText, [row.text for row in rows] )

    def sendTextToInputBox( self, sendText = None ) :
        inputbox = self.getItemInputBox()
        if sendText is not None :
            inputbox.send_keys(sendText)
        inputbox.send_keys(Keys.ENTER)

    def waitForRowInListTable( self, rowText ) :
        startTime = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn( rowText, [row.text for row in rows] )
                return
            except( AssertionError, WebDriverException ) as e :
                currentTime = time.time()
                if currentTime - startTime > MAX_WAIT_TIME :
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT_TIME:
                    raise e
                time.sleep(0.5)


    def restartBrowser( self, url = None ) :
        self.browser.quit()
        self.browser = webdriver.Firefox()
        if url == None :
            url = self.live_server_url
        self.browser.get( url )

    def getItemInputBox( self ) :
        return self.browser.find_element_by_id('id_text')


