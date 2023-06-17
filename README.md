# SSU
synthetic student transcripts

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
