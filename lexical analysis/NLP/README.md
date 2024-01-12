# NLP: extract workable feature from the text
I will discuss the feature we extract, and discuss the method we use in coding part.
## Working engine
The main engines we used in this project composed of three parts:
### Spacy

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/f56c78bb-9e63-444b-9a45-95e7361326f6)

A scientific engine built on Python has the advantages of easy-to-use function calls, an extensive support library based on it, and the speed of a natural language process, but it also has disadvantages in terms of lacking professional skills in parser trees or more advanced NLP skills.
## Extract features
### POS tagging 
POS, aka part of sentence, has the following tags: ADJ (adjective), ADP (adposition), ADV (adverb), AUX (auxilary), CONJ (conjunction), DET (determiner), INTJ (interjection), NOUN (noun), NUM (numerical), PART (particle), PRON (pronoun), PROPN (propernoun), PUNCT (punctuation), SCONJ (subordinating conjuction), SYM (symbol), VERB (verb), X (other), SPACE (space), we only exclude the SYM (symbol) tag from the Spacy POS tagging set. The POS tagging set is based on the Penn treebank developed by Penn University. Compared to the POS tagging set in Stanford NLP, there are slight differences, but we think the Spacy POS tagging set is good enough for analysis.
### lemma number

