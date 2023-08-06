![Image of REDACTED STAMP](https://github.com/freelawproject/pdf-redaction-detector/blob/master/Screenshot%20from%202020-12-17%2011-06-09.png)

x-ray is a Python 3.8 library for finding bad redactions in PDF documents.

# Why this exists

XXX

# Installation

With poetry, do:

```text
poetry add x-ray
```

With pip, that'd be:
```text
pip install x-ray
```

# Usage

You can easily use this on the command line. Once installed, just:

```bash
% python -m xray path/to/your/file.pdf
{
  "1": [
    {
      "bbox": [
        58.550079345703125,
        72.19873046875,
        75.65007781982422,
        739.3987426757812
      ],
      "text": "12345678910111213141516171819202122232425262728"
    }
  ]
}
```

That'll give you json, so you can use it with tools like [`jq`][jq]. Handy.

If you want a bit more, you can use it in Python:

```python
from pprint import pprint
import xray
bad_redactions = xray.inspect("some/path/to/your/file.pdf")
pprint(bad_redactions)
{1: [{'bbox': (58.550079345703125,
               72.19873046875,
               75.65007781982422,
               739.3987426757812),
      'text': '12345678910111213141516171819202122232425262728'}]}
```

That's pretty much it. There are no configuration files or other variables to
learn. You give it a file name. If there is a bad redaction in it, you'll soon
find out.

# How it works

{{NEW-PROJECT}} is an open source repository to ...
It was built for use with Courtlistener.com.

Its main goal is to ...
It incldues mechanisms to ...

Further development is intended and all contributors, corrections and additions are welcome.

## Background

Free Law Project built this ...  This project represents ...  
We believe to be the ....


## Fields

1. `id` ==> string; Courtlistener Court Identifier
2. `court_url` ==> string; url for court website
3. `regex` ==>  array; regexes patterns to find courts


## Installation

Installing {{NEW-PROJECT}} is easy.

```sh
pip install {{NEW-PROJECT}}
```


Or install the latest dev version from github

```sh
pip install git+https://github.com/freelawproject/{{NEW-PROJECT}}.git@master
```

## Future

1) Continue to improve ...
2) Future updates

## Deployment

If you wish to create a new version manually, the process is:

1. Update version info in `setup.py`

2. Install the requirements using `poetry install`

3. Set up a config file at `~/.pypirc`

4. Generate a universal distribution that works in py2 and py3 (see setup.cfg)

```sh
python setup.py sdist bdist_wheel
```

5. Upload the distributions

```sh
twine upload dist/* -r pypi (or pypitest)
```

## License

This repository is available under the permissive BSD license, making it easy and safe to incorporate in your own libraries.

Pull and feature requests welcome. Online editing in GitHub is possible (and easy!)

[jq]: https://stedolan.github.io/jq/
