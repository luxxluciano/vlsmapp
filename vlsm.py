import streamlit as st
import ipaddress
import math

#hide_menu_style = """
#        <style>
#        #MainMenu {visibility: hidden;}
 #       </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)

def create_vlsm():
    # Get the major network IP and mask from the user
    major_network = st.text_input("Enter the major network IP and mask (e.g. 192.168.0.0/16): ")
    try:
        ip = ipaddress.IPv4Network(major_network)
    except ValueError:
        st.error("Enter a valid IP and mask")
        return

    # Create a dictionary to store the subnets and their host requirements
    hosts_per_subnet = {}

    # Get the number of subnets from the user
    num_subnets = int(st.number_input("Enter the number of subnets to create: "))
    if num_subnets <= 0:
        st.error("Please enter a valid number")
        return

    # Get the host requirements for each subnet from the user
    for i in range(num_subnets):
        subnet_name = st.text_input(f"Enter the name of subnet {i+1}: ")
        hosts = int(st.number_input(f"Enter the number of hosts required for {subnet_name}: "))
        if hosts <= 0:
            st.error("Please enter a valid number of hosts")
            return
        hosts_per_subnet[subnet_name] = hosts

    # Create a list to store the subnets
    subnets = []

    # Iterate through the number of hosts per subnet
    for subnet_name, hosts in hosts_per_subnet.items():
        # Calculate the number of required subnets and the prefix length
        num_subnets = (ip.num_addresses / hosts) + 1
        prefix_length = 32 - int(math.log2(num_subnets))

        # Create the subnets
        subnet = next(ip.subnets(new_prefix=prefix_length))
        subnets.append((subnet,subnet_name,subnet.prefixlen))

    # Create a table to display the subnets
    st.table(subnets)

if __name__ == '__main__':
    st.title("VLSM Subnet Calculator")
    create_vlsm()
