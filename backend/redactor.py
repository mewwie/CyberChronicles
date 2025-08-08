import re
import spacy
from typing import List, Tuple

# --- Advies over Gevoelige Identificatienummers ---
# BSN (Burgerservicenummer) of SSN (Social Security Number) zijn extreem gevoelig.
# Eenvoudige regex-patronen hiervoor kunnen veel fout-positieven genereren.
# Voor productieomgevingen is het aan te raden om validatie met controletotalen (zoals de "elfproef" voor BSN)
# en context-bewuste detectieregels te gebruiken in plaats van brede regex-patronen.
# De verwerking van dergelijke gegevens dient onderworpen te zijn aan strikte beveiligings- en privacy-audits.

# --- Laden van het spaCy Model ---
NLP = None
try:
    # Het is efficiënter om het model eenmalig te laden wanneer de module wordt geïmporteerd.
    NLP = spacy.load("en_core_web_sm")
except OSError:
    print("Waarschuwing: spaCy-model 'en_core_web_sm' niet gevonden.")
    print("Voer 'python -m spacy download en_core_web_sm' uit om het te installeren.")
    print("NER-gebaseerde redactie wordt overgeslagen.")

REGEX_PATTERNS = {
    'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    # Using negative lookbehind to avoid issues with word boundaries and '+'
    'PHONE_E164': r'(?<!\w)\+?\d{10,15}\b',
    'IBAN_NL': r'\bNL\d{2}[A-Z]{4}\d{10}\b',
    'CREDIT_CARD': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b'
}

def redact_text(text: str, options: dict = None) -> str:
    """
    Redigeert persoonlijk identificeerbare informatie (PII) uit een tekst.

    Deze functie gebruikt zowel reguliere expressies als Named Entity Recognition (NER)
    om PII te vinden en te redigeren. Regex-matches krijgen prioriteit boven NER-matches.

    Args:
        text (str): De invoertekst die geredigeerd moet worden.
        options (dict, optional): Een woordenboek met redactie-opties.
            'mode' (str): 'replace' (standaard) of 'mask'.
            'mask_char' (str): Het karakter om te gebruiken bij maskeren (standaard 'X').
            'replacement' (str): De tekst om te gebruiken bij vervangen (standaard '[REDACTED]').

    Returns:
        str: De geredigeerde tekst.

    Voorbeelden van unit-tests in docstring:
    >>> test_text = "Neem contact op met Jan op jan@example.com of bel +31612345678. Zijn IBAN is NL20INGB0001234567."
    >>> redact_text(test_text)
    "Neem contact op met [REDACTED] op [REDACTED] of bel [REDACTED]. Zijn IBAN is [REDACTED]."

    >>> redact_text(test_text, options={'mode': 'mask'})
    "Neem contact op met XXX op XXXXXXXXXXXXXXX of bel XXXXXXXXXXXX. Zijn IBAN is XXXXXXXXXXXXXXXXXX."

    >>> redact_text("Geen PII hier.", options={'mode': 'mask', 'mask_char': '#'})
    'Geen PII hier.'
    """
    if options is None:
        options = {}

    # Standaardwaarden voor opties instellen
    config = {
        'mode': options.get('mode', 'replace'),
        'mask_char': options.get('mask_char', 'X'),
        'replacement': options.get('replacement', '[REDACTED]')
    }

    redactions: List[Tuple[int, int, str]] = []

    # Stap 1: Regex-pass
    for pii_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            replacement_text = config['replacement']
            if config['mode'] == 'mask':
                replacement_text = config['mask_char'] * len(match.group(0))
            redactions.append((start, end, replacement_text))

    # Stap 2: NER-pass (alleen als spaCy beschikbaar is)
    if NLP:
        doc = NLP(text)
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'GPE', 'LOC', 'ORG']:
                is_overlapping = False
                for r_start, r_end, _ in redactions:
                    if max(r_start, ent.start_char) < min(r_end, ent.end_char):
                        is_overlapping = True
                        break

                if not is_overlapping:
                    replacement_text = config['replacement']
                    if config['mode'] == 'mask':
                        replacement_text = config['mask_char'] * len(ent.text)
                    redactions.append((ent.start_char, ent.end_char, replacement_text))

    # Stap 3: Pas redacties toe
    if not redactions:
        return text

    # Sorteer redacties op startpositie om de juiste volgorde te garanderen
    redactions.sort(key=lambda item: item[0])

    result = []
    last_end = 0
    for start, end, replacement in redactions:
        # Voeg het stuk tekst toe sinds de laatste redactie
        result.append(text[last_end:start])
        # Voeg de vervangende tekst toe
        result.append(replacement)
        last_end = end

    # Voeg het laatste stuk van de tekst toe
    result.append(text[last_end:])

    return "".join(result)

if __name__ == '__main__':
    # Demo van de functionaliteit
    sample_text = (
        "De CEO, Jan Janssen, woont in Amsterdam en zijn e-mail is jan.janssen@example.nl. "
        "Zijn telefoonnummer is +31201234567. "
        "Betalingen kunnen worden overgemaakt naar NL30RABO0123456789. "
        "Gebruik geen creditcard zoals 5123456789012345. "
        "Het bedrijf, ExampleCorp, is gevestigd in Nederland."
    )

    print("--- Originele Tekst ---")
    print(sample_text)
    print("\n" + "="*30 + "\n")

    print("--- Modus: Standaard Vervangen ---")
    redacted_replace = redact_text(sample_text)
    print(redacted_replace)
    print("\n" + "="*30 + "\n")

    print("--- Modus: Maskeren met '#' ---")
    redacted_mask = redact_text(sample_text, options={'mode': 'mask', 'mask_char': '#'})
    print(redacted_mask)
    print("\n" + "="*30 + "\n")

    print("--- Docstring Tests Uitvoeren ---")
    import doctest
    doctest.testmod()
