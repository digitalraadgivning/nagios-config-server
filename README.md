# nagios-config-server
A server side Nagios configuration template for using NSClient++ with RestAPI

## Getting started

1. Install Nagios on a optional Linux distro.
2. Navigate to the Nagios directory and create a plugin directory:

    `cd /usr/local/nagios` (NB: Distro dependent path)

    `mkdir plugins` 

    `cd plugins`
3. Clone the repository: `git clone https://github.com/digitalraadgivning/nagios-config-server`.
4. Navigate to the repository: `cd nagios-config-server`.
5. Make the python script executable `chmod +x check_nsclient.py`
6. Create a file named **nsclient_config.cfg** for the configuration variables: `vim nsclient_config.cfg`.
7. Open the *nsclient_config.cfg* in an editor and paste in the following template:
    ```  
    define command {
            command_name       generic_check_nsclient
            _restport          8443
            _hostpassword      
            _pluginpath        
            _vcenterhost       
            _vcenteruser       
            _vcenterpassword   
    }
    ```
8. Fill out the configuration variables for your environment and save the file. If you don't plan to monitor vmware snapshots or esxi versions you mak leave the *_vcenter** variables blank. Example:
    ```  
    define command {
            command_name       generic_check_nsclient
            _restport          8443
            _hostpassword      secret_pass1
            _pluginpath        /usr/local/nagios/plugins
            _vcenterhost       vcenter.customer.no
            _vcenteruser       readonly@vsphere.local
            _vcenterpassword   secret_pass2
    }
    ```
9. Open the main nagios configuration file: `vim /usr/local/nagios/etc/nagios.cfg` (NB: Distro dependent path)
10. Add the following lines to the part that declares object configuration files:
    ```
    cfg_file=/usr/local/nagios/plugins/nagios-config-server/nsclient_config.cfg
    cfg_file=/usr/local/nagios/plugins/nagios-config-server/nsclient_commands.cfg
    ```
11. Verify the Nagios configuration `/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg` (NB: Distro dependent path)
12. Restart the Nagios Service `service nagios restart` (NB: Distro dependent)

## Examples

TODO

## FAQ:

### How do i add custom commands?

If the new commands are generic and may benifit more than one customer, they should be added to **nsclient_commands.cfg** in the same fasion as the rest, and pushed back to the repository. If not, make a new file for the custom commands named **nsclient_commands_custom.cfg** in the repostory. The file is excluded in the *.gitignore*-file and will not be pushed back or create conflicts.