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
**Details information project, please access pdf report and video demo.**  
**Demo video: https://www.youtube.com/watch?v=a9al9RQk7xk**

# System requirements
- Ubuntu 22.04.5  
- Installed Mininet and Ryu-manager  
- Virtual python environment 3.8 (Used to run Ryu-manager)
- Install hping3 library
# Download project
In desktop, open Terminal and clone source code.  
```bash
git clone https://github.com/an2101/SDN_final.git
```
# Collect data
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
ryu-manager collect_benign_trafic.py
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
ryu-manager collect_ddos_trafic.py
```
run mininet (open another terminal in desktop)
```bash
cd SDN_final/mininet
```
```bash
sudo python3 generate_ddos_trafic.py
```
After collect (take about 2 days), file FlowStatsfile.csv will be create. **Remember move FlowStatsfile.csv inside controller Folder.**  
Link dataset: https://drive.google.com/file/d/13VJCkPponpPnL-H0myPteMwE9U3qpDz3/view  
# Train model
There are two way to train model: in Google Colab (source code in sdn_data.ipynb) or run directly on your computer. This will take about 6 minutes.  
```bash
ryu-manager MLP-controller.py
```
After train model, file mlp_model_detech.pkl will be create. **Remember move mlp_model_detech.pkl inside controller Folder.** 
# Simulation SDN topology and Detect and Mitigate DDoS Attacks Using Deep Learning
Run Ryu-manager (open Terminal in Desktop)  
```bash
source my_env/bin/activate
```
run controller (in virtual python environment)
```bash
cd SDN_final/controller
```
```bash
ryu-manager MLP-controller.py
```
Run Mininet (open another terminal in desktop)
```bash
cd SDN_final/mininet
```
```bash
sudo python3 topology.py
```
In mininet CLI, open xterm (example open h2 and h3).
```bash
mininet> xterm h2 h3
```
Simulate normal traffic in xterm CLI (example h2 ping to h1):
```bash
ping 10.0.0.1
```
Simulate icmp flood in xterm CLI (example h3 sent to h1):
```bash
hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.1
```
Simulate syn flood in xterm CLI (example h3 sent to h1):
```bash
hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.1
```
Simulate udp flood in xterm CLI (example h3 sent to h1):
```bash
hping3 -2 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.1
```
Open wireshark (another Terminal)
```bash
sudo wireshark
```
Then choose s1-eth1 to view the packet.
