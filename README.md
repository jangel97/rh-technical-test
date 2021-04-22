next steps


1)- cada role maneje sus dependencias vitales con vars.yml
- hacer README.md y comentar el codigo
- hacer README.md del role

unix:///var/run/docker.sock
dockerd


posibles mejoras:
- firewalld
- si el fichero Dockerfile ha cambiado levantar el nuevo container y tirar abajo el viejo, sujeto a convencion numerica para el nombre
- parametrizar lista de tests, en vez de un unico test ejecutado por el role de test
 

ansible-playbook playbooks/deploy_docker_container.yaml -e playbook_serial=1


prerrequisito:
ansible-galaxy install -r requirements.yml

ansible docker_host -m ping #debe funcionar

si es CentOS para que el pull funcione contra el registry hay que lanzar el siguiente comando:

$ openssl s_client -showcerts -servername registry.access.redhat.com -connect registry.access.redhat.com:443 </dev/null 2>/dev/null | openssl x509 -text > /etc/rhsm/ca/redhat-uep.pem

https://github.com/CentOS/sig-atomic-buildscripts/issues/329

comentarios:
el docker se trata del docker de toda la vida con el socket, se podria haber usado podman... 
- se ha probado con centos 7, rhel 7, fedora 30

- usuario con grupo docker para poder conectarse y levantar el container sin root, se permite usuario ansible
problema centos 7 instalar dependencias => https://github.com/ansible/ansible/issues/67083
