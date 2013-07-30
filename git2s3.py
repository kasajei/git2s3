import os

from git import *
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from bottle import route, run, default_app



# TODO: setting your account!
# aws setting
AWS_KEY_ID = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = ""
# git directory
REPOSITORY_DIRE = ""


def git_pull():
    repo = Repo(REPOSITORY_DIRE)
    assert False == repo.bare

    origin = repo.remotes.origin
    origin.fetch()
    origin.pull()


def sync_s3():
    conn = S3Connection(AWS_KEY_ID, AWS_SECRET_KEY, host='s3-ap-northeast-1.amazonaws.com')
    bucket = conn.get_bucket(BUCKET_NAME)

    for abspath, rpath in iterate_files(REPOSITORY_DIRE):
        key = Key(bucket)
        key.key = rpath
        key.set_contents_from_filename(abspath)


def iterate_files(basedir):
    for (path, dirs, files) in os.walk(basedir):
        for fn in files:
            if fn.startswith('.'):  # file name not
                continue
            if path.find(".git") != -1:  # ignore file path has .git
                continue
            abspath = os.path.join(path, fn)
            yield abspath, os.path.relpath(abspath, basedir)


@route("/git2s3")
def git2s3():
    git_pull()
    sync_s3()
    return "sync ok!"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


app = default_app()




