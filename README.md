# fuzzer-sr2072
** The program will guess any every possible links on a page, and display them, BUT will not follow links that are external or not valid (does not give reponse 200) **


## Getting started

pip3 install MechanicalSoup (added to .yml file)

## Usage 

*Discover*
    For custom-auth (DVWA):
    (the program will assume that if custom is given, it will be ran on dvwa )
        example command: python3 fuzz.py discover http://localhost/ --custom dvwa

    For any other urls: 

        example command: python3 fuzz.py discover http://127.0.0.1/fuzzer-tests/

    Using the common_word: 

        example command: python3 fuzz.py discover http://localhost/fuzzer-tests/ --words common_word.txt

*Test* 
    The only command possible for testing at this time is :
        python3 fuzz.py test http://localhost/fuzzer-tests/ --words common_word.txt --sensitive sensitive.txt
    