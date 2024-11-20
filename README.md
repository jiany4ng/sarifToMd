# .sarif To .md

Simple python code to convert .sarif into .md


### Example output

# SARIF Summary Report

## Tool: Checkov (Version: 2.0.1000)

### CKV_ANSIBLE_100

Ensure all tasks in Ansible playbook include `become`

- File: playbooks/main.yml, Line: 12

```yaml
- name: Install nginx
  yum:
    name: nginx
    state: present