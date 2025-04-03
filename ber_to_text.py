import streamlit as st
import numpy as np

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

# --- Streamlit Interface ---
st.title("Binary Transmission Error Simulator")

# Step 1: Text input
message = st.text_area("Enter your message:", "Audio watermarking: this message will be embedded in an audio signal, using spread spectrum modulation, and later retrieved from the modulated signal.")

if message:
    bits = text_to_bits(message)
    st.write(f"Number of bits: {len(bits)}")
    st.text(f"Original bits (preview): {bits[:50]} ...")

    # Step 2: BER Slider
    ber = st.slider("Bit Error Rate (BER)", 0.0, 0.1, 0.001, 0.001, format="%0.3f")
    bits_with_errors = introduce_errors(bits, ber)
    st.text(f"Modified bits (preview): {bits_with_errors[:50]} ...")

    # Step 3: Reconstruction
    reconstructed_message = bits_to_text(bits_with_errors)
    st.subheader("Reconstructed message:")
    st.text(reconstructed_message)
