[![Python package](https://github.com/bkoester/SSU/actions/workflows/python-aws.yml/badge.svg)](https://github.com/bkoester/SSU/actions/workflows/python-aws.yml)

# SSU
Synthetic student transcripts, runs on build server from 3.7 up through 3.10 and probably higher, runs on AWS EC2 with Ubuntu image.

# Basics
1. Setup SSH keys
2. Create environment: python -m venv ~/.SSU'''
    - can also make this in CWD, .gitignore will omit ".venv" and similar
3. source ~/.SSU/bin/activate
4. Clone this repo
5. Run Makefile
6. In the python shell
     - `import make_data as md`
     - `std,crse,term = md.create_student_struct(10)`
7. or from command line: python make_data.py 10 '/home/ec2-user/'
