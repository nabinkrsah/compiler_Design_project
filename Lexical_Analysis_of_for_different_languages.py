import re
import time
from collections import OrderedDict
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

# Define regex patterns for C++ and C
def make_regex_map(language):
    keywords_c = (
        r"\bauto\b|\bbreak\b|\bcase\b|\bchar\b|\bconst\b|\bcontinue\b|\bdefault\b|\bdo\b|\bdouble\b|\belse\b|"
        r"\benum\b|\bextern\b|\bfloat\b|\bfor\b|\bgoto\b|\bif\b|\bint\b|\blong\b|\bregister\b|\breturn\b|"
        r"\bshort\b|\bsigned\b|\bsizeof\b|\bstatic\b|\bstruct\b|\bswitch\b|\btypedef\b|\bunion\b|\bunsigned\b|"
        r"\bvoid\b|\bvolatile\b|\bwhile\b|\band\b|\bor\b|\bnot\b|\bxor\b"
    )
    
    keywords_cpp = (
        r"\basm\b|\bauto\b|\bbreak\b|\bcase\b|\bcatch\b|\bchar\b|\bclass\b|\bconst\b|\bcontinue\b|"
        r"\bdefault\b|\bdelete\b|\bdo\b|\bdouble\b|\belse\b|\benum\b|\bextern\b|\bfalse\b|\bfloat\b|"
        r"\bfor\b|\bgoto\b|\bif\b|\binline\b|\bint\b|\blong\b|\bmutable\b|\bnamespace\b|\bnew\b|\boperator\b|"
        r"\bprivate\b|\bprotected\b|\bpublic\b|\bregister\b|\breturn\b|\bshort\b|\bsigned\b|\bsizeof\b|"
        r"\bstatic\b|\bstruct\b|\bswitch\b|\btemplate\b|\bthis\b|\bthrow\b|\btrue\b|\btry\b|\btypedef\b|"
        r"\bunion\b|\bunsigned\b|\bvirtual\b|\bvoid\b|\bvolatile\b|\bwhile\b|\band\b|\bor\b|\bnot\b|\bxor\b|"
        r"\bstatic_cast\b"
    )
    
    keywords_java = (
        r"\babstract\b|\bassert\b|\bboolean\b|\bbreak\b|\bbyte\b|\bcase\b|\bcatch\b|\bchar\b|\bclass\b|\bconst\b|"
        r"\bcontinue\b|\bdefault\b|\bdo\b|\bdouble\b|\belse\b|\benum\b|\bextends\b|\bfalse\b|\bfinal\b|\bfinally\b|"
        r"\bfloat\b|\bfor\b|\bgoto\b|\bif\b|\bimplements\b|\bimport\b|\binstanceof\b|\bint\b|\blong\b|\bnative\b|"
        r"\bnew\b|\bnull\b|\bpackage\b|\bprivate\b|\bprotected\b|\bpublic\b|\breturn\b|\bshort\b|\bstatic\b|\bstrictfp\b|"
        r"\bsuper\b|\bswitch\b|\bsychronized\b|\bthis\b|\bthrow\b|\bthrows\b|\btransient\b|\btrue\b|\btry\b|\bvoid\b|\bvolatile\b|\bwhile\b"
    )
    
    keywords_python = (
        r"\bFalse\b|\bNone\b|\bTrue\b|\band\b|\bas\b|\bassert\b|\basync\b|\bawait\b|\bbreak\b|\bclass\b|\bcontinue\b|"
        r"\bdef\b|\bdel\b|\belif\b|\belse\b|\bexcept\b|\bfinally\b|\bfor\b|\bfrom\b|\bglobal\b|\bif\b|\bimport\b|"
        r"\bin\b|\bis\b|\blambda\b|\btry\b|\bwhile\b|\bwith\b|\byield\b"
    )

    constant_patterns = {
        r"\b\d+\b": "Integer Constant",
        r"\b\d+\.\d+\b|\b\d+\.\d*([eE][-+]?\d+)?\b": "Floating Constant",
        r"'[^\\']'": "Character Constant",
        r'"[^"\\]*"': "String Constant",
        r"0[0-7]+": "Octal Constant",
        r"0[xX][0-9a-fA-F]+": "Hexadecimal Constant"
    }

    if language == 'C':
        return {
            r"\".*?\"": "String Literal",
            keywords_c: "Keyword",
            r"#include\b|#define\b|#undef\b|#ifdef\b|#ifndef\b|#if\b|#elif\b|#else\b|#endif\b|#error\b|#warning\b|#pragma\b": "Pre-Processor Directive",
            r"<stdio>|<stdlib>|<string>": "Library",
            r"\+|-|\*|/|%|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>=|=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|--|\+\+|\?|\:": "Operator",
            r"\(|\)|\{|\}|\[|\]|\;|\,|\.|\:\:": "Punctuator",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "Identifier",
            r"\t|\n| ": "Separator",
        }, constant_patterns
    elif language == 'C++':
        return {
            r"\".*?\"": "String Literal",
            keywords_cpp: "Keyword",
            r"#include\b|#define\b|#undef\b|#ifdef\b|#ifndef\b|#if\b|#elif\b|#else\b|#endif\b|#error\b|#warning\b|#pragma\b": "Pre-Processor Directive",
            r"<iostream>|<stdio>|<string>": "Library",
            r"\+|-|\*|/|%|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>=|=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|--|\+\+|\?|\:": "Operator",
            r"\(|\)|\{|\}|\[|\]|\;|\,|\.|\:\:": "Punctuator",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "Identifier",
            r"\t|\n| ": "Separator",
        }, constant_patterns
    elif language == 'Java':
        return {
            r"\".*?\"": "String Literal",
            keywords_java: "Keyword",
            r"\+|-|\*|/|%|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>=|=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|--|\+\+|\?|\:": "Operator",
            r"\(|\)|\{|\}|\[|\]|\;|\,|\.|\:\:": "Punctuator",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "Identifier",
            r"\t|\n| ": "Separator",
        }, constant_patterns
    elif language == 'Python':
        return {
            r"\".*?\"": "String Literal",
            keywords_python: "Keyword",
            r"\+|-|\*|/|%|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>=|=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|--|\+\+|\?|\:": "Operator",
            r"\(|\)|\{|\}|\[|\]|\;|\,|\.|\:\:": "Punctuator",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "Identifier",
            r"\t|\n| ": "Separator",
        }, constant_patterns

def match_language(patterns, constants, text):
    lang_matches = {}
    occupied_positions = set()
    
    # Exclude comments from tokenization
    text_without_comments = re.sub(r"//.*?$|/\*.*?\*/", "", text, flags=re.DOTALL | re.MULTILINE)   

    for pattern, label in patterns.items():
        matches = re.finditer(pattern, text_without_comments)  # Use 'text_without_comments'
        for match in matches:
            token = match.group()
            start_pos = match.start()
            end_pos = match.end()
            
            if any(pos in occupied_positions for pos in range(start_pos, end_pos)):
                continue
            
            lang_matches[start_pos] = (token, label)
            occupied_positions.update(range(start_pos, end_pos))
    
    for pattern, label in constants.items():
        matches = re.finditer(pattern, text_without_comments)  # Use 'text_without_comments'
        for match in matches:
            token = match.group()
            start_pos = match.start()
            end_pos = match.end()
            
            if any(pos in occupied_positions for pos in range(start_pos, end_pos)):
                continue
            
            lang_matches[start_pos] = (token, label)
            occupied_positions.update(range(start_pos, end_pos))

    return OrderedDict(sorted(lang_matches.items()))

def analyze_code():
    text = code_input.get("1.0", tk.END).strip()
    language = language_dropdown.get()
    patterns, constants = make_regex_map(language)
    lang_matches = match_language(patterns, constants, text)
    
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "\tNUMBER".ljust(20) + "TOKEN".ljust(20) + "PATTERN\n")
    output_box.insert(tk.END, "-" * 50 + "\n")
    
    count = 1
    for position, (token, pattern) in lang_matches.items():
        if pattern != "Separator":
            token_info = f"{count:02} | {token.ljust(20)} | {pattern}"
            output_box.insert(tk.END, token_info + "\n")
            count += 1
        time.sleep(0.05)

def toggle_mode():
    if root.cget("bg") == "#ECEFF4":
        root.configure(bg="#2E3440")
        code_input.config(bg="#3B4252", fg="#ECEFF4", insertbackground="white")
        output_box.config(bg="#3B4252", fg="#ECEFF4", insertbackground="white")
        mode_button.config(text="Switch to Light Mode", bg="#81A1C1", activebackground="#5E81AC")
    else:
        root.configure(bg="#ECEFF4")
        code_input.config(bg="#D8DEE9", fg="#2E3440", insertbackground="black")
        output_box.config(bg="#D8DEE9", fg="#2E3440", insertbackground="black")
        mode_button.config(text="Switch to Dark Mode", bg="#5E81AC", activebackground="#81A1C1")

def change_button_color(event):
    submit_button.config(bg="#4C566A")

def reset_button_color(event):
    submit_button.config(bg="#81A1C1")

def clear_output():
    output_box.delete("1.0", tk.END)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                code_input.delete("1.0", tk.END)
                code_input.insert(tk.END, file_content)
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while opening the file: {e}")

# Reset the code input box based on the selected language
def reset_code_box():
    templates = {
    "C++": "#include <iostream>\nint main() {\n    return 0;\n}",
    "C": "#include <stdio.h>\nint main() {\n    return 0;\n}",
    "Java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
    "Python": "def main():\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    main()"
}
    selected_lang = language_dropdown.get()
    code_input.delete("1.0", tk.END)
    code_input.insert(tk.END, templates.get(selected_lang, ""))

# UI setup
root = tk.Tk()
root.title("Lexical Analyzer")
root.geometry("950x800")
root.configure(bg="#ECEFF4")

label_font = ("Arial", 12, "bold")
text_font = ("Courier", 10)
button_font = ("Arial", 12, "bold")

# Language selection dropdown
language_dropdown = tk.StringVar(value="C++")  # Default value
language_menu = tk.OptionMenu(root, language_dropdown, "C++", "C", "Java", "Python", command=lambda _: reset_code_box())
language_menu.grid(row=0, column=0, padx=10, pady=10)

# Label for mentor
mentor_label = tk.Label(root, text="Mentor: Divya K V")  # Create a label with the desired text
mentor_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Place it beside the dropdown

# # Language selection dropdown
# language_dropdown = tk.StringVar(value="C++")
# language_menu = tk.OptionMenu(root, language_dropdown, "C++", "C","Java","Python", command=lambda _: reset_code_box())
# language_menu.grid(row=0, column=0, padx=10, pady=10)

# Code input box
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20, font=text_font)
code_input.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Analyze button
submit_button = tk.Button(root, text="Analyze", font=button_font, bg="#81A1C1", width=10, command=analyze_code)
submit_button.grid(row=2, column=0, padx=10, pady=10)

# Clear button
clear_button = tk.Button(root, text="Clear", font=button_font, bg="#D08770", width=10, command=clear_output)
clear_button.grid(row=2, column=1, padx=10, pady=10)

# Load File button
load_button = tk.Button(root, text="Load File", font=button_font, bg="#A3BE8C", width=10, command=load_file)
load_button.grid(row=2, column=2, padx=10, pady=10)

# Output box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=15, font=text_font)
output_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Mode toggle button
mode_button = tk.Button(root, text="Switch to Dark Mode", font=button_font, bg="#5E81AC", activebackground="#81A1C1", command=toggle_mode)
mode_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
# Set button hover effects
submit_button.bind("<Enter>", change_button_color)
submit_button.bind("<Leave>", reset_button_color)

root.mainloop()

