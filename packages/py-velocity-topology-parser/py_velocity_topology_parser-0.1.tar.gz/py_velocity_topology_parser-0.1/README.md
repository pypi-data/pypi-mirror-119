# topology_parser_tbml

VelocityTopologyParser can be used to parse the topology from .tbmlfile, string format or .xml file
Supports  python2+ and python3+

You can refer the attached FDK_CFv_FWv_Testing.tbml for supported format

:returns object structure
                 - topology_name
                 - resource_list
                 -resource
                     - property_list
                     - port_list
                     - port_names
                     - property
                         - value
                     - port
                         -value
                         -property
                             -value

## Installation and updating
Use the package manager pip to install VelocityTopologyParser like below. 
Rerun this command to check for and install updates .

pip install py_velocity_topology_parser # python2
python3 -m pip install py_velocity_topology_parser # python3

## Usage

    # parser will pic the tbml file from velocity environ
    velocity = VelocityTopologyParser()
    velocity.parse_topology
    print(velocity.__getattribute__('TG-1').port_list)
    print(velocity.__getattribute__('TG-1').__getattribute__('1/1').property_list)

## Contact
feel free to contact for any issue while using the topology_parser
poornima.wari@spirent.com
support@spirent.com

## License
[MIT]
