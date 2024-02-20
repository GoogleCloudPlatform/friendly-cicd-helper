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

import vertexai
import os
import sys
from vertexai.language_models import TextGenerationModel

if os.environ.get("VERTEX_GCP_PROJECT")==None:
    print("Please set VERTEX_GCP_PROJECT environment variable", file=sys.stderr)
    sys.exit(1)

vertex_location = "europe-west1"
if os.environ.get("VERTEX_LOCATION")!=None:
    vertex_location = os.environ.get("VERTEX_LOCATION")

vertexai.init(project=os.environ.get("VERTEX_GCP_PROJECT"), location=vertex_location)

model = TextGenerationModel.from_pretrained("text-bison-32k@002")

parameters = {
    "max_output_tokens": 1024,
    "temperature": 0,
}

def load_diff(diff_path):
    """
    Load a Git diff from a file.
    """
    if not os.path.exists(diff_path):
        print(f"{diff_path} does not exist", file=sys.stderr)
        sys.exit(1)
    with open(diff_path, 'r') as file:
        data = file.read()
    return f"""

A Git Diff works as follows:
- Lines starting with a space character ' ' are unchanged and included for context only.
- Lines starting with a plus character '+' are added.
- Lines starting with a minus character '-' are removed.
- Lines starting with a caret character '^' are modified.
- Lines starting with a pound character '#' are comments.
- Lines starting with an at character '@' are meta data.

When working with the Git diff, you only comment on code that has been changed, added or removed as indicated in the Git diff.

======= START Git Diff =======
${data}
======= START Git Diff =======
    """

def code_summary(diff_path):
    """
    Generate a code summary based on a Git diff.
    """

    response = model.predict(
        f"""
You are an experienced software engineer.

Provide a summary of the most important changes based on the following Git diff:

${load_diff(diff_path)}

        """,
    **parameters
    )
    print(response.text.strip())
    return response.text


def code_review(diff_path):
    """
    Generate a code review based on a Git diff.
    """

    response = model.predict(
        f"""
You are an experienced software engineer.
You only comment on code that you found in the merge request diff.
Provide a code review with suggestions for the most important 
improvements based on the following Git diff:

${load_diff(diff_path)}

        """,
    **parameters
    )
    print(response.text.strip())
    return response.text

def release_notes(diff_path):
    """
    Generate release notes based on a Git diff in unified format.
    """

    response = model.predict(
        f"""
You are an experienced tech writer.
Write short release notes as markdown bullet points for the most important changes based on the following Git diff:

${load_diff(diff_path)}
        """,
    **parameters
    )
    print(response.text.strip())
    return response.text
