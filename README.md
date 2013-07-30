# git2s3

Upload files in git directory to S3 when access /git2s3

## pip

```
pip install bottle
pip install GitPython
pip install boto
```

## run

### debug

```
python git2s3.py
```

### production

I recommend gunicorn

```
pip install gunicorn
gunicorn -b 127.0.0.1:3000 -w 1 git2s3:app --timeout=3000 --daemon
```
