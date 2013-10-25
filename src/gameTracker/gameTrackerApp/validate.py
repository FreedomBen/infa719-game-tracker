# provides functions views can use to validate data

import re

from django.forms import EmailField
from django.core.exceptions import ValidationError


# validate name and return empty string if passes
# or a string describing the error if it doesn't
def validateName( name ):
    # Ensure not empty string
    if not name:
        return "Name cannot be empty"
    # Ensure does not contain digits
    if re.compile( '\d' ).search( name ):
        return "Name cannot contain digits"

    return ""

# validate email and return empty string if passes
# or a string describing the error if it doesn't
def validateEmail( email ):
    try:
        EmailField().clean( email )
        return ""
    except ValidationError:
        return "Email was invalid."

# validate password and return empty string if passes
# or a string describing the error if it doesn't
# Password requirements are:
#     1. At least 15 characters
#     2. At least one number
#     3. At least one upper case letter
#     4. At least one lower case letter
# This will make rainbow table attacks unfeasible and makes it harder (though not impossible) for the user to use a dictionary word 
def validatePassword( password ):
    # Make sure password is at least 15 characters
    # This makes a rainbow table attack against the password hashes unfeasible
    if len( password ) < 12:
        return "Password must be at least 12 characters"
    if not re.compile( '\d' ).search( password ):
        return "Password must contain at least one number"
    if not re.compile( '[a-z]' ).search( password ):
        return "Password must contain at least one lower case letter"
    if not re.compile( '[A-Z]' ).search( password ):
        return "Password must contain at least one upper case letter"
    return ""

# validate twitter and return empty string if passes
# or a string describing the error if it doesn't
def validateTwitter( twitter ):
    pass
