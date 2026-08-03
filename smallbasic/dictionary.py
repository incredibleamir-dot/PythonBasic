# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Dictionary object - online word definitions and translations.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import urllib.request
import urllib.parse
import json


class Dictionary:
    """
    Provides access to an online dictionary and translation service.
    Uses free APIs for definitions and translations.
    
    Usage:
        definition = Dictionary.GetDefinition("hello")
        print(definition)
        
        translation = Dictionary.GetDefinitionEnglishToSpanish("hello")
        print(translation)
    """

    _BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
    _TRANSLATE_URL = "https://api.mymemory.translated.net/get"

    @classmethod
    def _fetch_definition(cls, word: str) -> str:
        """Fetch definition from the free dictionary API."""
        try:
            url = f"{cls._BASE_URL}/{urllib.parse.quote(word)}"
            req = urllib.request.Request(url, headers={"User-Agent": "SmallBasicPython/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode("utf-8")
                entries = json.loads(data)
                if entries and len(entries) > 0:
                    meanings = entries[0].get("meanings", [])
                    if meanings:
                        defs = meanings[0].get("definitions", [])
                        if defs:
                            return defs[0].get("definition", "No definition found.")
            return "No definition found."
        except Exception as e:
            return f"Could not retrieve definition: {e}"

    @classmethod
    def _translate(cls, word: str, source: str, target: str) -> str:
        """Translate a word using the MyMemory translation API."""
        try:
            lang_pair = f"{source}|{target}"
            params = urllib.parse.urlencode({
                "q": word,
                "langpair": lang_pair
            })
            url = f"{cls._TRANSLATE_URL}?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "SmallBasicPython/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                if data.get("responseStatus") == 200:
                    translated = data.get("responseData", {}).get("translatedText", "")
                    if translated and translated.lower() != word.lower():
                        return translated
            return f"Translation not available for '{word}'"
        except Exception as e:
            return f"Could not retrieve translation: {e}"

    @classmethod
    def GetDefinition(cls, word: str) -> str:
        """
        Gets the English definition of the specified word.
        
        Args:
            word: The word to look up.
            
        Returns:
            The definition of the word.
        """
        return cls._fetch_definition(word)

    @classmethod
    def GetDefinitionEnglishToEnglish(cls, word: str) -> str:
        """
        Gets the English definition of the specified word.
        
        Args:
            word: The word to look up.
            
        Returns:
            The English definition.
        """
        return cls._fetch_definition(word)

    @classmethod
    def GetDefinitionEnglishToGerman(cls, word: str) -> str:
        """Gets the German translation of the specified word."""
        return cls._translate(word, "en", "de")

    @classmethod
    def GetDefinitionEnglishToFrench(cls, word: str) -> str:
        """Gets the French translation of the specified word."""
        return cls._translate(word, "en", "fr")

    @classmethod
    def GetDefinitionEnglishToSpanish(cls, word: str) -> str:
        """Gets the Spanish translation of the specified word."""
        return cls._translate(word, "en", "es")

    @classmethod
    def GetDefinitionEnglishToItalian(cls, word: str) -> str:
        """Gets the Italian translation of the specified word."""
        return cls._translate(word, "en", "it")

    @classmethod
    def GetDefinitionEnglishToJapanese(cls, word: str) -> str:
        """Gets the Japanese translation of the specified word."""
        return cls._translate(word, "en", "ja")

    @classmethod
    def GetDefinitionEnglishToKorean(cls, word: str) -> str:
        """Gets the Korean translation of the specified word."""
        return cls._translate(word, "en", "ko")

    @classmethod
    def GetDefinitionEnglishToSimplifiedChinese(cls, word: str) -> str:
        """Gets the Simplified Chinese translation."""
        return cls._translate(word, "en", "zh-CN")

    @classmethod
    def GetDefinitionEnglishToTraditionalChinese(cls, word: str) -> str:
        """Gets the Traditional Chinese translation."""
        return cls._translate(word, "en", "zh-TW")
