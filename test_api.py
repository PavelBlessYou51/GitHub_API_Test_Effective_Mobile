import os

import pytest
import requests
from dotenv import load_dotenv


# CRUD methods
class GitHubUser:
    """Class contains CRUD methods for GitHub"""

    @staticmethod
    def get_repository(owner: str, repo: str, headers: dict[str, str]) -> tuple[int, str]:
        """Get repository from GitHub by name and owner"""
        url = f'https://api.github.com/repos/{owner}/{repo}'
        request = requests.get(url, headers=headers)
        status = request.status_code
        result_repo_name = request.json().get('name')
        return status, result_repo_name

    @staticmethod
    def create_repository(repo: str, headers: dict[str, str]) -> tuple[int, str]:
        """Creates repository from GitHub by name and owner"""
        url = 'https://api.github.com/user/repos'
        data = {
            'name': repo,
        }
        request = requests.post(url, headers=headers, json=data)
        status = request.status_code
        result_repo_name = request.json().get('name')
        return status, result_repo_name

    @staticmethod
    def delete_repository(owner: str, repo: str, headers: dict[str, str]) -> int:
        """Deletes repository from GitHub by name and owner"""
        url = f'https://api.github.com/repos/{owner}/{repo}'
        request = requests.delete(url, headers=headers)
        status = request.status_code
        return status


# Fixtures
@pytest.fixture(scope='module')
def env_vars() -> dict[str, str]:
    """Gets and returns variables of environment"""
    load_dotenv()
    data_dict = {
        'token': os.getenv('GITHUB_TOKEN'),
        'owner': os.getenv('GITHUB_OWNER'),
        'repo': os.getenv('REPOSITORY_NAME')
    }
    return data_dict


@pytest.fixture(scope='module')
def request_headers(env_vars: dict[str, str]) -> dict[str, str]:
    """Returns headers for requests"""
    headers = {
        'Accept': 'application/vnd.github.+json',
        'Authorization': f'token {env_vars["token"]}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    return headers


# Tests
class TestGitHubCRUD:
    """Class contains simple test for checking CRUD methods"""

    def test_absence_repository(self, request_headers: dict[str, str], env_vars: dict[str, str]):
        status, result_repo_name = GitHubUser.get_repository(env_vars['owner'], env_vars['repo'], request_headers)
        assert status == 404 and result_repo_name is None, "The repository exists"

    def test_create_repository(self, request_headers: dict[str, str], env_vars: dict[str, str]):
        status, result_repo_name = GitHubUser.create_repository(env_vars['repo'], request_headers)
        assert status == 201 and result_repo_name == env_vars['repo'], "The repository has not been created!"

    def test_delete_repository(self, request_headers: dict[str, str], env_vars: dict[str, str]):
        status = GitHubUser.delete_repository(env_vars['owner'], env_vars['repo'], request_headers)
        assert status == 204, "The repository has not been deleted!"
