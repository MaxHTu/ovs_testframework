# ovs_testframework
### Overview
To automatically reproduce and evaluate the vulnerabilities within the packet parsing process of Open vSwitch(OvS), we have developed a Testing Framework. This framework is designed to automate the testing for nine CVEs, to enhance the understanding and mitigation of network vulnerabilities leveraging OvS deployments.

### Disclaimer
To ensure the integrity and safety of operational networks, all testing linked to this framewokr was entirely within our own isolated infrastructure. This work provides open-source access to code that could potentially be used to exploit flaws in different versions of Open vSwitch. It is important to highlight that the purpose of this thesis and the OvS Testing Framework is strictly educational and aimed at supporting research and enhancing security. It is especially not intended for any malicious use, including 
unauthorized testing or causing any network disruptions.

### Requirements
The Testing Framework is mainly developed in Python, supporting versions ranging from 2.7 to 3.x. Due to the nature of the network emulation and the tests, superuser(root) rights are required to run it. Additionally, the framework relies on the following key dependencies: Mininet (tested on the versions 2.2.2 and 2.3.0) and its Python library for network emulation and manipulation, Valgrind for memory debugging and leak detection, and tcpdump for network traffic analysis. Most of the test packets are implemented in C and are compiled using the GNU Compiler Collection (gcc tested on the versions 4.8.4 and 11.4.0).

### Usage
```
sudo python main.py
```
or to install a diffrent OvS version:
```
sudo python main.py -V <version>
```
# openvswitch_version_check
### Overview
This script lists the vulnerabilities for OvS, provides a short description
of each, prints the total count, and calculates the average Common Vulnerability Scoring
System Base Score for the given version.

### Requirements

The script openvswitch_version_check.py requires Python 3.x and the following Python packages:
- `requests`

You can install these packages using pip:

```
pip install requests
```
### Usage

```
python openvswitch_version_check.py
```
