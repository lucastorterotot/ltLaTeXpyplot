# ltLaTeXpyplot python package

This package is under development for the moment!

## Introduction

This package for Python 3.x provides tools to produce easily `pgf` figures to be used with LaTeX with a pre-defined theme.

## Installation

1. Go in a directory where you want to install this repository and clone it:
```
git clone git@gitlab.com:lucastorterotot/ltLaTeXpyplot.git --origin lucas
```
2. Run the provided installation script:
```
./ltLaTeXpyplot/install
```
3. Install required `Python3` modules:
```
apt-get update
apt-get install python3-numpy python3-scipy python3-matplotlib
```
4. You might want the most up-to-date version of matplotlib:
```
apt-get install python3-pip
python3 -m pip install matplotlib --upgrade
```
5. As LaTeX rendering is used along with some packages, `texlive` is also required. One could either make a minimal installation with
```
apt-get install texlive texlive-latex-extra texlive-science
```
or use a full (but heavier) installation with
```
apt-get install texlive-full
```

## Usage

See the examples [in this directory](https://gitlab.com/lucastorterotot/ltLaTeXpyplot/tree/master/examples).