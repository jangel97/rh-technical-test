next steps

- assert params al principio y los que no sean obligatorios pues... defaults
- parametriza el dockerfile con ARG
- param everything
- probar con diferentes entornos
- hacer README.md y comentar el codigo
- hacer README.md del role



posibles mejoras:
- firewalld
- si el fichero Dockerfile ha cambiado levantar el nuevo container y tirar abajo el viejo, sujeto a convencion numerica para el nombre
- usuario con grupo docker para poder conectarse y levantar el container sin root
- parametrizar lista de tests, en vez de un unico test ejecutado por el role de test
 

prerrequisito:
ansible-galaxy install -r requirements.yml
ansible docker_host -m ping #debe funcionar
