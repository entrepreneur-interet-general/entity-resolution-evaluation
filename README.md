
# entity-resolution-evaluation

A python package to evaluate entity resolution

This package allows to evaluate entity resolution by efficiently computing several state of the art metrics : basic merge distance, precision, recall, variation of information. It's using the slice algorithm from the paper :

Menestrina, David and Whang, Steven Euijong and Garcia-Molina, Hector (2010) Evaluating Entity Resolution Results
http://ilpubs.stanford.edu:8090/975/3/ERMetricVLDB.pdf

## Getting Started

### Installing

```bash
pip install entity-resolution-evaluation
```

### Testing

Evaluate your resolution *R* against the gold standard *S* using a *metric*.

Examples

```
S = [[0, 1], [2, 3, 4], [5]]
R = [[0, 1, 2], [3, 4], [5]]

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
