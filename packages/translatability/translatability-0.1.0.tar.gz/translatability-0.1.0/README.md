# Assessing-Translatability
Algorithmic procedure for scoring German compounds according to English-Translatability.

---

### Overview

If you have done any translation or are familiar with the vocabulary of a second language, then it is apparent that some words or concepts are easier to translate than others. Many are familiar with the German-English loanwords ‘Schadenfreude’ or ‘Wanderlust,’ which mean, respectively, a perverse pleasure gained at the expense of another’s pain and a desire to leave an area of comfort and see the outside world.

This project aims to develop an algorithmic procedure for quantifying a 'translatability' score using the statistical properties of words and their translations. The procedure only works for German compound nouns.

---

### Installation

```
pip install translatability
```

***

### CLI

```
python -m translatability --help
```

---

### Corpora

You can download parallel corpora necessary for the calculations from the links below.

- http://opus.nlpl.eu/Europarl.php

- http://opus.nlpl.eu/Wikipedia.php

- http://opus.nlpl.eu/OpenSubtitles-v2018.php

Ensure you download the above corpora as aligned MOSES format. The image below demonstrates the appropriate download link for the OpenSubtitles corpus, which is found in the second of the two download matrices, within the lower-left triangle where the indices for "EN" and "DE" align. Please do not use the other "DE-EN" link in the top-right triangle because these data are in the wrong format.

![](https://github.com/christianj6/assessing-translatability/blob/master/docs/moseslink.png)

You may pass the absolute path to each of the files when running the main script, as in the example below.

```
python -m translatability -w <path to Wikipedia corpus> -e <path to Europarl corpus> -s <path to OpenSubtitles corpus> -f <path to file>
```

---

### Usage Example

```
python -m translatability -w "./wikipedia" -f res/test_short.txt

>>> ...
>>> The final list of scored words:
	0.7139908155580019 Salzwasser
	0.6117190378041573 Landzunge
	0.5171641715308692 Schnapsidee
```

In the ```/res``` directory you will find several sample texts which may be used for similar evaluations.

---

### Documentation

For further details on the algorithm, its evaluation, and application in a small study, please consult the ```/docs``` directory.

---

### Notes

- The ```src/split.py``` module is a modified version of the [CharSplit](https://github.com/dtuggener/CharSplit) algorithm by dtuggener. All credit goes to this individual.
- At the end of each run of the scripts, there is created in the current working directory a ```results``` and ```segments``` directory containing temporary data. You should clean these files between runs or else results will be contaminated.

***

