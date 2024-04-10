from setuptools import setup, find_packages

setup(
    name="MCQ_generator", 
    version=0.01,
    author="shivam",
    install_requires=["OpenAi", "langchain", "streamlit", "pyPDF2", "python-dotenv"],
    packages=find_packages()
)