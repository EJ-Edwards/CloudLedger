# Project 1: Build a CLI App

Build a command-line application of your own design, using the Python
fundamentals from Mod 1.

- [What You Are Building](#what-you-are-building)
- [AI Use on This Project](#ai-use-on-this-project)
- [Setup](#setup)
- [Requirements](#requirements)
- [Ideas](#ideas)
- [Submitting](#submitting)

## What You Are Building

A CLI app is a program you run in the terminal that talks to the user through
printed text and typed answers. It shows a menu, the user picks an option, the
app does something, and the menu comes back until they choose to quit.

The example we looked at in class was a task manager: add a task, mark one
complete, delete them all, quit. You can read that one in full in the
[Task Manager Case Study](https://github.com/The-Marcy-Lab-School/swe-casestudy-1-cli-task-manager),
and its investigation questions are worth working through first.

Yours does not have to be a task manager. It has to be yours.

## AI Use on This Project

Use whichever mode matches where you are with this material. Both are fine,
and most people move between them as a concept clicks.

**Tutor mode.** The AI explains, questions, quizzes, and critiques, and you
write every line you submit. For this project that means asking it how a
`while` loop keeps a menu running, or why your loop never exits. Ask it a
hundred questions — that is the whole point. What you do not do is ask it for
the feature. Paste this at the start of a chat and it will hold for the rest
of the conversation:

> You are acting as a tutor. Your job is to explain what this coding question
> is asking, clarify confusing wording, and highlight the relevant concepts I
> need to know — but do not provide the full solution or code that directly
> answers the question. Instead, rephrase the problem in simpler terms,
> identify what is being tested, and suggest what steps or thought processes
> might help. Ask me guiding questions to make sure I am thinking critically.
> Do not write the final function, algorithm, or code implementation.

**Implementer mode.** You write a specification first, the AI writes code from
it, and then you verify that code line by line. For this project your spec has
to list every menu option, what each one does to your data, and what the user
sees afterward. If what comes back does more than you asked for, reject it —
over-delivery is a defect, and catching it is part of the job.

You own every line either way, and you will be asked to explain it.

## Setup

Work in `development/mod-1`. Make a draft branch before you start.

```sh
git checkout -b draft
python3 src/main.py
```

There is nothing to install. Python reads a line of typed input with the
built-in `input()` function, so this project has no dependencies.

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

`input()` always gives you a **string**. Convert it with `int()` when you need
a number. Then think about what happens if the user types something that is
not a number.

## Requirements

Your app must:

- [ ] Show a menu of at least **four** options, one of which exits
- [ ] Keep showing the menu until the user chooses to exit
- [ ] Store its data in a **list of dictionaries**
- [ ] Let the user **add** an item
- [ ] Let the user **change or remove** an item
- [ ] Display the stored items in a readable way
- [ ] Split the work across **several functions**, each doing one job
- [ ] Handle a bad menu choice without crashing

Write your code in `src/`. Start in `src/main.py` and split into more files
when one file gets hard to read.

Then, two pieces of writing:

- [ ] **Replace `README.md`** with a description of *your* project: what it
      does, how to run it, and a usage example. Write it for someone who has
      never seen it. This is a real skill, and it is the first thing anyone
      looks at
- [ ] **Fill in `REFLECTIONS.md`**

## Ideas

Pick something you would actually use.

- A recipe box that stores ingredients and steps
- A workout log that tracks sets and reps
- A budget tracker that adds expenses and totals them by category
- A flashcard quiz that keeps score
- A reading list with a "finished" flag and a filter

## Submitting

```sh
git add -A
git commit -m "your message"
git push
```

Open a pull request to your instructor for feedback.
