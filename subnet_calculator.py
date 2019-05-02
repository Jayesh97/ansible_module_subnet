DOCUMENTATION = '''
---
module: subnet_calculator

options:
    class_type:
        description:
            - This is the message to send to the sample module
        type: str
        required: True
    network_ip:
        description:
            - Control to demo if the result of this module is changed or not
        type: str
        required: True
    hosts:
        description:
            - Total hosts required in the subnet
        type: str
        required: True
'''

EXAMPLES = '''

name: "subnet module"
    subnet_calculator: 
        class_type: "B"
        network_ip: "172.15.0.0"
        hosts: "1600"


name: "subnet module"
    subnet_calculator: 
        class_type: "C"
        network_ip: "192.168.10.0"
        hosts: "25"



'''

RETURN = '''
start_ip:
    description: The starting IP of 1st subnet
    type: str

end_ip:
    description: The last IP(Broadcast Address) of the 1st subnet
    type: str
'''

from ansible.module_utils.basic import AnsibleModule

def sub_calc():

    module_args = dict(
        class_type=dict(type='str', required=True),
        network_ip=dict(type='str', required=True),
        hosts=dict(type='str', required=True),
    )

    result = dict(
        start_ip='',
        end_ip='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result

    network_ip = module.params['network_ip']
    hosts = module.params['hosts']
    class_type = module.params['class_type']
    l = list()
    l = network_ip.split('.')
    hosts = int(hosts)
    if class_type == 'A':
        if (int(l[0]) <= 127)  & (int(l[1]) == 0) & (int(l[2]) == 0) & (int(l[3]) == 0):
            h = hosts+2
            #Finding nuber of host bits
            for i in range(1,25):
                if(2**i/h > 1):
                    s= i-1
                    break
            n = [x for x in l]
            if(2**s/65536 >=1 ):
                n[1] = int(int(n[1])+2**s/65536)
                n[2] = int(int(n[2])+n[1]*256-2**s/256)
                print(n[1],n[2])
            elif(2**s/256 >= 1):
                n[2] = int(int(n[2])+2**s/256)
                n[3] = int(int(n[3])+255)
            else:
                n[3] = int(int(n[3])+2**s)

            if(2**s/256 >= 256):
                n[3] = int(n[3])+255
                n[2] = int(n[2])+255
                n[1] = int(n[1])-1
            else:
                n[2] = n[2] -1

            l[3] = int(l[3])
            str1 = '.'.join(str(e) for e in l)

            n[3] = int(n[3])
            str2 = '.'.join(str(e) for e in n)

            result['start_ip'] = str1
            result['end_ip'] = str2

            module.exit_json(**result)

        else:
            module.exit_json(**result)
    #If input is a class B
    if class_type == 'B':
        if (int(l[0]) > 127) &  (int(l[0]) < 192) & (int(l[1]) < 256) & (int(l[2]) == 0) & (int(l[3]) == 0):
            h = hosts+2
            #Finding nuber of host bits
            for i in range(1,17):
                if(2**i/h > 1):
                    s= i-1
                    break
            n = [x for x in l]
            if(2**s/256 >= 1):
                n[2] = int(int(n[2])+2**s/256)
            else:
                n[3] = int(int(n[3])+2**s)

            if(2**s >= 256):
                n[3] = int(n[3])+255
                n[2] = int(n[2])-1
            else:
                n[3] = n[3] -1

            l[3] = int(l[3])
            str1 = '.'.join(str(e) for e in l)

            n[3] = int(n[3])
            str2 = '.'.join(str(e) for e in n)

            result['start_ip'] = str1
            result['end_ip'] = str2

            module.exit_json(**result)

        else:
            module.exit_json(**result)
    #If input is a class C
    if class_type == 'C':
        if (int(l[0]) >= 192) &  (int(l[0]) < 223) & (int(l[1]) < 256) & (int(l[2]) < 256) & (int(l[3]) == 0):
            print("hello")
            h = hosts+2
            #Finding nuber of host bits
            for i in range(1,17):
                if(2**i/h > 1):
                    s= i-1
                    break
            n = [x for x in l]
            n[3] = int(int(n[3])+2**s)-1

            l[3] = int(l[3])
            str1 = '.'.join(str(e) for e in l)

            n[3] = int(n[3])
            str2 = '.'.join(str(e) for e in n)

            result['start_ip'] = str1
            result['end_ip'] = str2

            module.exit_json(**result)

        else:
            module.exit_json(**result)
    else:
        module.exit_json(**result)

def main():
    sub_calc()

if __name__ == '__main__':
    main()

