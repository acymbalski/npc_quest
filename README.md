# NPC Quest Remake

## Compiling to binary

At the moment, you will need to have Python 3.11 installed for nuitka to successfully compile
Using `nuitka`, you can compile using:

```
nuitka --standalone --plugin-enable=numpy --plugin-enable=pylint-warnings main.py -o NPCQuestR.exe --output-dir=package --windows-icon-from-ico=graphics/fatbird.png --include-data-dir=./graphics=./graphics --include-data-dir=./sound=./sound --include-data-dir=./font=./font --disable-console
```

It will take awhile.
