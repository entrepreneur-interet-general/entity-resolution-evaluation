
# entity-resolution-evaluation

A python package to evaluate entity resolution

This package allows to evaluate entity resolution by efficiently computing several state of the art metrics : basic merge distance, precision, recall, f1-score and variation of information. It's using the slice algorithm from the paper :

Menestrina, David and Whang, Steven Euijong and Garcia-Molina, Hector (2010) Evaluating Entity Resolution Results
http://ilpubs.stanford.edu:8090/975/3/ERMetricVLDB.pdf

## Getting Started

### Prerequisites

This package assume that you have a gold standard (or truth) *S* on at least a subset of your records. [Create a gold standard](#create-a-gold-standard)

### Installing

```bash
pip install entity-resolution-evaluation
```

### Testing

Evaluate your resolution *R* against the gold standard *S* using a *metric*.

Examples

```
R = [[0, 1, 2], [3, 4], [5]]
S = [[0, 1], [2, 3, 4], [5]]

evaluate(R,S, 'bmd')
# returns 2
```
To go from R to S, you have to do 1 split and 1 merge.
```
evaluate(R,S,'precision')
# returns 0.5, 
```
Half of the pairs of R are incorrect. (0,2) and (1,2) are incorrect. (0,1) and (3,4) are correct
```
evaluate(R,S,'recall')
# returns 0.5
```
Half of the pairs of S are present in R. (0,1) and (3,4) are present. (2,3) and (2,4) are absent.
```
evaluate(R,S,'variation of information')
# returns 0.6365141682948129
````

### Metrics 

You can currently compute the following metrics :

|metric|value if perfect|bounds|intepretation|
|------|----------------|------|--------------|
|'bmd'|0|[0,infinity]|basic merge distance : the number of split and merge necessary to go from R to S|
|'precision'|1|[0,1]|proportion of pairs in R present in S|
|'recall'|1|[0,1]|proportion of pairs in S present in R|
|'f1'|1|[0,1]|harmonic mean of precision and recall|
|'variation_of_information'|0|[0,infinity]|amount of information that is lost and added to go from R to S|

### Reconciliation

Given that labelling is expensive, usually your gold standard S will contains only a subset of all your records. But your entity resolution R will contains all of them. In that case you'll get an error when evaluating :

```
R = [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9]]
S = [[0, 1], [2, 3, 4], [5]]

evaluate(R,S, 'bmd')
# returns an error
# "R and S have different numbers of distincts records : R has 10 distinct records while S has 6 distinct records"
```

Here you first need to reconcile R and S so that they contain the same subset of records. In order to do that you can use the function reconcile :

```
R = [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9]]
S = [[0, 1], [2, 3, 4], [5]]

R0, S = reconcile(R,S, 'R0S')

# R0 = [[0, 1, 2], [3, 4], [5]]
# S = [[0, 1], [2, 3, 4], [5]]
```

Here using the 'R0S' method we only changed R so that R have the same subset of records as S. [8,9] is an entity where all records are not in S. Therefore we'll just delete it.
[5,6,7] is more problematic. Indeed part of the entity (5) is present in S while part of it (6,7) is not. Let's call it a "mixed entity". By using the 'R0S' reconciliation method the entity [5, 6, 7] transformed into [5]. So we may have lost quite a bit of information about R.
Here we get a better estimation of the recall of our entity resolution than in the 'R1S1' method.

Another way to reconcile R and S while keeping more of the information in R is to use 'R1S1' method :

```
from entity_resolution_evaluation import reconcile

R = [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9]]
S = [[0, 1], [2, 3, 4], [5]]

R1, S1 = reconcile(R,S, 'R1S1')

# R1 = [[0, 1, 2], [3, 4], [5, 6, 7]]
# S1 = [[0, 1], [2, 3, 4], [5], [6, 7]]
```

Here we added the rest of our mixed entity [6,7] in S as another entity. Here we get a better estimation of the precision of our entity resolution than in 'R0S'.

### Qualitative Evaluation

Sure getting a quantitative evaluation of our entity resolution is nice. But to get a better feeling of what went wrong there's no getting around looking at examples of badly resolved entities.

We'll differentiate 2 types of badly resolved entities : 
- *glued entities* are entities of R that glued together a large number of entities of S. 
- *broken entities* are entities of S that were broken in a large number of entities in R.

```
from entity_resolution_evaluation.evaluation import worst_entities

R = [[0, 1, 2], [3, 4], [5]]
S = [[0, 1], [2, 3, 4], [5]]

s_broken_entities, s_r_broken_entities_dic = worst_entities(R,S,'broken') 

# s_broken_entities = [1, 0, 2]
# s_r_broken_entities_dic = {0: {0}, 1: {0, 1}, 2: {2}}
```
The worst broken entities are : the second entity (0 indexing) of S ([2,3,4]) which is present in the entities 0 and 1 of R (respectively [0,1,2] and [3,4] ). It's the only entity of S that is broken.


```
from entity_resolution_evaluation.evaluation import worst_entities

R = [[0, 1, 2], [3, 4], [5]]
S = [[0, 1], [2, 3, 4], [5]]

r_glued_entities, r_s_glued_entities_dic = worst_entities(R,S,'glued') 

# r_glued_entities = [[0, 1, 2]
# r_s_glued_entities_dic = {0: {0}, 1: {0, 1}, 2: {2}}
```
The worst glued entities are : the first entity of R ([0,1,2]) which is present in the entities 0 and 1 of S (respectively [0,1] and [2,3,4] ). It's the only entity of R that is glued.


### Create a gold standard


## Credits

<div align="center">
  <a href="https://entrepreneur-interet-general.etalab.gouv.fr/">
    <img src="docs/img/logo-eig.png" width="500px">
  </a>
</div>

Please visit the [Hopkins mission](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2018/hopkins.html) page for more information

## License

MIT License

Copyright (c) 2018 Ministère de l'Action et des Comptes Publics, Paul Boosz, Benoît Guigal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
