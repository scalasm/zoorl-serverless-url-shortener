from abc import ABC, abstractmethod
from typing import Any, Optional

import boto3
import os

class ShortenedUrlModel:
    """Data model for Shortened URLs"""
    def __init__(self, long_url: str, alias: str, ttl: int) -> None:
        self.long_url = long_url
        self.alias = alias
        self.ttl = ttl

class ApplicationException(Exception):
    """Base class for all application exception"""
    pass

class ShortenedUrlRepository(ABC):
    """Interface for repository implementations"""
    @abstractmethod
    def save(self, shortened_url: ShortenedUrlModel) -> None:
        """Save the model to database
        
        Args:
            shortened_url: the model to save
        """
        pass

    @abstractmethod
    def get_by_alias(self, alias: str) -> Optional[str]:
        """Returns the long url associated, if present
                
        Args:
            alias: the model to save
        
        Returns:
            the long URL associated to that alias or None if not present
        """
        pass

class RepositoryException(ApplicationException):
    """Exception throws because of the errors in the repository layer"""
    pass


class TTLBoundaries:
    def __init__(self, lower_bound: int, upper_bound: int) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

class ApplicationConfig:
    """Well-known configuration options for the URL Shortener service"""
    def __init__(self) -> None:
        self.__dynamodb_client = None
        self.__urls_table = None
        self.ttl_boundaries = TTLBoundaries(1, 30)

    def get_env(self, env_var: str, default_value: str = None) -> str:
        """Returns the value of an OS environment variable or a default value if not present

        Args:
            env_var: the name of the environment variable
            default_value: the default value if there is no such variable name
        Returns:
            a string with the env var (or its specified default value)
        """
        return os.environ.get(env_var, default_value)

    @property
    def dynamodb_client(self) -> Any:
        """Returns the AWS DynamoDB client (lazily created and then cached)"""
        if not self.__dynamodb_client:
            self.__dynamodb_client = boto3.resource("dynamodb")
        return self.__dynamodb_client

    @property
    def urls_table(self) -> Any:
        """Returns the DynamoDB table for mapping URLs and aliases (lazily created and then cached)"""
        if not self.__urls_table:
            table_name = self.get_env("URLS_TABLE")
            self.__urls_table = self.dynamodb_client.Table(table_name)
        return self.__urls_table

    @property
    def valid_ttl_boundaries(self) -> range:
        """Returns the limits for the TTL, namely one day minimum and 30 days top.
        
        Returns:
            a range that can be used for checking boundary conditions
        """
        return range(self.ttl_boundaries.lower_bound, self.ttl_boundaries.upper_bound)