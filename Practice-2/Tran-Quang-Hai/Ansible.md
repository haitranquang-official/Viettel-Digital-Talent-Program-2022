# **PRACTICE 2: Ansible**

## **TASK**: Deploy a project with Ansible

*Since this homework is about practicing Ansible, I will use a public Docker repository to alleviate the headache*

Here is the docker repository on hub.docker.com
<br></br>
<img src="imgs/1-Docker image.png">

### **Step 1: Create an inventory file**

```
[personal]
159.89.203.89
```
To avoid showing plaintext password in inventory file, do step 1.1
### **Step 1.1**: Create a public SSH key and add it to the VM

#### **Step 1.1.1**: Generate a public key

First, we change our directory to ~/.ssh

```
cd ~/.ssh
```
Run the following command to generate a key
```
ssh-keygen -t rsa
```
You will have to fill several questions
<img src="imgs/2-Generate SSH key.png">
*Don't capture and show the screenshot as I did here*

Next, we copy the generated .pub file to the remote server with the following command:
```
ssh-copy-id -i <file_name>.pub <remote_user>@<remote_server>
```
Type in the password as usual, but from now on you won't have to type the password again while trying to SSH to the remote server. To finalize and make the SSH context persistent between sessions, add those 2 lines into ~/.bashrc file
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/<file_name_only>
```

### **Step 2: Install Docker on remote hosts**

To run a docker image, of course we would have to install docker first. For reference to the manual steps, here is the [URL (DigitalOcean tutorial on installing Docker)](https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-install-and-set-up-docker-on-ubuntu-20-04)
<br>

From there, we know that there are 3 mandatory steps to install docker, which are:
### **Step 2.1**: Installing required packages

```
sudo apt update | sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

Translating it to ansible playbook, we have a task:

```
  - name: Install required packages
    apt:
    pkg:
    - apt-transport-https 
    - ca-certificates 
    - curl 
    - software-properties-common
    - python3-pip
    update_cache: true
```
### **Step 2.2**: Add Docker GPG key
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
Ansible corresponding task:
```
  - name: Add Docker GPG key
    apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present
```
### **Step 2.3**: Update apt and install docker-ce
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" |
sudo apt install docker-ce
```
Ansible corresponding task:
```
  - name: Update apt and install docker-ce 
    apt:
    name: docker-ce
    state: latest
    update_cache: true
```
Finally, to check docker service status and run docker without sudo, run the command:
```
sudo systemctl status docker | sudo usermod -aG docker ${USER}
```
Translating to ansible (with become:true):
```
- name: Show docker info
    command:
    cmd: systemctl status docker
    register: shell_result
- debug:
    var: shell_result.stdout_lines
- name: Run docker without sudo 
    shell: |
    usermod -aG docker root 
```
Output of the debug command in playbook file:
<img src="imgs/3-Docker status.png">

FINAL VERSION OF THE PLAYBOOK:
```
- hosts: all
  become: true
  tasks:
    - name: Install required packages
      apt:
        pkg:
        - apt-transport-https 
        - ca-certificates 
        - curl 
        - software-properties-common
        - python3-pip
        update_cache: true
    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present
    - name: Update apt and install docker-ce 
      apt:
        name: docker-ce
        state: latest
        update_cache: true
    - name: Show docker info
      command:
        cmd: systemctl status docker
      register: shell_result
    - debug:
        var: shell_result.stdout_lines
    - name: Run docker without sudo 
      shell: |
        usermod -aG docker root 

```