# Bibliotheca Buddhica

*Public-domain Buddhist studies texts, properly typeset as epub. [English below](#in-english).*

Тексты по буддизму и буддийской философии, вычитанные и нормально свёрстанные в epub.

Большинство классических работ по буддологии лежит в сети в виде набора HTML-страниц
с битой кодировкой, сносками, которые никуда не ведут, и вёрсткой из 1999 года. Читать
это на телефоне или ридере невозможно. Здесь то же самое, но собранное так, чтобы можно
было читать.

Название — по серии «Bibliotheca Buddhica», которую Академия наук начала издавать в
Петербурге в 1897 году под редакцией С. Ф. Ольденбурга; в ней печатались Ф. И. Щербатской,
Е. Е. Обермиллер и другие. Преемственности никакой, только уважение к предмету.

## Содержание

| Текст | Год | Язык | Статус |
|---|---|---|---|
| [О. О. Розенберг. Проблемы буддийской философии](texts/rozenberg-1918-problemy-buddiyskoy-filosofii/) | 1918 | ru | общественное достояние |

## Принципы

- **Только свободные тексты.** Общественное достояние либо разрешение правообладателя.
  Правовой статус указан в README каждого текста и в колофоне внутри файла.
- **Сноски должны работать.** Собственно, единственная причина, по которой всё это затевалось.
  Ссылка на примечание ведёт к примечанию, а не в пустоту.
- **Сборка воспроизводима.** У каждого текста лежит `build/build.py`: он скачивает источник,
  вычищает разметку и собирает epub. Никаких ручных правок в бинарнике.
- **Источник указывается всегда.** Тем, кто набирал текст, мы обязаны больше, чем принято
  признавать.

## Сборка

Нужны `pandoc` (3.x) и Python с Pillow.

```sh
cd texts/<название>/build
python3 build.py
```

Скрипт кэширует скачанные страницы в `build/cache/`, так что повторный запуск не бьёт
по чужому серверу.

## Благодарности

Электронные тексты взяты у тех, кто проделал главную работу по набору и вычитке, прежде
всего у библиотеки [PSYLIB](https://psylib.org.ua/) (Киев). Оцифровка не создаёт прав на
текст в общественном достоянии, но создаёт долг вежливости.

## Лицензии

- Тексты — общественное достояние, статус указан у каждого.
- Скрипты сборки — MIT, см. [LICENSE](LICENSE).
- Обложки — CC0, используйте как хотите.

---

## In English

Classic works of Buddhist studies, mostly in Russian, cleaned up and typeset as readable
epub files.

Much of this literature exists online only as a pile of HTML pages with broken encodings,
footnotes that link nowhere and layout from 1999. It is unreadable on a phone or an e-reader.
This repository holds the same texts, assembled so that they can actually be read.

The name refers to *Bibliotheca Buddhica*, the series the Imperial Academy of Sciences began
publishing in St. Petersburg in 1897 under S. F. Oldenburg, which printed F. I. Stcherbatsky,
E. E. Obermiller and others. No continuity is claimed, only respect for the subject.

### Contents

| Text | Year | Language | Status |
|---|---|---|---|
| [O. O. Rosenberg, *Problems of Buddhist Philosophy*](texts/rozenberg-1918-problemy-buddiyskoy-filosofii/) | 1918 | Russian | public domain |

### Principles

- **Free texts only.** Public domain, or with the rightsholder's permission. The legal
  status is stated in each text's README and in the colophon inside the file itself.
- **Footnotes must work.** That is the entire reason this exists: a reference to a note
  takes you to the note, not into the void.
- **Reproducible builds.** Every text ships a `build/build.py` that fetches the source,
  strips the markup and assembles the epub. Nothing is hand-patched inside the binary.
- **Sources are always credited.** Whoever typed and proofread the text did the harder part
  of the work.

### Building

Requires `pandoc` (3.x) and Python with Pillow.

```sh
cd texts/<name>/build
python3 build.py
```

Fetched pages are cached in `build/cache/`, so re-running does not hammer anyone's server.

### Licensing

- Texts: public domain; the specific basis is documented per text.
- Build scripts: MIT, see [LICENSE](LICENSE).
- Cover art: CC0, do as you like with it.

A note on jurisdiction: public-domain determinations here are made for Russia, the EU and
the United States, and are stated explicitly per text. If you are reading from somewhere
else, check your local term of protection.
