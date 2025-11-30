"""
Advanced OSINT Resources Module
Comprehensive list of OSINT tools and databases
"""

from typing import Dict, List


class OSINTResources:
    """Collection of OSINT resources organized by category"""
    
    # US People Search
    US_PEOPLE_SEARCH = [
        {'name': '10digits.us', 'url': 'http://10digits.us', 'type': 'phone'},
        {'name': 'WhitePages', 'url': 'http://www.whitepages.com', 'type': 'general'},
        {'name': '411.com', 'url': 'http://www.411.com', 'type': 'general'},
        {'name': 'ZabaSearch', 'url': 'http://www.zabasearch.com', 'type': 'general'},
        {'name': 'Intelius', 'url': 'http://www.intelius.com', 'type': 'premium'},
        {'name': 'YellowPages', 'url': 'http://www.yellowpages.com', 'type': 'business'},
        {'name': 'Public Records Directory', 'url': 'http://publicrecords.directory/', 'type': 'records'},
        {'name': '411locate', 'url': 'http://www.411locate.com', 'type': 'general'},
        {'name': 'Addresses.com', 'url': 'http://www.addresses.com', 'type': 'address'},
        {'name': 'Spokeo', 'url': 'http://www.spokeo.com', 'type': 'premium'},
        {'name': 'AnyWho', 'url': 'http://www.anywho.com', 'type': 'general'},
        {'name': 'PeopleFinders', 'url': 'http://www.peoplefinders.com', 'type': 'premium'},
        {'name': 'SkipEase', 'url': 'http://www.skipease.com', 'type': 'general'},
        {'name': 'VetFriends', 'url': 'https://www.vetfriends.com/', 'type': 'veterans'},
        {'name': 'Radaris', 'url': 'http://radaris.com', 'type': 'general'},
        {'name': 'SuperPages', 'url': 'http://www.superpages.com', 'type': 'business'},
        {'name': 'Advanced Background Checks', 'url': 'http://www.advancedbackgroundchecks.com/', 'type': 'premium'},
        {'name': 'Nuwber', 'url': 'https://nuwber.com/', 'type': 'general'},
        {'name': 'PeopleSmart', 'url': 'https://www.peoplesmart.com/', 'type': 'premium'},
        {'name': 'PeekYou', 'url': 'http://www.peekyou.com/', 'type': 'social'},
        {'name': 'iPeople', 'url': 'http://www.ipeople.com', 'type': 'general'},
        {'name': 'Yasni', 'url': 'http://www.yasni.com', 'type': 'social'},
        {'name': 'DOBSearch', 'url': 'https://www.dobsearch.com', 'type': 'birthdate'},
        {'name': 'BirthDatabase', 'url': 'http://www.birthdatabase.com', 'type': 'birthdate'},
    ]
    
    # International People Search
    INTERNATIONAL_SEARCH = [
        {'name': 'Phonebook of the World', 'url': 'https://phonebookoftheworld.com/', 'region': 'global'},
        {'name': 'Europe Telephones', 'url': 'https://europetelephones.com/white_pages', 'region': 'europe'},
        {'name': '192.com', 'url': 'http://www.192.com', 'region': 'uk'},
        {'name': 'WebMii', 'url': 'http://webmii.com', 'region': 'uk'},
        {'name': 'KGB People', 'url': 'http://www.kgbpeople.com', 'region': 'uk'},
        {'name': 'British Phonebook', 'url': 'http://britishphonebook.com/', 'region': 'uk'},
        {'name': 'UK Electoral Roll', 'url': 'https://www.gov.uk/electoral-register/overview', 'region': 'uk'},
        {'name': 'Canada411', 'url': 'http://www.canada411.ca', 'region': 'canada'},
        {'name': 'Infobel', 'url': 'http://www.infobel.com/en/world', 'region': 'global'},
        {'name': '118.dk', 'url': 'http://118.dk', 'region': 'denmark'},
    ]
    
    # Phone Lookup Services
    PHONE_LOOKUP = [
        {'name': 'SpyDialer', 'url': 'http://www.spydialer.com/', 'type': 'reverse'},
        {'name': 'PhoneValidator', 'url': 'http://www.phonevalidator.com', 'type': 'validation'},
        {'name': 'FoneFinder', 'url': 'http://www.fonefinder.net', 'type': 'reverse'},
        {'name': 'Infobel', 'url': 'http://www.infobel.com/en/world', 'type': 'international'},
        {'name': 'Spokeo Phone', 'url': 'http://www.spokeo.com/reverse-phone-lookup', 'type': 'premium'},
        {'name': 'Instant Checkmate', 'url': 'https://www.phone.instantcheckmate.com/', 'type': 'premium'},
        {'name': 'Free Cell Directory', 'url': 'http://www.freecellphonedirectorylookup.com', 'type': 'cell'},
        {'name': 'NumberWay', 'url': 'http://www.numberway.com/', 'type': 'reverse'},
        {'name': 'Number Data', 'url': 'https://www.number-data.org', 'type': 'data'},
        {'name': 'ThisPhoneNumber', 'url': 'http://this-phone-number.com', 'type': 'lookup'},
    ]
    
    # Username Search
    USERNAME_SEARCH = [
        {'name': 'Google Advanced', 'url': 'https://www.google.com/advanced_search', 'type': 'search'},
        {'name': 'Pipl', 'url': 'https://pipl.com', 'type': 'people'},
        {'name': 'CheckUsernames', 'url': 'http://checkusernames.com', 'type': 'availability'},
        {'name': 'KnowEm', 'url': 'http://knowem.com', 'type': 'social'},
    ]
    
    # Image/Picture Search
    IMAGE_SEARCH = [
        {'name': 'TinEye', 'url': 'http://www.tineye.com', 'type': 'reverse'},
        {'name': 'Google Images', 'url': 'https://images.google.com/', 'type': 'reverse'},
        {'name': 'EXIF Data', 'url': 'http://exifdata.com/', 'type': 'metadata'},
        {'name': 'GeoImgr', 'url': 'http://geoimgr.com/', 'type': 'geolocation'},
    ]
    
    # Email Search
    EMAIL_SEARCH = [
        {'name': 'Lullar', 'url': 'http://com.lullar.com', 'type': 'search'},
        {'name': 'EmailFinder', 'url': 'http://www.emailfinder.com', 'type': 'search'},
        {'name': 'Spokeo Email', 'url': 'http://www.spokeo.com/email-search', 'type': 'premium'},
        {'name': 'Google Image Email', 'url': 'http://ctrlq.org/google/images/', 'type': 'social'},
        {'name': 'EmailChange', 'url': 'http://emailchange.com/', 'type': 'tracker'},
        {'name': 'Verify Email', 'url': 'http://verify-email.org/', 'type': 'validation'},
        {'name': 'Hunter.io', 'url': 'https://hunter.io/', 'type': 'business'},
    ]
    
    # Social Network Search
    SOCIAL_SEARCH = [
        {'name': 'Facebook Directory', 'url': 'http://www.facebook.com/directory/people/', 'platform': 'facebook'},
        {'name': 'Topsy', 'url': 'http://topsy.com/', 'platform': 'twitter'},
        {'name': 'Monitter', 'url': 'http://monitter.com/', 'platform': 'twitter'},
        {'name': 'Twitter Details', 'url': 'http://www.twitteraccountsdetails.com', 'platform': 'twitter'},
        {'name': 'Social Mention', 'url': 'http://socialmention.com/', 'platform': 'multi'},
        {'name': 'KnowEm', 'url': 'http://knowem.com/', 'platform': 'multi'},
        {'name': 'Twoogel', 'url': 'http://twoogel.com/', 'platform': 'twitter'},
        {'name': 'YackTrack', 'url': 'http://www.yacktrack.com', 'platform': 'multi'},
        {'name': 'SamePoint', 'url': 'http://www.samepoint.com/', 'platform': 'multi'},
        {'name': 'WhosTalkin', 'url': 'http://www.whostalkin.com/', 'platform': 'multi'},
    ]
    
    # Breach/Password Databases
    BREACH_DATABASES = [
        {'name': 'Have I Been Pwned', 'url': 'https://haveibeenpwned.com/', 'type': 'breach'},
        {'name': 'Hacked-DB', 'url': 'https://www.hacked-db.com/', 'type': 'breach'},
        {'name': 'HashKiller', 'url': 'http://www.hashkiller.co.uk/md5-decrypter.aspx', 'type': 'hash'},
        {'name': 'Hacked Emails', 'url': 'https://hacked-emails.com', 'type': 'breach'},
        {'name': 'Breach Alarm', 'url': 'https://breachalarm.com/', 'type': 'monitoring'},
        {'name': 'LastPass Adobe', 'url': 'https://lastpass.com/adobe/', 'type': 'adobe-breach'},
        {'name': 'SkidBase', 'url': 'https://skidbase.io/', 'type': 'premium'},
    ]
    
    # IP Address Tools
    IP_TOOLS = [
        {'name': 'IP Location', 'url': 'https://www.iplocation.net/', 'type': 'geolocation'},
        {'name': 'WhatIsMyIP', 'url': 'http://whatismyipaddress.com/geolocation-accuracy', 'type': 'geolocation'},
        {'name': 'ProxyOrNot', 'url': 'http://www.proxyornot.com', 'type': 'proxy-detect'},
        {'name': 'InfoSniper', 'url': 'http://www.infosniper.net', 'type': 'lookup'},
        {'name': 'WHOIS.net', 'url': 'https://www.whois.net', 'type': 'whois'},
        {'name': 'IP Tracker', 'url': 'http://www.ip-tracker.org', 'type': 'tracking'},
        {'name': 'SkypeGrab', 'url': 'http://skypegrab.net', 'type': 'skype'},
        {'name': 'IP Host Info', 'url': 'http://iphostinfo.com/cloudflare/', 'type': 'cloudflare'},
        {'name': 'WhatsTheirIP', 'url': 'http://whatstheirip.com', 'type': 'grabber'},
        {'name': 'Skype Resolver', 'url': 'http://resolver.in/resolve', 'type': 'skype'},
        {'name': 'ResolveThem', 'url': 'http://resolvethem.com/', 'type': 'skype'},
        {'name': 'Hanz Resolver', 'url': 'https://www.hanzresolver.com/', 'type': 'skype'},
        {'name': 'IPAddress.com', 'url': 'http://ipaddress.com/', 'type': 'lookup'},
        {'name': 'SpeedGuide', 'url': 'http://www.speedguide.net/ip/', 'type': 'lookup'},
        {'name': 'DB-IP', 'url': 'http://db-ip.com/', 'type': 'geolocation'},
        {'name': 'IPGeek', 'url': 'http://www.ipgeek.org/', 'type': 'lookup'},
    ]
    
    # Criminal/Public Records
    CRIMINAL_RECORDS = [
        {'name': 'Criminal Searches', 'url': 'http://www.criminalsearches.com', 'type': 'criminal'},
        {'name': 'USA Trace', 'url': 'http://www.usatrace.com', 'type': 'general'},
        {'name': 'Abika', 'url': 'http://www.abika.com', 'type': 'public'},
        {'name': 'Public Records Online', 'url': 'http://publicrecords.onlinesearches.com', 'type': 'public'},
        {'name': 'JailBase', 'url': 'http://www.jailbase.com/', 'type': 'arrests'},
        {'name': 'AAD Archives', 'url': 'http://aad.archives.gov/aad/series-list.jsp?cat=GS29', 'type': 'archives'},
        {'name': 'Archive.org', 'url': 'http://www.archive.org/web/web.php', 'type': 'web-archive'},
    ]
    
    # OSINT Frameworks
    OSINT_FRAMEWORKS = [
        {'name': 'OSINT Framework', 'url': 'https://osintframework.com/', 'type': 'framework'},
        {'name': 'Soople', 'url': 'http://www.soople.com', 'type': 'search'},
        {'name': 'Keotag', 'url': 'http://www.keotag.com/', 'type': 'search'},
        {'name': 'FinderMind', 'url': 'http://www.findermind.com/free-people-search-engines/', 'type': 'directory'},
        {'name': 'iSearch', 'url': 'http://www.isearch.com/', 'type': 'search'},
    ]
    
    @classmethod
    def get_all_resources(cls) -> Dict[str, List[Dict]]:
        """Get all OSINT resources organized by category"""
        return {
            'us_people_search': cls.US_PEOPLE_SEARCH,
            'international_search': cls.INTERNATIONAL_SEARCH,
            'phone_lookup': cls.PHONE_LOOKUP,
            'username_search': cls.USERNAME_SEARCH,
            'image_search': cls.IMAGE_SEARCH,
            'email_search': cls.EMAIL_SEARCH,
            'social_search': cls.SOCIAL_SEARCH,
            'breach_databases': cls.BREACH_DATABASES,
            'ip_tools': cls.IP_TOOLS,
            'criminal_records': cls.CRIMINAL_RECORDS,
            'osint_frameworks': cls.OSINT_FRAMEWORKS,
        }
    
    @classmethod
    def search_by_type(cls, search_type: str) -> List[Dict]:
        """Get resources by specific type"""
        all_resources = cls.get_all_resources()
        return all_resources.get(search_type, [])
    
    @classmethod
    def get_resource_count(cls) -> int:
        """Get total count of all resources"""
        all_resources = cls.get_all_resources()
        return sum(len(resources) for resources in all_resources.values())
