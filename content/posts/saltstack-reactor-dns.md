Title: Reacting to Infrastructure Changes with SaltStack Reactor
Date: 2016-06-27 18:52
Category: technical
Author: Jeffrey Moore

### SaltStack

  [SaltStack] \( or Salt\) is a remote execution and configuration management tool that I've been using for a few years.  While other tools like Chef and Puppet might have a bigger userbase (I have no numbers to back up this statement), I appreciated both the completeness of the Salt ecosystem, as well as the fact that it's written in [Python], making it much easier for me to extend.  Configuration is done in Salt using standard YAML, meaning there's a much lower learning curve than some other players in the space that use a custom DSL.
  
### SaltStack Reactor System
  Working on a proof of concept project, I needed some functionality that involved reacting to certain events.  In this particular case, I needed to be able to respond to VMs being created and deleted dynamically (think auto-scaling type behavior) in both our AWS and onsite VMWare environments. 
  
After looking around for several solutions, I settled upon using Salt's [Reactor System].  The key driver for this solution is that since I was using [SaltCloud] to provide a single interface for system provisioning, I didn't want to complicate things by utilizing each platforms own custom events and have to manage my reactions in two places.  Plus, it is a good example of the completeness of the Salt ecosystem.

From the [Reactor System] webpage, it looks like just what I need

>Salt's Reactor system gives Salt the ability to trigger actions in response to an event. It is a simple interface to watching Salt's event bus for event tags that match a given pattern and then running one or more commands in response.

Events in Salt are similar to a RESTful API, except the JSON transfered much like everything else in Salt, along a message queue, and given a tag, rather than a web endpoint.  In fact, you can integrate your own tools in to the Salt Event System using their [REST API](https://docs.saltstack.com/en/latest/topics/event/events.html#remotely-via-the-rest-api) to have your application react to changes in your infrastructure.

### Data Gathering
  It turns out that Salt makes it incredibly easy to do what we're trying to do.  Per [this](https://docs.saltstack.com/en/latest/topics/event/master_events.html#cloud-events) documentation, [SaltCloud] fires off events at various stages of the provisioning and decomissioning process.
  
While watching ```salt-run state.event pretty=True``` in one window to view the event queue, I fired off a provision and destroy action using SaltCloud in another window and found (among others) the two following entries which looked useful.

**salt/cloud/*vm_name*/deploy_script**
> Fired once the deploy script is finished.

```json
salt/cloud/jmtest1/deploy_script	{
    "_stamp": "2016-06-27T03:01:00.529873", 
    "event": "jmtest1 has been deployed at 10.10.51.151", 
    "host": "10.10.51.151", 
    "name": "jmtest1"
}
```
and

**salt/cloud/*vm_name*/destroyed**
> Fired when an instance has been destroyed.

```json
salt/cloud/jmtest1/destroyed	{
    "_stamp": "2016-06-27T03:02:14.852897", 
    "event": "destroyed instance", 
    "name": "jmtest1"
}
```

I chose these two particular events as they were significant points in the provisioning process, and contained all the data (hostname and IP) that I needed.  So now I just had to trap these two events using the Salt Reactor System, then   fire off the reaction I'm interested.  In this case, we'll do something simple... Add the host to DNS when it's created, and remove it from DNS when it's destroyed.

### Implementation
First step is to define the actions to be taken.  We add the following file in to /srv/reactor.

**/srv/reactor/add_dns.sls**

```yaml
add_dns:
    runner.ddns.add_host:
        - name: {{ data['name'] }}
        - zone: 'mydomain.com'
        - ttl: 60
        - ip: {{ data['host'] }}
        - keyname: None
        - keyfile: None
        - nameserver: '10.10.38.250'
```

**/srv/reactor/rem_dns.sls**
 
```yaml
rem_dns:
    runner.ddns.delete_host:
        - name: {{ data['name'] }}
        - zone: 'mydomain.com'
        - keyname: None
        - keyfile: None
        - nameserver: '10.10.38.250'
```

These two files will define our actions using Salt's [Runner System].  As you can see, with the Reactor System, we are given access to the data passed in the event JSON from above.  

_Note: In a production environment, be sure to use a keyfile for security.  Within our lab environment, we allow some rather insecure practices given the nature of the experiments run within it._


 Now that we have our actions defined, we can attach them to the events we defined earlier.
 
 We will create a new file in /etc/salt/master.d pointing to the reactor files we created earlier and restart the salt-master
 
```yaml
 reactor:
    - 'salt/cloud/*/deploy_script':
        - /srv/reactor/add_dns.sls
    - 'salt/cloud/*/destroyed':
        - /srv/reactor/rem_dns.sls
```

### The end result
Once we've restarted our salt-master process, our changes should take effect and we should see a new DNS entry created upon VM creation, and deleted upon VM destruction.

```bash
[root@saltmaster01 ~]# host jmtest1.mydomain.com
Host jmtest1.mydomain.com not found: 3(NXDOMAIN)
[root@saltmaster01 ~]# salt-cloud -p centos7-prod jmtest1
# Output snipped for brevity
[root@saltmaster01 ~]# host jmtest1.mydomain.com
jmtest1.mydomain.com has address 10.10.51.152
[root@saltmaster01 ~]# salt-cloud -d jmtest1
# Output snipped for brevity
[root@saltmaster01 ~]# host jmtest1.red8coe.com
Host jmtest1.mydomain.com not found: 3(NXDOMAIN)
[root@saltmaster01 ~]#
```

**SUCCESS!**

### Conclusion
We can now see the power of Salt's Reactor System.  One can imagine a multitude of use cases surrounding this feature.  

For instance:

* fire an event when your application is installed
* using Salt's [Beacon System], fire events based on load average or when an important file is modified
* utilize open source [plugins](https://github.com/saltstack-formulas/ec2-autoscale-reactor) to react to AWS events
* react to systems being out of desired state
* automatically add a system to DNS, monitoring, inventory control systems upon creation or remove it from the same after destruction
* using Salt's [RESTful API](https://docs.saltstack.com/en/develop/ref/netapi/all/salt.netapi.rest_cherrypy.html), allow your application to send events to your infrastructure

Automation of infrastructure provisioning and deprovisioning is an important part of any dynamic DevOps or Cloud infrastructure, and this is just one tool in a tool chest of many to help accomplish that.

**Questions, comments, improvements, or ideas?**  Please let me know in the comments below!






[SaltStack]:https://saltstack.com
[SaltCloud]:https://docs.saltstack.com/en/latest/topics/cloud/
[Reactor System]:https://docs.saltstack.com/en/latest/topics/reactor/
[Runner System]:https://docs.saltstack.com/en/latest/ref/runners/
[Beacon System]:https://docs.saltstack.com/en/latest/topics/beacons/index.html
[Python]:https://python.org

