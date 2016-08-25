from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from git import Repo

def get_commits(git_repo_dir='/tmp/test/', max_count=20):
    repo = Repo(git_repo_dir)
    commits = list(repo.iter_commits("master", max_count=max_count))
    return commits

def index(request):
    git_repo_dir = "/tmp/test/"
    commits = get_commits()
    if request.method == "POST":
        rollback_hash = request.POST["rollback"]
        for commit in commits:
            if commit.hexsha == rollback_hash:
	        repo = Repo(git_repo_dir)
                git = repo.git
                git.reset("--hard", commit)
                break  

    return render_to_response('commit/index.html', {"commits": commits}, context_instance=RequestContext(request))
