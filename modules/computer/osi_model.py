import streamlit as st

def render_osi_tab():
    st.subheader("🌐 OSI Model 7-Layer Encapsulation Simulator")
    st.markdown("Step-by-step simulation of how data travels down through the 7 layers of the OSI model, accumulating headers at each step.")
    
    message = st.text_input("Enter Message to Send (Application Data):", value="Hi")
    
    if not message:
        st.warning("Please enter a message to start the simulation.")
        return

    binary_data = "".join([format(ord(char), '08b') for char in message])

    presentation_data = f"[ASCII Binary: {binary_data}]"

    session_data = f"[Session ID: 7788] -> {presentation_data}"

    st.markdown("### Transport Layer Inputs")
    col1, col2 = st.columns(2)
    with col1:
        src_port = st.number_input("Source Port", value=5000, step=1)
    with col2:
        dst_port = st.number_input("Destination Port", value=80, step=1)
    
    transport_header = f"[Src Port: {src_port} | Dst Port: {dst_port}]"
    transport_segment = f"{transport_header} -> {session_data}"

    st.markdown("### Network Layer Inputs")
    col3, col4 = st.columns(2)
    with col3:
        src_ip = st.text_input("Source IP Address", value="192.168.1.10")
    with col4:
        dst_ip = st.text_input("Destination IP Address", value="192.168.1.50")
        
    network_packet = f"[IP: {src_ip} -> {dst_ip}] -> {transport_segment}"

    st.markdown("### Data Link Layer Inputs")
    col5, col6 = st.columns(2)
    with col5:
        src_mac = st.text_input("Source MAC Address", value="AA:BB:CC:11:22:33")
    with col6:
        dst_mac = st.text_input("Destination MAC Address", value="DD:EE:FF:44:55:66")
        
    data_link_frame = f"[MAC: {src_mac} -> {dst_mac}] -> {network_packet}"

    st.divider()

    layers = [
        "Layer 7: Application",
        "Layer 6: Presentation",
        "Layer 5: Session",
        "Layer 4: Transport",
        "Layer 3: Network",
        "Layer 2: Data Link",
        "Layer 1: Physical"
    ]
    
    selected_layer = st.radio("Select OSI Layer to Inspect:", options=layers, horizontal=False)
    
    st.divider()

    if selected_layer == "Layer 7: Application":
        st.markdown("### Layer 7: Application Layer")
        st.info("The application layer interacts directly with software applications.")
        st.write("**User Message:**")
        st.code(message, language="text")

    elif selected_layer == "Layer 6: Presentation":
        st.markdown("### Layer 6: Presentation Layer")
        st.info("Converts application data into standardized binary format.")
        st.write("**Data including Layer 7 & 6:**")
        st.code(presentation_data, language="text")

    elif selected_layer == "Layer 5: Session":
        st.markdown("### Layer 5: Session Layer")
        st.info("Manages communication sessions and adds control tokens.")
        st.write("**Data including Layer 5 (Session Header):**")
        st.code(session_data, language="text")

    elif selected_layer == "Layer 4: Transport":
        st.markdown("### Layer 4: Transport Layer")
        st.info("Breaks data into segments and adds port numbers (TCP/UDP headers).")
        st.write("**Data including Layer 4 (Transport Segment):**")
        st.code(transport_segment, language="text")

    elif selected_layer == "Layer 3: Network":
        st.markdown("### Layer 3: Network Layer")
        st.info("Adds logical source and destination IP addresses (Packets).")
        st.write("**Data including Layer 3 (Network Packet):**")
        st.code(network_packet, language="text")

    elif selected_layer == "Layer 2: Data Link":
        st.markdown("### Layer 2: Data Link Layer")
        st.info("Adds physical MAC addresses and frames the data.")
        st.write("**Data including Layer 2 (Data Link Frame):**")
        st.code(data_link_frame, language="text")

    elif selected_layer == "Layer 1: Physical":
        st.markdown("### Layer 1: Physical Layer")
        st.info("Converts the complete encapsulated frame into electrical or optical signals.")
        st.write("**Final Frame Ready for Transmission:**")
        st.code(data_link_frame, language="text")
        
        st.write("**Electrical Signal Waveform:**")
        signal_display = " ‾|_|‾ ".join(list(binary_data[:16]))
        st.code(signal_display, language="text")
        st.success("Transmission ready over physical medium!")
