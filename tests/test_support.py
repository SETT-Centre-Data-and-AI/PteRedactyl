import re

import pytest

from pteredactyl.regex_check_functions import is_nhs_number
from pteredactyl.regex_entities import REGEX_ENTITIES

nhs_numbers = {
  "999 000 0018": True,
  "999-000-0026": True,
  "999 000-0034": True,
  "999000 0042": True,
  "999-000 0050": True,
  "999 000 0069": True,
  "999-000-0077": True,
  "999 000-0085": True,
  "9990000093": True,
  "999-000-0107": True,
  "999 000 0000": False,
  "999-000-0140": False,
  "999 000-0280": False,
  "999-000 0310": False,
  "9990000450": False
}


uk_postcodes = {
    "B1A 1AA": True,
    "SW1A 1AA": True,
    "AAA 1AA": False,
    "E20 1EJ": True,
    "W1A 1AA": True,
    "ABCD 123": False,
    "EC1A 1BB": True,
    "W1": False,
    "B33 8TH": True,
    "N1A 1AA": True,
    "CR2 6XH": True,
    "DN55 1PT": True,
    "E10": False,
    "SW10 9RJ": True,
    "NW1E 2BU": True,
    "SE9 6RJ": True,
    "LS111AA": True,
}

email_addresses = {
    "valid.email@gmail.com": True,
    "user.name+tag+sorting@live.com": True,
    "user@sub.yahoo.com": True,
    "user.name@company.co.uk": True,
    "firstname.lastname@business.com": True,
    "user1234@gmail.com": True,
    "user@localhost": False,
    "user@website.web": True,
    "user@.com": False,
    "user@domain": False,
    "user@exam_ple.com": False,
}


def test_is_nhs_number():
    for nhs_number, expected_match in nhs_numbers.items():
        assert is_nhs_number(nhs_number) == expected_match


def test_is_uk_postcode():
    postcode_pattern = REGEX_ENTITIES["POSTCODE"][0]
    for postcode, expected_match in uk_postcodes.items():
        assert bool(re.search(postcode_pattern, postcode)) == expected_match


if __name__ == "__main__":
    pytest.main([__file__])
