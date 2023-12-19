# Friendly CI/CD Helper

`friendly-cicd-helper` is a small demo project for how to use Vertex AI in common CI/CD tasks.

It uses Vertex AI to analyze code changes (in the form of a GitDiff) and generate the following outputs:
- Summary of the changes to help speed up a MR/PR review
- PR/MR comments for code changes to provide initial feedback to the author
- Release Notes for changes for code changes

To integrate directly with a PR/MR flow it uses the Gitlab or GitHub API to:
- Comment on an issue
- Comment on a PR or MR

The firendly-cicd-helper can be used in the following ways:
- as a standalone python application
- as a container image 
- in a container-based CI/CD pipeline such as Cloud Build

## Getting Started

To use the `friendly-cicd-helper` as a container image you'll need to build and run the image:

```sh
docker build . -t friendly-cicd-helper
docker run friendly-cicd-helper --help
```

To use the `friendly-cicd-helper` as a python application you'll need to install the dependencies and then run the application:

```sh
pip install -r
python friendly-cicd-helper.py --help
```

To use the `friendly-cicd-helper` in a Cloud Build pipeline you'll need to build the image and then submit a pipeline that uses it.

```sh
# adapt these with your values
PROJECT_ID=<your-project-id>
REGION=europe-west1
REPO_NAME=default
IMAGE_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/friendly-cicd-helper"

gcloud builds submit . --substitutions "_IMAGE_PATH=$IMAGE_PATH"
gcloud builds submit --config ./docs/demo-pipeline/print-cli-help.yaml --substitutions "_IMAGE_PATH=$IMAGE_PATH"
```

In all of these cases you should see the following help output:

```txt
Usage: friendly-cicd-helper.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  github-comment       This command will post a comment to a GitHub issue.
  gitlab-comment       This command will post a comment to a Gitlab issue.
  gitlab-mergerequest  Find the most recent Merge Request for a given...
  vertex-code-comment  Comment on a Git Diff in the form of a summary
  vertex-code-review   Review on a Git Diff
```

## How to use the `friendly-cicd-helper`

Detailed instructions for how to use the `friendly-cicd-helper` are located in the [docs](./docs/USAGE.md) folder.

## Contributing

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).

## Getting help

Please use the [issues page](https://github.com/GoogleCloudPlatform/friendly-cicd-helper/issues) to provide feedback or submit a bug report.

## Disclaimer

This is not an officially supported Google product. The code in this repository is for demonstrative purposes only.