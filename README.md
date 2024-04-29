# NPC Quest Remake

## Compiling to binary

At the moment, you will need to have Python 3.11 installed for nuitka to successfully compile
Using `nuitka`, you can compile for Windows using:

```
nuitka --standalone --plugin-enable=numpy --plugin-enable=pylint-warnings main.py -o NPCQuestR.exe --output-dir=package --windows-icon-from-ico=graphics/fatbird.png --include-data-dir=./graphics=./graphics --include-data-dir=./sound=./sound --include-data-dir=./font=./font --disable-console
```

It will take awhile.


## "Style" Guide

There are not many rules here. No linter will survive this repo. However, all files should have sorted imports and be formatted using Black formatter, if possible.

# Credits

This project is an adaptation of work done by Mike Hommel (Hamumu Software) and is released with their permission.

Concept, art, and sound effects are all credited to Mike Hommel.


> Source code is provided AS-IS, and you use it at your own risk. If it blows up your computer, that's your problem.

Thanks, Mike!

Conversion to Python by Andrew Cymbalski.

If you are going to do anything with this, please leave the credits intact and available. Thanks!

[Hamumu Games](https://hamumu.com/)

[NPC Quest (Original)](https://hamumu.itch.io/npc-quest)