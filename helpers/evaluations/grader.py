import os
import time
import re
import yaml
import subprocess
import shutil
import wget
import platform
import aicrowd_evaluations
from aicrowd.config import Config
from aicrowd import fmt
from helpers.evaluations import HELM_REPO, API_HOST
from helpers.evaluations.auth import api_configuration


def parse_secrets(secrets):
    """Parse the secrets passed on command line into python dict"""
    parsed_secrets = {}
    for secret in secrets:
        key, value = secret.split("=")
        parsed_secrets[key] = value
    return parsed_secrets


class Settings:
    """Helper class to convert dicts to object"""

    def __init__(self, **entries):
        self.__dict__.update(entries)


def validate(repository_uri, secrets):
    """Validate the repository structure and aicrowd.yaml"""
    check_git_uri(repository_uri)
    check_aicrowd_yaml_keys()
    check_secrets(secrets)
    download_helm()
    check_template()


def check_git_uri(repository_uri):
    """Check if the passed git repository is in valid SSH format"""
    if re.match("(.+@)*([\w\d\.]+):(.*)", repository_uri) is None:
        raise ValueError(
            "--repo should be a valid git repository URL. Example: git@gitlab.aicrowd.com:aicorwd/aicrowd.git"
        )


def check_aicrowd_yaml_keys():
    """Validate the fields in aicrowd.yaml"""
    if not os.path.exists("./aicrowd.yaml"):
        raise FileNotFoundError(f"{os.path.curdir}/aicrowd.yaml does not exist!")
    with open("./aicrowd.yaml") as fp:
        grader_ctx = yaml.safe_load(fp)
    check_keys(["challenge.template"], 1, grader_ctx["challenge"])
    if "dataset" in grader_ctx:
        check_dataset_keys(grader_ctx)
    if "notifications" in grader_ctx:
        check_notifications_keys(grader_ctx)


def check_dataset_keys(grader_ctx):
    """Check for required fields for dataset"""
    check_keys(
        ["dataset.url", "dataset.capacity"],
        1,
        grader_ctx["dataset"],
        "when using a dataset",
    )
    if grader_ctx["dataset"]["capacity"][-1] not in ["K", "M", "G"]:
        raise ValueError(
            "`dataset.capacity` should specify a valid size, example: 300K, 100M, 1G"
        )
    if grader_ctx["dataset"]["url"].startswith("s3://"):
        check_keys(
            ["dataset.s3"], 1, grader_ctx["dataset"], "when using s3 resource",
        )
        check_keys(
            [
                "dataset.s3.endpoint",
                "dataset.s3.region",
                "dataset.s3.access_key",
                "dataset.s3.secret_key",
            ],
            2,
            grader_ctx["dataset"]["s3"],
            "when using s3 resource",
        )


def check_keys(keys, offset, ctx, msg=""):
    """Check if the keys exist in the given context dict"""
    for key in keys:
        path = key.split(".")[offset:]
        res = ctx
        for i in path:
            res = res.get(i)
            if res is None:
                raise KeyError(f"`{key}` should be specified in ./aicrowd.yaml {msg}")


def check_notifications_keys(grader_ctx):
    """Check for required fields for notifications"""
    for notifier in grader_ctx["notifications"]:
        check_keys(
            [
                "notifications[].name",
                "notifications[].image",
                "notifications[].message",
            ],
            1,
            notifier,
        )
        check_keys(
            ["notifications[].message.name", "notifications[].message.value"],
            2,
            notifier["message"],
        )


def check_secrets(secrets):
    """Check if all the secrets are mapped and return warning if there are unmapped ones"""
    with open("./aicrowd.yaml") as fp:
        secrets_in_yaml = set(re.findall("{[A-Za-z0-9_\.]+}", fp.read()))
    for key in secrets:
        secrets_in_yaml.remove("{" + str(key) + "}")
    if len(secrets_in_yaml) > 0:
        fmt.echo_alert(f"{', '.join(secrets_in_yaml)} do not have secrets mapped!")


def download_helm():
    """Check if helm exists and download it if it doesn't"""
    conf_dir, settings = load_config()
    if not os.path.exists(f"{conf_dir}/helm"):
        fmt.echo_info("Helm not found, downloading...")
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        wget.download(
            f"https://get.helm.sh/helm-v{settings.helm_version}-{settings.os}-{settings.arch}.tar.gz",
            out=f"{conf_dir}/helm.tar.gz",
        )
        shutil.unpack_archive(f"{conf_dir}/helm.tar.gz", f"{conf_dir}/tmp")
        shutil.move(
            f"{conf_dir}/tmp/{settings.os}-{settings.arch}/helm", f"{conf_dir}/helm"
        )
        shutil.rmtree(f"{conf_dir}/tmp")
        os.remove(f"{conf_dir}/helm.tar.gz")
        os.chmod(f"{conf_dir}/helm", 0o777)
        helm("init -c", stdout=subprocess.DEVNULL)
        helm(f"repo add aicrowd {HELM_REPO}")


def helm(cmd, stdout=None):
    """Execute a helm command"""
    conf_dir, settings = load_config()
    res = subprocess.run(f"{conf_dir}/helm {cmd}", shell=True, stdout=stdout)
    if res.returncode != 0:
        raise ValueError("Helm template check failed.")


def check_template():
    """Expand helm template and check for errors"""
    with open("./aicrowd.yaml") as fp:
        template = yaml.safe_load(fp)["challenge"]["template"]
    if os.path.exists(".aicrowd"):
        shutil.rmtree(".aicrowd/")
    helm(f"fetch --untar --untardir .aicrowd aicrowd/{template}")
    shutil.move(f".aicrowd/{template}/aicrowd.yaml", f".aicrowd/{template}/values.yaml")
    shutil.copytree(
        "./",
        f".aicrowd/{template}",
        ignore=shutil.ignore_patterns(".*"),
        dirs_exist_ok=True,
    )
    helm(
        f"template --values aicrowd.yaml .aicrowd/{template}", stdout=subprocess.DEVNULL
    )
    shutil.rmtree(".aicrowd/")


def load_config():
    """Load the CLI config"""
    config = Config()
    conf_dir = os.path.join(os.path.expanduser("~"), config.config_directory)
    settings = Settings(**config.settings)
    settings.os = platform.system().lower()
    settings.arch = "amd64"
    return conf_dir, settings


def create(cluster_id, repo, parsed_secrets, repo_tag, meta, auth_token):
    """Make post request to Evaluations API"""
    configuration = api_configuration(auth_token)

    api_instance = aicrowd_evaluations.GradersApi(
        aicrowd_evaluations.ApiClient(configuration)
    )
    payload = aicrowd_evaluations.Grader(
        evaluator_repo=repo,
        evaluator_repo_tag=repo_tag,
        cluster_id=cluster_id,
        secrets=parsed_secrets,
        meta=meta,
    )
    api_response = api_instance.create_grader(payload)
    return api_response
