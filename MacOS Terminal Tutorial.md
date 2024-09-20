# MacOS Terminal Tutorial - Self-Study Guide

- Fei Tian Colledge at Middletown NY

---

## Introduction

This tutorial will guide you through basic MacOS terminal commands. We'll use the bash shell and create all example files and folders as we go. Keep a Finder window open alongside your Terminal to see the visual effects of your commands.

---

## Step 1: Switching to Bash (if needed)

```bash
# Check your current shell
echo $SHELL

# If it's not /bin/bash, switch to bash
bash
```

Explanation: The first command shows which shell you're currently using. If it's not bash, the second command switches you to bash for this tutorial.

---

## Step 2: Finding Your Home Directory

```bash
# Print working directory
pwd

# Change to home directory
cd ~

# Print working directory again
pwd

# open finder Window
open .
```

Explanation: `pwd` shows your current location in the file system. `cd ~` takes you to your home directory. After running these commands, you should see your home directory path (like `/Users/yourusername`) in the Terminal. The last command opens current directory, which is your home dir in finder.

---

## Step 3: Understanding Directory Structure

```bash
# List contents of current directory
ls

# List with details
ls -l

# List hidden files too
ls -la
```

Explanation: `ls` lists the contents of the current directory. `-l` shows more details like permissions and dates. `-a` includes hidden files (those starting with a dot). Compare the Terminal output with what you see in Finder. Notice that Finder doesn't show hidden files by default.

---

## Step 4: Creating a Working Directory

```bash
# Create a new directory for this tutorial
mkdir TerminalTutorial

# Move into the new directory
cd TerminalTutorial

# Verify your location
pwd
```

Explanation: `mkdir` creates a new directory. `cd` changes into that directory. You should now see a new 'TerminalTutorial' folder in Finder, and your Terminal should show you're inside this folder.

---

## Step 5: Creating Files

```bash
# Create a text file
echo "Hello, Terminal!" > hello.txt

# Create an empty file
touch emptyfile.txt

# List the contents of the directory
ls -l
```

Explanation: `echo` with `>` creates a file with content. `touch` creates an empty file. You should now see these two new files in both the Terminal output and in Finder.

---

## Step 6: Viewing File Contents

```bash
# View the content of hello.txt
cat hello.txt

# Try to view the content of the empty file
cat emptyfile.txt
```

Explanation: `cat` displays the contents of a file. You should see "Hello, Terminal!" for the first file, and no output for the empty file.

---

## Step 7: Editing Files

```bash
# Append text to hello.txt
echo "This is a new line." >> hello.txt

# View the updated content
cat hello.txt

# Edit the file using nano (a simple text editor)
nano hello.txt
```

Explanation: `>>` appends text to a file. `nano` opens a text editor in the Terminal. In nano, you can add more text, then press Ctrl+X, Y, and Enter to save and exit.

---

## Step 8: Copying and Moving Files

```bash
# Copy hello.txt
cp hello.txt hello_copy.txt

# Move (rename) emptyfile.txt
mv emptyfile.txt renamed_file.txt

# List directory contents
ls -l
```

Explanation: `cp` copies files, `mv` moves or renames them. You should now see `hello_copy.txt` and `renamed_file.txt` in both the Terminal output and Finder.

---

## Step 9: Creating Subdirectories

```bash
# Create a subdirectory
mkdir SubFolder

# Move a file into the subdirectory
mv hello_copy.txt SubFolder/

# List contents of the current directory and subdirectory
ls -R
```

Explanation: This creates a new folder and moves a file into it. `ls -R` lists contents recursively, showing the contents of subdirectories too. Check Finder to see these changes reflected.

---

## Step 10: Navigating Directories

```bash
# Move into the subdirectory
cd SubFolder

# Check your location
pwd

# Move back to the parent directory
cd ..

# Check your location again
pwd
```

Explanation: `cd` changes directories. `..` represents the parent directory. Watch in Finder as you navigate between folders.

---

## Step 11: Deleting Files and Directories

```bash
# Remove a file
rm renamed_file.txt

# Remove the subdirectory and its contents
rm -r SubFolder

# List directory contents
ls -l
```

Explanation: `rm` removes files. `-r` allows it to remove directories and their contents recursively. Be very careful with `rm`, especially with `-r`, as it permanently deletes files and folders. Verify in Finder that these items are gone.

---

## Step 12: Using Wildcards

```bash
# Create some files
touch file1.txt file2.txt file3.doc

# List only .txt files
ls *.txt

# Remove all .txt files
rm *.txt

# List remaining files
ls
```

Explanation: `*` is a wildcard that matches any characters. `*.txt` matches all files ending with .txt. This demonstrates how to work with multiple files at once.

## Final words

You've now learned basic terminal commands for file and directory manipulation. Practice these commands to become more comfortable with the terminal. Remember, the terminal offers powerful tools for file management and system control.


