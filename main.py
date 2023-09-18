#!/usr/bin/env python3
import os
import openai
import argparse
from goose3 import Goose
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access your variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


def main(sentence):
    openai.api_key = OPENAI_KEY

    g = Goose()
    article = g.extract(url=sentence)
    # print(article.cleaned_text)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Deine Antworten müssen deutsch sein. Verwende Bulletpoints wo es sinnvoll ist. Verwende Tabellen wo es sinnvoll ist. Markiere wichtige Textphrasen in kursiv. Gib weiterführende Links. Gib mir eine übersichtliche Zusammenfassung folgenden Textes als gut formatiertes Markdown Dokument.",
            },
            {"role": "user", "content": article.cleaned_text},
        ],
        temperature=1,
        max_tokens=548,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nehmen Sie einen Satz als Parameter entgegen."
    )
    parser.add_argument(
        "sentence", type=str, help="Ein Satz, der als Parameter übergeben wird."
    )

    args = parser.parse_args()
    main(args.sentence)
