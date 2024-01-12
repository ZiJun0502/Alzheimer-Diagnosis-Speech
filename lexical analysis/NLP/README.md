# NLP: extract workable feature from the text
I will discuss the feature we extract, and discuss the method we use in coding part.
## Working engine
The main engines we used in this project composed of three parts:
### Spacy

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/f56c78bb-9e63-444b-9a45-95e7361326f6)

A scientific engine built on Python has the advantages of easy-to-use function calls, an extensive support library based on it, and the speed of a natural language process, but it also has disadvantages in terms of lacking professional skills in parser trees or more advanced NLP skills.
## Extract features

### POS tagging 
POS, aka part of a sentence, has the following tags: ADJ (adjective), ADP (adposition), ADV (adverb), AUX (auxilary), CONJ (conjunction), DET (determiner), INTJ (interjection), NOUN (noun), NUM (numerical), PART (particle), PRON (pronoun), PROPN (propernoun), PUNCT (punctuation), SCONJ (subordinating conjuction), SYM (symbol), VERB (verb), X (other), SPACE (space), we only exclude the SYM (symbol) tag from the Spacy POS tagging set. The POS tagging set is based on the Penn treebank developed by Penn University. Compared to the POS tagging set in Stanford NLP, there are slight differences, but we think the Spacy POS tagging set is good enough for analysis. The research has shown that there is some relationship between the ratios in the POS tagging set.

### Syntactic complexity

Including the counting numbers of lemma, chunks, person singular verbs, clauses, and t-units.
We can use Spacy to tokenize and return the original lemma of the words, as well as count the most frequently used words.
In personal singular nouns, based on English grammar, we only need to count the number of verbs that appear after the singular noun (I) without Spacy or any NLP engine.
As for chunks, clauses, or t-units, they are the basic components in sentences that are based on the formula (e.g., {<.*>+}        }<VB.?|IN>+{). We can filter out the numbers simply by using some of the analysis provided in Spacy and StanfordNLP, like dependency trees or parser trees.
We have the prediction that the syntactic complexity will decrease in number in AD patients because of a leak of language-speaking memory.

### Vocabulary richness

