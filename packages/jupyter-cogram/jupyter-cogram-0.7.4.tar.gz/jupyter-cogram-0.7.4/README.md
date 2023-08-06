<a href="https://cogram.ai">                                                        
<img src="https://uploads-ssl.webflow.com/61294dc1bd225d7c490b4389/61337287d439e010eae32f7f_logo_black_and_white_2048.png" 
width="250" align="right"/>
</a>

# Cogram: Intuitive coding with natural language

Cogram brings intuitive coding with natural language to Jupyter Notebook.

[![pypi Version](https://img.shields.io/pypi/v/jupyter-cogram.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/jupyter-cogram/)
[![Cogram on Slack](https://img.shields.io/badge/Slack-pink.svg)](https://join.slack.com/t/slack-cng9493/shared_invite/zt-v79xffk1-oTkdfMJ9yLpd8E2YhU2l4Q)

## 📖 Documentation

| Documentation              |                                                                |
| -------------------------- | -------------------------------------------------------------- |
| 🚀️ **[Sign up]**        | Sign up to get your API token and get started!              |
| ⭐️ **[How to]**        | New to Cogram? Check out our videos on how to get started!              |
| 📚 **[Community]**      | Have questions our comments? Join our Slack!                             |

[sign up]: https://get.Cogram.ai
[how to]: https://youtu.be/8i1zTdQ1xKI
[community]: https://join.slack.com/t/slack-cng9493/shared_invite/zt-v79xffk1-oTkdfMJ9yLpd8E2YhU2l4Q

## Features

- AI-powered coding for Jupyter Notebooks
- Supports Python: ideal for data science tasks
- Cycle through different suggestions

## ⏳ Install cogram

### Requirements

- **API token**: If you don't have one yet, [sign up]
- **Operating system**: macOS · Linux · Windows
- **Python version**: Python 3.6+ (only 64 bit)
- **Package managers**: [pip]

[pip]: https://pypi.org/project/spacy/
[conda]: https://anaconda.org/conda-forge/spacy

### Installation

The easiest way to install Cogram for Jupyter Notebook is using pip.

```bash
pip install -U jupyter-cogram
jupyter nbextension enable jupyter-cogram/main
```

You can now start a new Jupyter Notebook server with 
```bash
jupyter notebook
```

and you're ready to go!


### Updating Cogram

The easiest way to upgrade to a new version of Cogram is using pip:

```bash
pip install -U jupyter-cogram
```

You'll then have to kill any active Jupyter Notebook servers and start a new one with 
```bash
jupyter notebook
```

## 📚 Use Cogram

### 🛫 First start

If you've installed Cogram by following the instructions on your [My Account](https://get.cogram.ai/account) page your API token
will automatically be saved. You can open a Jupyter Notebook and get started.  

You may be asked for your API token when you open a new Notebook for the first time. 
You can find your API token on your [My Account](https://get.cogram.ai/account) page. 
Paste this into the prompt box that opens when you start a new Jupyter Notebook.

You can toggle the extension off and on by clicking the Cogram button 
(<img align="center" width="14" src="https://uploads-ssl.webflow.com/61294dc1bd225d7c490b4389/6131d7249979f73249363dd0_icon_black_64.png" />) in the toolbar. The green
circle indicates that Cogram is active. 
  
### 🔮 Prompting Cogram

You can prompt Cogram by writing a comment into a code cell starting with `##`. 
Submit the prompt by typing `##` again. 
The status light will turn orange indicating that Cogram is busy. 
 
For example, the prompt
```python
## fibonacci sequence ##
```
will generate different functions that produce the Fibonacci sequence.
 
Once your code has been generated, you can explore different options with the ← and → keys. 
If you're happy with a suggestion, you can accept it by waiting for two seconds. 
Alternatively, you can accept it right away by hitting ⌘+⏎ (macOS) or Ctrl+⏎ (Windows & Linux).

### 💡 Tips for working with Cogram

Cogram works especially well if you give it some context. 
Cogram knows the cells in your notebook above the cell in which you're prompting Cogram. 
So the more cells you've already written, the better Cogram will work.

### 📚 Support 

For help with Cogram please join our support channel in [community]. 
