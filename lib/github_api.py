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

from github import Github, Auth

import os

def issue_comment(repo_path, issue_number, comment):
    """
    Post a comment to an existing GitHub issue in the specified repo.
    """

    token = os.getenv('GITHUB_TOKEN')
    if token is None:
        print('Please set the GITHUB_TOKEN environment variable.')
        return

    auth = Auth.Token(token)
    client = Github(auth=auth)
    repo = client.get_repo(repo_path)
    issue = repo.get_issue(number=issue_number)
    issue_comment = issue.create_comment(comment)
    print(f'Posted a comment to GitHub issue. Link: {issue_comment.html_url}')
