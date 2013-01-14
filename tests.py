from django.utils import unittest
from django.test import TestCase
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

'''put the test.py and formfields.py in an application directory and run "python manage.py test <application name>" from your project's root directory'''

from formfields import ProEmailField, HtmlExtractField, UserEmailField

class ProEmailFieldTestCase(unittest.TestCase):
        
    def setUp(self):
        #pass along a list of excluded domains upon instantiation
        self.formfield = ProEmailField(['gmail', 'yahoo'])
        
    def tearDown(self):
        self.formfield = None
        
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean,'greg@gmail.com')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean('greg@corpemail.com'), u'greg@corpemail.com')

class HtmlExtractFieldTestCase(unittest.TestCase):
    
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

    def tearDown(self):
        self.formfield = None
    
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'www.slideshare.net/thereisnothinghere')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean(self.correct_input), ['15936422', 'How to create great slides for presentations'])

class UserEmailFieldTestCase(TestCase):
    
    def setUp(self):
        self.formfield = UserEmailField()
        self.user = User.objects.create_user(username='test', email='test@gmail.com')
        
    def tearDown(self):
        self.formfield = None
    
    def test_clean_fails(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'info@gmail.com')
    
    def test_clean_fails_no_email(self):
        self.assertRaises(ValidationError, self.formfield.clean, 'info@')
        
    def test_clean_passes(self):
        #if value validates, clean must return the value
        self.assertEqual(self.formfield.clean(self.user.email), [self.user.email])
        
    