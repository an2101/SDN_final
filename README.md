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
**- Google colab, Slide and pdf report:**  Contains report about project (Vietnamese language) and ipynb code.  
Details information project, please access pdf report and video demo.  
Demo video: https://www.youtube.com/watch?v=a9al9RQk7xk

# System requirements
- Ubuntu 22.04.5  
- Installed Mininet and Ryu-manager  
- Virtual python environment 3.8 (Used to run Ryu-manager)
- Install hping3 library  
# Collect data
In desktop, open Terminal and clone source code.  
```bash
git clone https://github.com/an2101/SDN_final.git
```
enable virtual python environment
```bash
source my_env/bin/activate
```
run controller (in virtual python environment)
```bash
cd SDN_final/controller
```
**Collect normal traffic.**  
```bash
ryu-manager collect_benign_trafic.py (in virtual python environment)
```
run mininet (open another terminal in desktop)
```bash
cd SDN_final/mininet
```
```bash
sudo python3 generate_benign_trafic.py
```
**Collect DDoS traffic.**  
```bash
ryu-manager collect_ddos_trafic.py (in virtual python environment)
```
run mininet (open another terminal in desktop)
```bash
cd SDN_final/mininet
```
```bash
sudo python3 generate_ddos_trafic.py
```
In mininet CLI, simulate normal traffic
```bash
h1 ping h2
```
In mininet CLI, simulate DDoS traffic
```bash
h2 hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood h1
```
