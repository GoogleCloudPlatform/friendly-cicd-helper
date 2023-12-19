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

import gitlab
import os
import sys

def issue_comment(project, issue, comment):
    """
    Post a comment to a Gitlab issue
    """
    gl = gitlab.Gitlab(private_token=os.environ['GITLAB_TOKEN'])
    project = gl.projects.get(project)
    issue = project.issues.get(issue)
    note = issue.notes.create({'body': comment})
    print(f'Posted a comment to Gitlab issue. Link: {issue.web_url}#note_{note.id}')

def merge_request_comment(project, mr, comment):
    """
    Post a comment to a Gitlab merge request
    """
    gl = gitlab.Gitlab(private_token=os.environ['GITLAB_TOKEN'])
    project = gl.projects.get(project)
    merge_request = project.mergerequests.get(mr)
    note = merge_request.notes.create({'body': comment})
    print(f'Posted a comment to Gitlab MR. Link: {merge_request.web_url}#note_{note.id}')

def get_latest_merge_request(project, source_branch):
    """
    Find the latest merge request id for a given source branch
    """
    gl = gitlab.Gitlab(private_token=os.environ['GITLAB_TOKEN'])
    project = gl.projects.get(project)
    merge_requests = project.mergerequests.list(source_branch=source_branch)
    if merge_requests:
        print(f'Latest merge request for {source_branch} is {merge_requests[0].iid}', file=sys.stderr)
        print(merge_requests[0].iid)
        return merge_requests[0].iid
    else:
        print(f'No merge requests found for {source_branch}', file=sys.stderr)
        return None
