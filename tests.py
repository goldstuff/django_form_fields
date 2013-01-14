from django.utils import unittest
from django.test import TestCase
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

'''
run as "$ python manage.py test formfields" from your project's root
after adding formfields to your INSTALLED_APPS
or just add formfields.py and tests.py to the same existing app folder

'''

from formfields import ProEmailField, HtmlExtractField, UserEmailField

class FormFieldTestCase(object):
    #base class, not part of unittest
    def tearDown(self):
        self.formfield = None
        
    def test_empty_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean, '')


class ProEmailFieldTestCase(unittest.TestCase, FormFieldTestCase):
        
    def setUp(self):
        #pass along a list of excluded domains upon instantiation
        self.formfield = ProEmailField(['gmail', 'yahoo'])
                
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean,'greg@gmail.com')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean('greg@corpemail.com'), u'greg@corpemail.com')


class HtmlExtractFieldTestCase(unittest.TestCase, FormFieldTestCase):
    
    def setUp(self):
        self.formfield = HtmlExtractField(
        r'.+slideshare.net/slideshow/embed_code/(?P<id>\d+).+title="(?P<title>[^"]+)"',
        ['id', 'title'],
        'there is something wrong with the SlideShares Embed code you pasted, please try again',
        help_text="Paste the embed code from slideshare.net",
        label="Html code",
        widget=forms.Textarea(attrs={'style': "width: 800px; height: 125px;"})
        )
        self.correct_input = '"http://www.slideshare.net/slideshow/embed_code/15936422" (.....) title="How to create great slides for presentations"'
    
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'www.slideshare.net/thereisnothinghere')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean(self.correct_input), ['15936422', 'How to create great slides for presentations'])


class UserEmailFieldTestCase(TestCase, FormFieldTestCase):
    
    def setUp(self):
        self.formfield = UserEmailField()
        self.user = User.objects.create_user(username='test', email='test@gmail.com')
            
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'info@gmail.com')
    
    def test_clean_fails_no_email(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'info@')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean(self.user.email), [self.user.email])
        
    