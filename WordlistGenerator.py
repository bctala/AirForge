import itertools
import random
import pyfiglet
import os
from termcolor import colored

def generate_passwords(keywords, num):
    special_chars = "!@#$%^&*()_+-="
    common_weak_passwords = ["password", "qwerty", "admin", "welcome", "123456", "letmein", "iloveyou"]
    common_patterns = [
        "{first}{dob}{char}", "{first}_{dob}", "{first}{dob}", "{dob}{first}", "{char}{first}{dob}",
        "{first}{dob}{char}{num}", "{first}_{dob}{num}", "{first}{dob}{num}", "{dob}{first}{char}",
        "{last}{dob}{char}", "{last}_{dob}", "{last}{dob}", "{dob}{last}", "{char}{last}{dob}",
        "{first}{last}{dob}", "{first}_{last}{dob}{num}", "{first}{last}{dob}{char}", "{dob}{first}{last}",
        "{first}{num}{char}", "{last}{num}{char}", "{first}{last}{char}{dob}", "{dob}_{first}{char}",
        "{dob}{char}{first}", "{first}{char}{num}", "{first}{first}{num}{char}", "{last}{last}{dob}{char}"
    ]
    generated = set()

    # Add exact keywords to the wordlist
    for keyword in keywords:
        generated.add(keyword.strip())

    while len(generated) < num:
        first, last, dob = "", "", ""
        
        for kw in keywords:
            if kw.isdigit() and len(kw) == 4:  
                dob = kw
            elif kw.istitle():  
                if not first:
                    first = kw
                else:
                    last = kw
            elif not last:  
                last = kw
        
        if not dob:
            dob = str(random.randint(1970, 2010))  
        
        if not first:
            first = "user"  
        if not last:
            last = "default" 
        
        num_suffix = random.randint(10, 99)
        char = random.choice(special_chars)
        pattern = random.choice(common_patterns)
        password = pattern.format(first=first, last=last, dob=dob, num=num_suffix, char=char)
        
        if random.random() < 0.2:
            password = password.capitalize()
        if random.random() < 0.1:
            password = password[::-1]  
        
        if random.random() < 0.15:
            password += random.choice(common_weak_passwords)
        
        generated.add(password)
    
    return list(generated)[:num] 

def save_to_file(words, filename):
    with open(filename, "w") as file:
        for word in words:
            file.write(word + "\n")
    print(colored(f"[+] Wordlist saved to {filename}", "green"))

def main():
    os.system("clear")  
    giraffe_ascii = """
           A--A
       .-./   #\.-.
      '--;d    b;--'
         \# \/  /
          |'--'/
           |==|
           | #|
           |# |
          /   #'
         ;   #  ;
         | #    |
        /|  ,, #| '
       /#|  ||  | 
   .-.'  |# ||  |# '.-.
  (.=.),'|  ||# |',(.=.)
   '-'  /  #)(   \  '-'
        `""`  `""`
    
    """
    print(colored(giraffe_ascii, "yellow"))
    print(colored(pyfiglet.figlet_format("Wordlist Gen"), "red"))
    print(colored("Welcome to the Ultimate Custom Wordlist Generator", "yellow"))
    print(colored("🔍 This tool generates wordlists based on common password patterns and user-defined keywords!", "yellow"))
    
    keywords = input(colored("[?] Enter keywords (comma-separated): ", "blue")).strip().split(",")
    keywords = [kw.strip() for kw in keywords if kw.strip()]
    
    if not keywords:
        print(colored("[!] No keywords provided. Exiting...", "red"))
        return
    
    try:
        num = int(input(colored("[?] How many passwords do you want to generate? ", "blue")))
    except ValueError:
        print(colored("[!] Invalid input. Please enter a numeric value.", "red"))
        return
    
    wordlist = generate_passwords(keywords, num)
    filename = "passwords_wordlist.txt"
    
    save_to_file(wordlist, filename)
    print(colored("[+] Wordlist generation complete!", "green"))

if __name__ == "__main__":
    main()
