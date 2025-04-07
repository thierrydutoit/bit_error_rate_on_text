import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Utility functions ---
def text_to_bits(text):
    ascii_vals = [format(ord(c), '07b') for c in text]  # 7-bit ASCII
    bits = [int(b) for char in ascii_vals for b in char]  # flatten
    return bits

def introduce_errors(bits, ber):
    bits = np.array(bits)
    n = len(bits)
    error_mask = np.random.rand(n) < ber
    flipped_bits = np.bitwise_xor(bits, error_mask.astype(int))
    return flipped_bits.tolist()

def bits_to_text(bits):
    bits = bits[:len(bits) - len(bits)%7]  # ensure multiple of 7
    chars = [''.join(str(b) for b in bits[i:i+7]) for i in range(0, len(bits), 7)]
    text = ''.join([chr(int(char, 2)) for char in chars])
    return text

st.title("Binary Transmission Error Simulator")
st.markdown('''What is the actual effect of a given bit error rate on text? \\
               In this application, text is encoded as 7-bit ASCII characters and 
               the resulting bit sequence is artificially scrambled with a given bit 
               error rate (BER).''')

col1, col2 = st.columns(2)

ber = st.slider("Bit Error Rate (BER)", 0.0, 0.1, 0.001, 0.001, format="%0.3f")

with col1:
   st.subheader("Emitted message:")
   message = st.text_area("Enter your message:", "Binary Transmission Error Simulator")
   bits = text_to_bits(message)     
   

with col2:
   st.subheader("Received message:")
   st.write(f"Number of bits: {len(bits)}")
       
   bits_with_errors = introduce_errors(bits, ber)
   reconstructed_message = bits_to_text(bits_with_errors)
      
   st.text(reconstructed_message)

   fig,ax = plt.subplots(figsize=(10,4))

   plt.xlim(1, len(bits))
   plt.ylim(-0.1, 1.1)    
   ax.plot(np.arange(len(bits)),bits, label="Emitted bits")
   ax.plot(np.arange(len(bits)),bits_with_errors, label="Received bits")
   ax.set_xlabel("Index")
   ax.set_ylabel("Value")
   ax.legend()
   st.pyplot(fig)

with st.expander("Open for comments"):
   st.markdown('''Obviously, a BER of 0.01 or lower makes transmision errors acceptable
                  to the eye. \\
                  Notice that, in practice, error correction codes can be added to 
                  encoded bits, to detect and correct such transmission errors.''')
