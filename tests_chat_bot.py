'''
    This file tests all methods in app.py.
'''

import unittest
import app
import unittest.mock as mock
from app import bot_response_api
import json  

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_FIRST_WORD = "first_word"
KEY_SECOND_WORD = "second_word"


class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data


class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "Type either: \n1)!! translate/funtranslate {text}\n2)!! tamil-translate {text}\n3)!! random-fact\n4)!! text-to-binary {text}\n5)!! help\n6)!! about"
            },
            {
                KEY_INPUT: "!! about me",
                KEY_EXPECTED: "I am a bot, I will respond to messages that start with !!"
            },
            {
                KEY_INPUT: "!! tamil-translate coconut",
                KEY_EXPECTED: "தேங்காய்"
            },
            {
                KEY_INPUT: "! tamil-translate coconut",
                KEY_EXPECTED: "Command not found"
            },
        ]
        self.success_test_funtranslate = [
            {
                KEY_INPUT: "!! funtranslate Master Obiwan has lost a planet.",
                KEY_EXPECTED: "Lost a planet,  master obiwan has."
            },
             
        ]
        self.failure_test_funtranslate = [
            {
                KEY_INPUT: "!! funtranslate Master Obiwan has lost a planet.",
                KEY_EXPECTED: "Error: Translate limit hit: try in an hour" 
            },
             
        ]
        self.failure_test_params = [
            {
                KEY_INPUT: "!! tamil-translate coconuts",
                KEY_EXPECTED: "my name is"
            },
             
        ]
        self.error_tamil_translate_test_params = [
            {
                KEY_INPUT: "!! tamil-translate",
                KEY_EXPECTED: "Error: text not given" 
            },
        ]
        self.error_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate",
                KEY_EXPECTED: "Error: text not given" 
            },
            ]
            
        self.success_test_text_to_binary = [
            {
                KEY_INPUT: "!! text-to-binary hello",
                KEY_EXPECTED: "0110100001100101011011000110110001101111" 
            },
            ] 
         
        self.failure_test_text_to_binary = [
            {
                KEY_INPUT: "!! text-to-binary",
                KEY_EXPECTED: "Error: text not given" },
            ]  
            
        self.success_random_fact= [
            {
                KEY_INPUT: "!! random-fact",
                KEY_EXPECTED: "In a test performed by Canadian scientists, using various different styles of music, it was determined that chickens lay the most eggs when pop music was played." },
            ]      
       
            
    #UNMOCKED TESTS
    def test_parse_message_success(self):
        for test in self.success_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_parse_message_failure(self):
        for test in self.failure_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)
            
    def test_parse_message_error_tamil_translate(self):
        for test in self.error_tamil_translate_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_parse_message_error_funtranslate(self):
        for test in self.error_funtranslate_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_text_to_binary_failure(self):
        for test_case in self.failure_test_text_to_binary:
            text_to_binary = bot_response_api(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(text_to_binary, expected)  
    
    #MOCKED TESTS
    def mocked_funtranslate_success(self,link, params):
        if link == "https://api.funtranslations.com/translate/yoda.json":
            dicts = {"contents": {"translated": "Lost a planet,  master obiwan has."}}
            return MockResponse(dicts, 200)
        
    def mocked_funtranslate_failure(self,link, params):
        dicts = {"error": {"translated": "Lost a planet,  master obiwan has."}}
        return MockResponse(dicts, 200)
    
    def mocked_text_to_binary_success(self,link, params):
        dicts = {'binary': '0110100001100101011011000110110001101111'}
        return MockResponse(dicts, 200) 
        
    def mocked_random_fact_success(self,link):
        dicts = {'text': 'In a test performed by Canadian scientists, using various different styles of music, it was determined that chickens lay the most eggs when pop music was played.'}
        return MockResponse(dicts, 200)  
          
        
    #-----------------------------------------------------------------    
    def test_funtranslate_success(self):
        for test_case in self.success_test_funtranslate:
            with mock.patch('requests.get', self.mocked_funtranslate_success):
                funtranslate = bot_response_api(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]
            self.assertEqual(funtranslate, expected)
            
    
           
if __name__ == '__main__':
    unittest.main()
