# Detecting and Mitigating DDoS Attacks Using Deep Learning in SDN Networks  
**This is project in Software Defined Networking course**. 
| ID   | Student    | Class    |
|:-------:|:-------:|--------|
|106210045      | Nguyễn Văn An| 21KTMT       |
|106210050      | Phạm Thị Phương| 21KTMT       |
|106210259      | Dương Thị Thảo Vi| 21KTMT2       |

Our group in Danang University of Science and Technology.  
**Directory Structure:**  
**- controller:** Contains Ryu-manager simulation about collect data (collect_benign_trafic.py, collect_ddos_trafic.py) and main Controller (MLP-controller.py) and deep-learning model checkpoint (mlp_model_detech.pkl).  
**- mininet:** Contains mininet simulation: include collect data normal traffic (generate_benign_trafic.py), DDoS traffic (generate_ddos_trafic.py) and main SDN topology (topology.py).  
**- README.md:** Contains introduction and instructions project.  
**- Slide and pdf report:**  Contains report about project (Vietnamese language).  
Details information midterm project, please access in Folder "Document/Slide_RTOS_midterm_report.pptx"  
Demo video: https://drive.google.com/file/d/1uJZdLKMzb7t7uUvIZkhNDOHja9ycd7Sn/view?usp=drive_link    

# System requirements
- Ubuntu 22.04.5  
- Installed Mininet and Ryu-manager  
- Virtual python environment 3.8 (Used to run Ryu-manager)
- Install hping3 library  
# Collect data
creat virtual python environment
```bash
git clone https://github.com/an2101/testsdn.git
```
creat virtual python environment
```bash
source my_env/bin/activate
```
run controller (in virtual python environment)
```bash
cd testsdn/Controller_Deep
```
```bash
ryu-manager MLP-controller.py
```
run mininet (open another terminal in desktop)
```bash
cd testsdn/mininet
```
```bash
sudo python3 topology.py
```
In mininet CLI, simulate normal traffic
```bash
h1 ping h2
```
In mininet CLI, simulate DDoS traffic
```bash
h2 hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood h1
```
