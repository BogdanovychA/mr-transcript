# Mr. Transcript

[![DOI](https://zenodo.org/badge/1212408609.svg)](https://doi.org/10.5281/zenodo.19630758) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/mr-transcript?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/mr-transcript) ![PyPI - License](https://img.shields.io/pypi/l/mr-transcript?logoColor=grey&color=blue) ![PyPI - Version](https://img.shields.io/pypi/v/mr-transcript?logoColor=grey&color=blue)

Зручна обгортка над бібліотекою `youtube-transcript-api` для швидкого та надійного отримання розшифровок (субтитрів) з відео на YouTube.

## Основні можливості

*   **Автоматична обробка URL:** Підтримка посилань форматів `youtube.com`, `youtu.be`, `shorts` та `embed`.
*   **Інтелектуальний пошук:** Пакет спочатку шукає субтитри, створені автором вручну, а якщо їх немає — автоматично перемикається на згенеровані YouTube.
*   **Таймкоди:** Опція додавання позначок часу до кожного блоку тексту.
*   **Список мов:** Швидке отримання словника доступних мов для конкретного відео.
*   **Типізація:** Повна підтримка анотацій типів для розробки.

## Встановлення

Встановіть пакет за допомогою `pip`:

```bash
pip install mr-transcript
```

Або за допомогою `uv`:

```bash
uv add mr-transcript
```

## Швидкий старт

```python
from mr_transcript import get_transcript, get_languages

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 1. Перевірка доступних мов
languages = get_languages(url)
print(f"Доступні мови: {languages}")

# 2. Отримання тексту субтитрів (наприклад, англійською)
if "en" in languages:
    text = get_transcript(url, language="en", timecodes=True)
    print(text[:500])  # Виведе перші 500 символів
```

## Скіл для ШІ-агентів

Цей репозиторій містить спеціалізований скіл (skill) для ШІ-агентів (наприклад, Gemini CLI). Він допомагає агенту надавати експертну допомогу у написанні Python-коду, парсингу URL та інтеграції цієї бібліотеки у ваші проєкти.

Щоб встановити скіл, виконайте:
```bash
npx skills add BogdanovychA/mr-transcript --skill "mr-transcript"
```

## Опис функцій

### `get_transcript(video_id, language, timecodes=False)`
Отримує повний текст субтитрів.
*   `video_id`: ID відео або повне посилання.
*   `language`: Код мови (наприклад, 'uk', 'en').
*   `timecodes`: Якщо `True`, додає час початку до кожного рядка.

### `get_languages(video_id)`
Повертає словник усіх доступних мов для відео.
*   Формат: `{"код_мови": "назва_мови"}` (наприклад, `{"uk": "Ukrainian"}`).

## Вимоги

*   Python >= 3.10
*   [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) >= 1.2.4

## Ліцензія

Проєкт поширюється під ліцензією MIT.
