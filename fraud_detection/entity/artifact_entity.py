from dataclasses import dataclass
"""
acts like an decorator and create variables for class
"""

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str