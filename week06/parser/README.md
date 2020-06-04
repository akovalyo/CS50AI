# Project 6a: Parser

Write an AI to parse sentences and extract noun phrases.

![parser](https://github.com/akovalyo/CS50AI/blob/master/week06/parser/src/parser.png?raw=true)

### Background

A common task in natural language processing is parsing, the process of determining the structure of a sentence. This is useful for a number of reasons: knowing the structure of a sentence can help a computer to better understand the meaning of the sentence, and it can also help the computer extract information out of a sentence. In particular, it’s often useful to extract noun phrases out of a sentence to get an understanding for what the sentence is about.

### Specification

The goal of this project is to parse english sentences using the context-free grammar formalism, and determine their structure.

Parser also trying not to parse obviously incorrect sentences like *"Armchair on the sat Holmes."*

### Requriements:

```python
nltk
```

### Usage

```
python parser.py [FILE.txt]
```

FILE.txt - (optional) file with sentence.

*Video on youtube showing result*

[![Parser - youtube](https://img.youtube.com/vi/dnpnv_x1TFE/0.jpg)](https://youtu.be/dnpnv_x1TFE)