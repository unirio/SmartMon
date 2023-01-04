#!/usr/bin/env bash
cd /home/sdn/onos
ONOS_APPS=drivers.bmv2,proxyarp,lldpprovider,hostprovider,fwd,gui,inbandtelemetry bazel run onos-local -- clean
