# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--repo', default=None, help='The repository to use (format: user/repo)', required=True, type=str)
@click.option('--issue', default=None, help='The issue number', required=True, type=int)
@click.option('--comment', default=None, help='The comment to post', required=False, type=str)
def github_comment(repo, issue, comment):
    """
    This command will post a comment to a GitHub issue.
    """
    import lib.github_api as github
    if comment is None:
        click.echo('Reading the comment from stdin. Press Ctrl+D when done.')
        std_in = click.get_text_stream('stdin')
        comment = std_in.read()

    github.issue_comment(repo, issue, comment)

@cli.command()
@click.option('--project', default=None, help='The project to use (format: user/repo)', required=True, type=str)
@click.option('--issue', default=None, help='The issue number', required=False, type=int)
@click.option('--mergerequest', default=None, help='The merge request number', required=False, type=int)
@click.option('--comment', default=None, help='The comment to post', required=False, type=str)
def gitlab_comment(project, issue, mergerequest, comment):
    """
    This command will post a comment to a Gitlab issue.
    """

    import lib.gitlab_api as gitlab
    if comment is None:
        click.echo('Reading the comment from stdin. Press Ctrl+D when done.')
        std_in = click.get_text_stream('stdin')
        comment = std_in.read()

    if issue is not None:
        gitlab.issue_comment(project, issue, comment)
    elif mergerequest is not None:
        gitlab.merge_request_comment(project, mergerequest, comment)
    else:
        click.echo('Please specify either an issue or a merge request to comment on')

@cli.command()
@click.option('--project', default=None, help='The project to use (format: user/repo)', required=True, type=str)
@click.option('--source', default=None, help='The name of the source branch of the merge request', required=False, type=str)
def gitlab_mergerequest(project, source):
    """
    Find the most recent Merge Request for a given source branch
    """
    import lib.gitlab_api as gitlab
    mergerequest = gitlab.get_latest_merge_request(project, source)
    return mergerequest


@cli.command()
@click.option('--diff', default=None, help='Path to the Git diff to comment on', required=True, type=str)
def vertex_code_summary(diff):
    """
    Write a human-readable summary of a Git Diff
    """
    import lib.vertex_api as vertex
    return vertex.code_summary(diff)

@cli.command()
@click.option('--diff', default=None, help='Path to the Git diff to comment on', required=True, type=str)
def vertex_code_review(diff):
    """
    Review on a Git Diff
    """
    import lib.vertex_api as vertex
    return vertex.code_review(diff)

@cli.command()
@click.option('--diff', default=None, help='Path to the Git diff to comment on', required=True, type=str)
def vertex_release_notes(diff):
    """
    Write release notes for a Git Diff
    """
    import lib.vertex_api as vertex
    return vertex.release_notes(diff)

if __name__ == '__main__':
    cli()