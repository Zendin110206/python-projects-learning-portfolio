# Project 07 - Mad Libs Generator

Status: In progress.

This project is a command-line Mad Libs generator. It is intended for practicing file reading, placeholder parsing, dictionaries, string replacement, and clean terminal prompts.

## Goal

Build a terminal program that:

- reads a story template from a text file,
- finds placeholders wrapped in angle brackets,
- asks the user to provide a word for each placeholder,
- replaces every placeholder with the user's answer,
- prints the completed story.

## Learning Focus

- reading text files,
- scanning strings character by character,
- collecting unique placeholders in a predictable order,
- using dictionaries to map placeholders to answers,
- replacing text with `.replace()`,
- keeping prompts and output easy to read.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/07_madlibs_generator/src/madlibs_generator.py
```

## Expected Terminal Interaction

The final prompt text will be finalized with the implementation. The intended shape is:

```text
Enter a word for <place>: library
Enter a word for <adjective>: bright
Enter a word for <noun>: robot
Enter a word for <verb>: dance

Here is your completed story:
Today I went to the library.
I saw a bright robot that loved to dance.
Everyone started to dance together, and it became a bright day.
```

## Completion Checklist

- The program can be run from the terminal.
- The story template is read from a text file.
- Placeholders are detected automatically.
- Each unique placeholder is requested once.
- User answers replace every matching placeholder.
- The completed story is printed clearly.
