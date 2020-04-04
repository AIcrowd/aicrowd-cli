import os

import click

from handlers.git_handler import Git

GITLAB_URL = "gitlab.aicrowd.com"

class Submission:
    def __init__(self, challenge_id, username, project_slug, ssh_private_key=None, personal_access_token=None, **kwargs):
        # if no gitlab project available tell the user to create one by
        # redirecting him to this page https://gitlab.aicrowd.com/projects/new
        self.challenge_id = challenge_id
        self.git_username = username
        self.git_project_slug = project_slug
        print(ssh_private_key, personal_access_token, project_slug, username)
        self.git_repo_username = self.git_username
        if(ssh_private_key):
            self.command_git_url = 'git@%s:%s/%s.git' %(GITLAB_URL, self.git_repo_username, self.git_project_slug)
            self.git = Git(ssh_private_key=ssh_private_key)
            self.git.remote('add ssh-submission %s' % (self.command_git_url))
        elif personal_access_token:
            self.command_git_url = 'https://oauth2:%s@%s/%s/%s.git' %(personal_access_token, GITLAB_URL, self.git_repo_username, self.git_project_slug)
            self.git = Git()
            self.git.remote('add http-submission %s' % (self.command_git_url))


        # Add remote "submission" for the project using these details

    def submit_current_project(self, version_number, http, dummy):
        current_directory = os.getcwd()
        self.git.add('.')
        self.git.commit("-m 'updated submission'")
        self.git.tag("-am 'submission-v%s' submission-v%s" % (version_number, version_number))
        if(http):
            self.git.push("-f ssh-submission master")
            self.git.push("-f ssh-submission submission-v%s" % (version_number))
        else:
            self.git.push("-f http-submission master")
            self.git.push("-f http-submission submission-v%s" % (version_number))


        click.echo("Now you can check details of your submission at: "
                   "https://gitlab.aicrowd.com/%s/%s/issues" % (self.git_repo_username, self.git_project_slug))
