from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

class ProEmailField(forms.EmailField):
    
    '''
    subclasses forms.EmailField, which validates against empty values, and that it is a correct email.
    then validate_pro will check whether not part of the excluded domains.
    I used an extra method as opposed to a custom validator because it seems to be difficult to know which validator is run first
    and we do want the default email validator to run first because otherwise there is a chance that the regexp will fail and crash the site.
    '''
    
    def __init__(self, excludedDomain, **kwargs):
        self.exclude = excludedDomain
        super(ProEmailField, self).__init__(self,**kwargs)

    def validate_pro(self, value):
        domain = re.search(r'@(\w+)', value)
        if domain.group(1) in self.exclude:
            raise ValidationError('it seems you have provided a %s address, please give us your professional email adress' % (domain.group(1)))
        
    def clean(self, value):
        #please note the extra validate_pro method
        value = super(ProEmailField, self).clean(value)
        self.validate_pro(value)
        return value

class RegexpExtractField(forms.CharField):
    '''
    Useful to extract a specific part of a user supplied chunk of text, if you know what you are looking for but not sure what else will be supplied along with us.
    Initialize with:
    1. one raw string regular expression pattern containing at least one match group,
    2. a list of all groups within the regexp, and
    3. one error message string.
    
    The field matches the imput value against the regexp, and returns a list containing the subgroups for use within the form's cleaned_data
    
    example:
    
    A user can create his own slideshare presentation widget by copy pasting the full widget html code found on the slideshare.net page.
    All that the application needs is the variable id of the presentation, therefore we will only extract that. The actual chunk of html will vary and we will ignore it.
    
    RegexpExtractField(
        r'.+slideshare.net/slideshow/embed_code/(?P<id>\d+).+title="(?P<title>[^"]+)"',
        ['id', 'title'],
        'there is something wrong with the SlideShares Embed code you pasted, please try again',
        help_text="Paste the embed code from slideshare.net",
        label="Html code",
        widget=forms.Textarea(attrs={'style': "width: 800px; height: 125px;"}))
        
    '''
    def __init__(self, regexp, groups, errormessage, **kwargs):
        self.regexp = re.compile(regexp)
        self.groups = groups
        self.errormessage = errormessage
        super(HtmlExtractField, self).__init__(self,**kwargs)

    def validate(self, value):
        if not self.regexp.match(value):
            raise forms.ValidationError(self.errormessage)    

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        matched = []
        for group in self.groups:
            match = self.regexp.match(value).group(group)
            matched.append(match)
        return matched
    
        
class UserEmailField(forms.EmailField):
    '''
    This field subclasses EmailField, so we get the validation that no blanks are supplied and that an actual email address was supplied
    This custom field adds validation for the existence of a registered user with this email. 
    '''
    def to_python(self, value):
        #call the super to_python, which returns a unicode object, trim any whitespace left between emails by the user, then create a list of emails
        value = super(UserEmailField, self).to_python(value).strip().replace(' ', '').split(',')
        #remove any 'empty' email, which would be caused by the user leaving a trailing comma
        value = [email for email in value if email != u'']
        return value
    
    def find_user(self, value):
        errorlist = []
        for email in value:
            #value is list returned by to_python
            #if we don't find a user for an email, add it to the list of errors
            try:
                User.objects.get(email=email)
            except:
                errorlist.append(email)
        if errorlist:
            #raise a field error
            raise forms.ValidationError(u"we haven't found a user for the following email(s): '%s'" % ( ', '.join(errorlist)))

    def clean(self, value):
        #run all the default validation, then call find_user
        value = self.to_python(value)
        for email in value:
            #check that each email in the list is a real email
            self.run_validators(email)
        #validate checks that something was imput, or raises 'field is required'    
        self.validate(value)
        #find_user checks that each email supplied belongs to a registered user
        self.find_user(value)
        return value
    

