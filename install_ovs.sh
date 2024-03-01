#!/bin/bash

version=$1

sudo apt-get install -y openvswitch-switch

sudo apt-get remove -y openvswitch-common openvswitch-datapath-dkms openvswitch-pki openvswitch-switch openvswitch-controller

sudo apt-get install -y build-essential fakeroot
sudo apt-get install -y graphviz autoconf automake bzip2 debhelper dh-autoreconf libssl-dev libtool openssl procps python-all python-qt4 python-twisted-conch python-zopeinterface python-s

cd /tmp
wget http://openvswitch.org/releases/openvswitch-$version.tar.gz
tar zxvf openvswitch-$version.tar.gz
cd openvswitch-$version
./configure --prefix=/usr --with-linux=/lib/modules/`uname -r`/build
sudo make
sudo make install
sudo make modules_install

rm -rf /tmp/openvswitch-$version*
sudo service openvswitch-switch restart
sudo ovs-vsctl -V
