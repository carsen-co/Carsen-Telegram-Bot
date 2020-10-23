from utils import load_makes

# general settings
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

MATCH_RATIO = 0.6

_MAKES_JSON = "makes.json"
_MDE_MAKES_DICT = load_makes("mobile_de")

BASE_URL = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"
PRICE_KEYS = ["Gross"]
REG_KEYS = ["New vehicle", "New car", "Pre-Registration"]
