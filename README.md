A bunch of form fields for Django projects, you can add it as an app to your django project, includes tests...

ProEmailField:

    subclasses forms.EmailField, which validates against empty values, and that it is a correct email.
    then validate_pro will check whether not part of the excluded domains.
    I used an extra method as opposed to a custom validator because it seems to be difficult to know which validator is run first
    and we do want the default email validator to run first because otherwise there is a chance that the regexp will fail and crash the site.
    
    
RegexpExtractField:

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
        
UserEmailField:

    This field subclasses EmailField, so we get the validation that no blanks are supplied and that an actual email address was supplied
    This custom field adds validation for the existence of a registered user with this email. 
