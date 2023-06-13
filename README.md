# README #

This automated Prometheus installation consists of 4 parts:

	• Blackbox exporter
	• Alertmanager
	• Grafana server
	• Prometheus server

Blackbox exporter is used to perform status checks: 

	• test for ssh service accessibility
	• test for host availability

Alertmanager is used for notifications.

Grafana visualizes data provided by Prometheus.

Prometheus server gathers data about the system.

To install Prometheus you will need to add two groups in your inventory: 

	• prom_nodes
	• prom_servers

In prom_nodes you should include all nodes you want to monitor (including server, if you want to monitor it)

In prom_severs you should include the server (or multiple severs)

To install prometheus you will need to:

	• add nodes and servers to respective groups in your inventory 
	• run prometheus_node role to install node-exporter on all nodes
	• run the prometheus_server role, which will install prometheus sever and auto-generate dashboards for every node included in prom_nodes

To update configuration on prometheus sever, if you want to add/remove prometheus nodes you will need to:

	• Add/remove node from the prom_nodes group
	• Run prometheus_server playbook with tags: "prometheus_server_update_config, grafana_server_update_config"

The Prometheus role includes all four roles, which install blackbox manager, alertmanager, grafana server and prometheus server.
