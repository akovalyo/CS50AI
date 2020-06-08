# Project 6b: Questions

Write an AI to answer questions.

### Specification

The goal of this project is to create a simple question answering system based on inverse document frequency.

AI will perform two tasks: document retrieval and passage retrieval. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

### Requriements:

```python
nltk
```

### Usage

```
python questions.py FOLDER
```

FOLDER - path to the folder with documents

*Video on youtube showing result*

[![Parser - youtube](https://img.youtube.com/vi/CYSXPbviW74/0.jpg)](https://youtu.be/CYSXPbviW74)

