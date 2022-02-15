# Ansible cron Role

When run against a host, the cron role will configure the cron entries on the host.

This role will do the following:

- Create the /etc/cron.d directory with the proper permissions
- Create /etc/cron.d/local using the template found at templates/etc/cron.d/local.j2

Important options for this role:

- cron_entries: empty by default, allows you to set specific cron entries for a host or group

Syntax: yaml list containing the desired cron entries

- cron_vars: empty by default, allows you to set specific environments for a host or group

This role is enabled by default, and will run if defined in the site_role_list unless specified otherwise in a group or host override.
