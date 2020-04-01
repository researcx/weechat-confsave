## weechat-confsave

Save non-default config variables to a file in various different formats.

Note: will attempt to exclude plaintext passwords.

https://weechat.org/scripts/source/confsave.py.html/

#### INSTALLATION:
##### Through weechat
```
/script install confsave.py
```

##### Manually
**wget:**
```
wget -P .weechat/python/ https://github.com/unendingPattern/weechat-confsave/raw/master/confsave.py
```

**curl:**
```
curl -LJo .weechat/python/confsave.py https://github.com/unendingPattern/weechat-confsave/raw/master/confsave.py
```


#### USAGE:
```
/confsave [filename] [format]

    filename: target file (must not exist)
    format: raw, markdown or commands
```