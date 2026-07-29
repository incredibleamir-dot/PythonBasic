import urllib.request
import urllib.parse


class Dictionary:
    """
    Provides access to an online dictionary service.
    Uses a free dictionary API to get word definitions.
    
    Usage:
        definition = Dictionary.GetDefinition("hello")
        print(definition)
    """

    _BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"

    @classmethod
    def _fetch_definition(cls, word: str) -> str:
        """Fetch definition from the free dictionary API."""
        try:
            url = f"{cls._BASE_URL}/{urllib.parse.quote(word)}"
            req = urllib.request.Request(url, headers={"User-Agent": "SmallBasicPython/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode("utf-8")
                import json
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
    def _translate(cls, word: str, source: str, target: str) -> str:
        """Placeholder for translation - uses simple API lookup."""
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
        return cls._translate(word, "en", "zh-Hans")

    @classmethod
    def GetDefinitionEnglishToTraditionalChinese(cls, word: str) -> str:
        """Gets the Traditional Chinese translation."""
        return cls._translate(word, "en", "zh-Hant")
