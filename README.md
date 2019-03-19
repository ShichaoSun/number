# number
re for Chinese number and quantity detection

## basic grammar label(defined by instances or re)
|    name    |   label    | example |
| :------------: | :----------: | :-----------: |
|    Arabic digit   |   ad    | 123 1e-5 |
|    Chinese digit    |   cd    | 一 二 十 玖 |
|    Chinese Magnitude   |   mag    | 十 百 佰 |
|    Chinese Fraction Connective    |   cfc    | 分之 比 |
|    Chinese Radix Point    |   crp    | 点 |
|    Skip Magnitude Connective    |   smc    | 零 |
|    adv    |   adv    | 大 小 （五小队士兵） |
|    Ordinal Number Prefix    |   nop    | 第 |
|    idioms   |   idiom    | 进一步 |
|    comparision prefix  |  cp   | 大于 多于 |
|    comparision suffix  |  cs   | 多 |
|    estimation prefix  |  ep   | 大约 |
|    estimation suffix  |  es   | 上下 左右 |
|    quantity computational connective  |  qc   | / * 每 |
|    number span connective |  nc   | 到 ～ |
|    quantity |  q   | 本 件 块 |

## combination grammar label
|    name    |   label    | example |
| :------------: | :----------: | :-----------: |
|    Ordinal Number   |   ON    | 第二 |
|    number    |   NUM    | 一百二 1e-5 |
|    Chinese Number    |   CN    | 一百二 |
|    Chinese Fraction number   |   CFN    | 十分之一 |
|    Quantity Phrase    |   QP    | 五米 |

## label definition grammar
- instance or re
```
 mag::百
 mag::十
 cd::十
 ad::[-+]?(\d+(\.\d*)?)([eE][-+]?\d+)?([\/:](\d+(\.\d*)?)([eE][-+]?\d+)?)?%?‰?|\d+(,\d{3})+
 ```
 
- combination of other labels
```
NUM::$ad$ $mag$
NUM::$ad$
NUM::$CN$ 
QP::$NUM$ $q$ 
```

## Requirements
python >=3.5

## Demo
```
python3 test.py
```
