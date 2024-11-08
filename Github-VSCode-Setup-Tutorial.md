## Git Setup and Usage Guide

### Step 0: Creating a new repository on GitHub's website 

1. Log in to your GitHub account.

2. In the upper-right corner of any page, click on the "+" icon, then select "New repository" from the dropdown menu.

3. On the "Create a new repository" page, you'll need to fill out several fields:

   - **Owner**: Use the dropdown menu to select the account where you want to create the repository (your personal account or an organization you belong to).
   
   - **Repository name**: Enter a name for your new repository (e.g. COS243).
   
   - **Description** (optional): Add a short description of your project.
   
   - **Visibility**: Choose whether the repository should be Public or Private.

4. You can initialize your repository with some files:

   - **README file**: Check this box to create an initial README.md file. This is recommended as it provides information about your project.
   
   - **.gitignore file**: If you want GitHub to ignore certain files, select an appropriate template from the dropdown.
   
   - **License**: Choose a license for your project from the dropdown menu.


After creating your repository, you'll be taken to the repository's main page. Here, you can start adding files, inviting collaborators, and setting up your project.

### Step 1: Install Git

#### For Windows:

1. Download Git from [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Run the installer, accepting default options (adjust if needed)
3. During installation, choose:
   - Default editor (e.g., Notepad++ or VS Code)
   - "Git from the command line and also from 3rd-party software" for PATH
   - "Use the native Windows Secure Channel library" for HTTPS transport
   - "Checkout Windows-style, commit Unix-style line endings" for line endings
4. Complete the installation

#### For macOS:
1. Open Terminal and check if Git is installed: `git --version`
2. If not installed:
   - Option A (recommended): Install Homebrew, then run `brew install git`
   - Option B: Download installer from [https://git-scm.com/download/mac](https://git-scm.com/download/mac) and run it

### Step 2: Configure Git

Run in Git Bash (Windows) or Terminal (macOS):
```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

### Step 3: Generate SSH Key

In Git Bash (Windows) or Terminal (macOS):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Press Enter to accept default location and set a passphrase if desired.

### Step 4: Add SSH Key to GitHub

1. Copy the SSH public key:
   - Windows: `cat ~/.ssh/id_ed25519.pub`
   - macOS: `pbcopy < ~/.ssh/id_ed25519.pub`
2. On GitHub: Settings > SSH and GPG keys > New SSH key
3. Paste the key and save

### Step 5: Configure SSH for Specific Repository

1. Edit `~/.ssh/config`:
   ```bash
   nano ~/.ssh/config
   ```
2. Add:
   ```
   Host github
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519
     IdentitiesOnly yes
   ```
3. Save and exit (Ctrl+X, Y, Enter in nano)

### Step 6: Clone Repository

1. On GitHub, copy the SSH URL of your repository
2. In terminal, navigate to desired location and run:
   ```bash
   git clone git@github.com:username/repository.git
   ```
e.g. for my repo COS243 I use:
    ```bash
    git clone  github:quz2004/COS243.git
    ```
3. Update remote URL for the specific config:
   ```bash
   cd ~/projects/COS243
   git remote set-url origin github:quz2004/COS243.git
   ```

### Step 7: Set Up Visual Studio Code

1. Install VS Code from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Open VS Code and install the "Git" extension if not already installed

### Step 8: Using Git in VS Code

1. Open your cloned repository: File > Open Folder
2. Make changes to files
3. In Source Control view (Ctrl+Shift+G on Windows, Cmd+Shift+G on macOS):
   - Stage changes: Click '+' next to modified files
   - Commit: Enter commit message and click checkmark or Ctrl/Cmd+Enter
   - Push: Click "..." and select "Push"
   - Pull: Click "..." and select "Pull"

### Additional Tips

- Windows: Start ssh-agent in Git Bash:
  ```bash
  eval $(ssh-agent -s)
  ssh-add ~/.ssh/id_ed25519
  ```
- macOS: Add SSH key to keychain:
  ```bash
  ssh-add -K ~/.ssh/id_ed25519
  ```
- To verify SSH connection: `ssh -T git@github.com`

