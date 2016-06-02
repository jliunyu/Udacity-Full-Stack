# Linux Server Configuration

## IP and Port
> The IP address and SSH port so your server can be accessed by the reviewer. 

* IP:   54.187.79.110
* Port: 2200

## URL
> The complete URL to your hosted web application. 

* http://ec2-54-187-79-110.us-west-2.compute.amazonaws.com

## Software and resources
> A summary of software you installed and configuration changes made.

* $ mv ~/Downloads/udacity_key.rsa ~/.ssh/;  
  $ chmod 600 ~/.ssh/udacity_key.rsa;  
  $ ssh -i ~/.ssh/udacity_key.rsa root@52.40.85.24  
  Reference Link: [Udacity](https://www.udacity.com/account#!/development_environment)
* $ sudo apt-get update;  
  $ sudo apt-get upgrade
* sudo adduser grader
* sudo visudo - and then copy "grader  ALL=(ALL:ALL) ALL" under root entry  
  Reference Link: [Digitalocean](https://www.digitalocean.com/community/tutorials/how-to-add-delete-and-grant-sudo-privileges-to-users-on-a-debian-vps)
* vim /etc/ssh/sshd_config; - change port 22 to 2200  
  sudo service ssh restart
* sudo ufw status; sudo ufw default deny incoming; sudo ufw default allow outgoing  
  sudo ufw allow 2200/tcp; sudo ufw allow 123/udp; sudo ufw allow 80/tcp  
  sudo ufw enable
* sudo dpkg-reconfigure tzdata  
  Reference Link: [ask ubuntu](http://askubuntu.com/questions/138423/how-do-i-change-my-timezone-to-utc-gmt)
*

> A list of any third-party resources you made use of to complete this project.
