# NLP: extract workable feature from the text
I will discuss the feature we extract, and discuss the method we use in coding part.
## Working engine
The main engines we used in this project composed of three parts:
### Spacy

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/0dc123af-7be8-4441-a92b-0b91769deee2)

A scientific engine built on Python has the advantages of easy-to-use function calls, an extensive support library based on it, and the speed of a natural language process, but it also has disadvantages in terms of lacking professional skills in parser trees or more advanced NLP skills.
### NLTK

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/7717a190-0384-4878-8838-c56b79b62d79)

With the NLTK library, we can use it to analyze more advanced lexical features with the Sk-Learn library, like the bag of words module and the basic parser tree module.

### Stanford NLP

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/d6794efd-22d6-4bc4-a186-a2d51f634516)

Stanford NLP, developed by Stanford University. It is built on a server, we can analyze the text with our local host, and it can do more advanced parser tree and dependency tree analysis, but it has a problem with the length of the sentence; if the sentence is too long, the analyzer will overflow in memory.

### Stanza

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/e89dfd5b-e9a3-4daa-b126-82b3776e8e34)


Stanza Library is the optimal version of Stanford NLP; it can simply use pip to install and execute, adding up to a more extensible package,so we usually use stanzas to analyze more advanced features because of their convenience.

## Extract features

### POS tagging 
POS, aka part of a sentence, has the following tags: ADJ (adjective), ADP (adposition), ADV (adverb), AUX (auxilary), CONJ (conjunction), DET (determiner), INTJ (interjection), NOUN (noun), NUM (numerical), PART (particle), PRON (pronoun), PROPN (propernoun), PUNCT (punctuation), SCONJ (subordinating conjuction), SYM (symbol), VERB (verb), X (other), SPACE (space), we only exclude the SYM (symbol) tag from the Spacy POS tagging set. The POS tagging set is based on the Penn treebank developed by Penn University. Compared to the POS tagging set in Stanford NLP, there are slight differences, but we think the Spacy POS tagging set is good enough for analysis. The research has shown that there is some relationship between the ratios in the POS tagging set.
We have chosen the specific POS tagging set, which is content words and function words. Content words usually include verbs, nouns, adjectives, and adverbs. Function words usually include auxiliary verbs, prepositions, conjunctions, and pronouns. We can predict that AD patients will reduce the frequency of content words and increase the frequency of function words. 

### Basic Syntactic complexity

Including the counting numbers of lemma, chunks, person singular verbs, clauses, and t-units.
We can use Spacy to tokenize and return the original lemma of the words, as well as count the most frequently used words.
In personal singular nouns, based on English grammar, we only need to count the number of verbs that appear after the singular noun (I) without Spacy or any NLP engine.
As for chunks, clauses, or t-units, they are the basic components in sentences that are based on the formula (e.g., {<.*>+}        }<VB.?|IN>+{). We can filter out the numbers simply by using some of the analysis provided in Spacy and StanfordNLP, like dependency trees or parser trees.
We have the prediction that the syntactic complexity will decrease in number in AD patients because of a leak of language-speaking memory.

### Vocabulary richness
Including type-token ratio, moving average type-token ratio, Brunet’s index, and Honore’s statistic.

In type-token ratio, we take a text for example:

<img width="433" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/e051452f-93b0-4a66-b4f2-bd5b63954229">

The text has fallowing types and token:

<img width="419" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/53d3d0ce-9558-4452-9002-4d152e8cb154">

We calculate the type-token ratio by simply divide type and tokens.

<img width="437" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/c6e94dd0-a564-4d04-838e-553b5f3ae5dc">

So, we assume total vocabulary used in a dialogue as V, total word count as N, the formula will be in below.

TTR = V / N
In moving average type-token ratio, we can extend the type-token ratio by designing a window, summing up the type-token ratio in different ways, and taking a mean of it.
The modify formula is like in below:

MATTR = Number of Windows / Sum of TTRs in all Windows
      = Σ vi / Σ Ni i = text in windows

Then, Brunét’s Index(BI), Honore’s Statistic (HS) can do deeply analysis by calculated it using the formula:

Brunét’s Index (BI) = N^V(-0.165)

Honore’s Statistic (HS) = (100 log N) / (1 - V1 / V)

We assume V1 = accounting for words that are only used once

In implementation, we can use tokenize function supported by Spacy library simply.

### Negation analysis
The negation detection is an important analysis in NLP segment. There are some different implement, there is negation tag in Spacy tagging set, but we have seen that it can only tagging out the not but bot the nagation meaning words. So, we seek for the negation detection library called NegSpaCy, it is originlally used in the diagnosis of the hospital, it can tag out the negation objective of the text. 

![icon](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/4fefcf06-13fd-4414-8563-e576d03e538d)

![1_kWJa0M0JI4oVhVgP7wnNTQ](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/00e962d7-a486-4e81-aac0-8b6352e58c14)

The demo result will be as below: 

```python
doc = nlp("She does not like Steve Jobs but likes Apple products.")

for e in doc.ents:
	print(e.text, e._.negex) 
```
```python
Steve Jobs True
Apple False
```

### Name entity recognized

When we examine the text, we can see some proper nouns that will occur in the text. In the Spacy library, there is a NER (name entity recognized) function to analyze different categories of proper nouns, so we tag out the NER (name entity recognized) in the text and specifically highlight out the time NER in the text because AD patients can hardly remember the time priority of the events that occur.

### Emoji analysis

When we listen to the patient's audio, we can observe that the patient won't have too much emotional effect on the speaker. So, we are using the Stanza library to analyze the emotional effect in each sentence of the text. There are three kinds of representations in expressing the emotional, respectively negative, positive, and no emotion.

### Psycholinguistics

Then, we will ask whether the words AD patients use are familiar to them in their daily lives. So, we use SUBTL frequency norms, which collect the daily term in drama and video clips. We can average each word in the text to get the degree of familiarity easily.

### Advanced Syntactic complexity

Including Yngve Depth, left-branching depth, Frazer Depth, and Syntactic Dependency Length (SDL) scores, three-part advanced analysis using a parser tree developed by Stanford NLP.
Yngve Depth is named after American linguist Kenneth Yngve. We need to use a parser tree to identify embedded structures, define the depth of each embedded structure, and sum all of the depths up. And the left-branching tree is the theory based on Yngve depth; we can also calculate it with a parser tree.
Frazer depth, which is similar to Yngve depth, It is named after American linguist Michael Frazer; it identifies and counts the number of subordinate clauses in the sentence.
Syntactic Dependency Length (SDL) is a measure of sentence complexity as well, but it is different from the above two methods. It's first performing dependency parsing with the sentence, calculating the syntactic dependency length, the difference between head words and dependency words, and giving an average on all of the syntactic dependency.
We are finally using the basic implements in syntactic complexity, dependency tree, and parser tree. We simply calculate the mean, average, and maximum height of these two trees.

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/b4ac49a9-dcf8-453b-b4ee-02d498155879)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/54e8b8f3-db51-4e2a-b482-c29d0d1a3b2e)

### Repetitiveness

Repeatness is an important issue in AD patient diagnosis as well. In the first place, we don't find a good way to extract this feature because the differences between the sentences can't be measured by the words or the lemma. However, we have discovered the Bag-of-Words Model (BoW) module and recognized its similarity to different words.

![20140744GORvWkZG8N](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/3745a8f5-58b9-427d-beb4-6a2b55878d20)

We can give a brief description in a bag of words. We uses Sk-Learn and NLTK to do the document vectorization, calculating the cosine distance between each sentence and forming the difference matrix. We will set a threshold; if the distance is below the threshold, we'll assume the two sentences are the same. So, we can calculate the proportion of repeatness in the text.

![0_B3rOPw4OVDRSqpU8](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/40e9c809-83cf-4067-9e5e-034298edbb2d)

### Silence splitting

`get_silent.py`

The silence pause splitting is an important issue in AD diagnosis. We can use a similar idea in noise reduction using the Pydub library and set a threshold in amplitude and the length of the silence segment. If the silence segment fits the threshold we set, we will split it out.

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/709a7e73-e0a2-4ee5-ac93-803bab56024d)

## Final result
`LearningModel_lasso_lexical.ipynb`

We select the lexical analysis features and training module on it. We can observe that if we put all of the features in the module, it'll have poorer performance in accuracy (about 0.7), a f1 score of 0.67, and very poor performance on the MCC value (about 0.2), so the dimension reduction is crucial for the training datasets.

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/6f6662f2-0d14-4dc4-9900-11c77467abef)

So, we implement the lasso dimension reduction and select the features that affect the results the most. We can speculate that syntactic complexity didn't work as well as we thought before. The reason behind this, I think, is that the daily speech didn't have a very complex syntactic structure. The final lexical result will be as below:

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/56293815-5f91-43f5-bf26-56a4b41ab26c)

It has higher accuracy, f1 score, and MCC scores, even as high as the fused result in the below context.

