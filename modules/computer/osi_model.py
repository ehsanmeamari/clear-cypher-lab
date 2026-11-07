import streamlit as st

def render_osi_tab():
    st.subheader("🌐 OSI Model 7-Layer Encapsulation Simulator")
    st.markdown("Step-by-step simulation of how data travels down through the 7 layers of the OSI model.")
    
    # دریافت پیام اولیه از کاربر در تب کاربرد
    message = st.text_input("Enter Message to Send (Application Data):", value="Hi")
    
    if not message:
        st.warning("Please enter a message to start the simulation.")
        return

    binary_data = "".join([format(ord(char), '08b') for char in message])

    # ایجاد تب‌های مجزا برای ۷ لایه
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
        st.info("The application layer interacts directly with software applications to implement a communicating component.")
        st.write(f"**Original User Message:** `{message}`")
        st.text("Protocol examples: HTTP, FTP, SMTP, DNS")

    elif selected_layer == "Layer 6: Presentation":
        st.markdown("### Layer 6: Presentation Layer")
        st.info("Responsible for data formatting, encryption, compression, and translation into binary code.")
        st.write(f"**Data converted to Binary (ASCII):**")
        st.code(binary_data, language="text")

    elif selected_layer == "Layer 5: Session":
        st.markdown("### Layer 5: Session Layer")
        st.info("Manages sessions and dialogs between computers (establishing, managing, and terminating connections).")
        st.code(f"[SESSION_BEGIN] | Data: {binary_data}", language="text")
        st.write("Adds session control tags to the data stream.")

    elif selected_layer == "Layer 4: Transport":
        st.markdown("### Layer 4: Transport Layer")
        st.info("Ensures reliable data transfer, breaking data into segments and adding port numbers.")
        
        col1, col2 = st.columns(2)
        with col1:
            src_port = st.number_input("Source Port", value=5000, step=1)
        with col2:
            dst_port = st.number_input("Destination Port", value=80, step=1)
            
        transport_header = f"[Src Port: {src_port} | Dst Port: {dst_port}]"
        segment = f"{transport_header} -> {binary_data}"
        st.code(segment, language="text")

    elif selected_layer == "Layer 3: Network":
        st.markdown("### Layer 3: Network Layer")
        st.info("Handles routing and logical addressing by adding IP addresses (Packets).")
        
        col1, col2 = st.columns(2)
        with col1:
            src_ip = st.text_input("Source IP Address", value="192.168.1.10")
        with col2:
            dst_ip = st.text_input("Destination IP Address", value="192.168.1.50")
            
        network_packet = f"[IP: {src_ip} -> {dst_ip}] -> [Transport Segment]"
        st.code(network_packet, language="text")

    elif selected_layer == "Layer 2: Data Link":
        st.markdown("### Layer 2: Data Link Layer")
        st.info("Handles physical addressing (MAC addresses) and packages data into frames.")
        
        col1, col2 = st.columns(2)
        with col1:
            src_mac = st.text_input("Source MAC Address", value="AA:BB:CC:11:22:33")
        with col2:
            dst_mac = st.text_input("Destination MAC Address", value="DD:EE:FF:44:55:66")
            
        data_link_frame = f"[MAC: {src_mac} -> {dst_mac}] -> [Network Packet]"
        st.code(data_link_frame, language="text")

    elif selected_layer == "Layer 1: Physical":
        st.markdown("### Layer 1: Physical Layer")
        st.info("Converts the final frame/binary bits into electrical, optical, or radio frequency signals sent over physical media.")
        
        st.write("**Binary Stream to Transmit:**")
        st.code(binary_data, language="text")
        
        st.write("**Electrical Signal Representation (Waveform):**")
        signal_display = " ‾|_|‾ ".join(list(binary_data[:16]))
        st.code(signal_display, language="text")
        st.success("Data transmitted successfully over the physical cable!")
