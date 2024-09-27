### Install:
```python
pip install -r requirements.txt
```
### Usage:
1. Run DirConverter.py with python3
2. Select the directory where the files for conversion are located
3. Select the variant(s)
4. Wait for the conversion to complete

In the code you can change these variables:
`audio_convertto = "your_format" # Audio convert to`
`pictures_convertto = "your_format" # Photo convert to`
`pictures_quality = your_value # Quality level for photos`

It is important that the format you wrote is in the **`audio_ext`** or **`pictures_ext`** array respectively. If you want to add an extension (maybe I forgot some), add an element to the corresponding array.