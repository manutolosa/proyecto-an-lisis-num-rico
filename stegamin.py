import wave
from itertools import cycle
from pydub import AudioSegment
from scipy.io import wavfile
import scipy.io.wavfile as wav
import numpy as np


# en el venv pip install pydub


def encode(order: list[int], sample_wav, out_wav):
    """
    This function encodes a secret ASCII message from a .wav file

    order: int list that determines which bit was changed when encoding
    sample_wav: input file name
    out_wav: output .wav file name
    """
    audio = wave.open(sample_wav, mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()
    string = input("What message (in ASCII) do you wish to hide? ")
    print(string)
    # string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * "##"
    string += "ÿÿ"
    bits = list(
        map(int, "".join([bin(ord(i)).lstrip("0b").rjust(8, "0") for i in string]))
    )
    order_bit = cycle(order)
    for i, bit in enumerate(bits):
        offset = 2 ** (order_bit.__next__())
        frame_bytes[i] = (frame_bytes[i] & (255 - offset)) | bit * (offset)
        # print(f"(frame_bytes[i] & 255 - {255 - offset:b}) | {bit * (offset):b}")
    frame_modified = bytes(frame_bytes)

    newAudio = wave.open(out_wav, "wb")
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified)

    newAudio.close()
    # encrypt_audio(out_wav, encryption_matrix=em)


def decode(order: list[int], out_wav: str):
    """
    This function extracts a secret message from a wav file

    order: list of integers that determine which bit of each sample is to be modified, the list is repeated until the message is finished
    out_wav: .wav file name
    """
    # decrypt_audio(out_wav,decryption_matrix=dm)
    audio = wave.open(out_wav, mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    # extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    n_extracted = [0] * len(frame_bytes)
    order_bit = cycle(order)
    # n_extracted = [
    #    (frame_bytes[i] >> order_bit.__next__()) & 1 for i in range(len(frame_bytes))
    # ]
    decoded = []
    for i in range(len(frame_bytes)):
        n_extracted[i] = (frame_bytes[i] >> order_bit.__next__()) & 1
        if i > 0 and i % 8 == 0:
            bin_list = n_extracted[i - 8 : i]
            decoded_string_byte = "".join(map(str, bin_list))
            bin_int = int(decoded_string_byte, 2)
            decoded_char = chr(bin_int)
            decoded.append(decoded_char)
            if decoded_char == "ÿ":
                break

    # string = "".join(
    #    chr(int("".join(map(str, n_extracted[i : i + 8])), 2))
    #    for i in range(0, len(n_extracted), 8)
    # )
    msg = "".join(decoded)
    decoded = msg.split("ÿ")[0]
    print("Sucessfully decoded: " + decoded)
    audio.close()


def convert_mp3_to_wav(mp3_path: str, wav_path: str):
    """
    Utility function to convert a mp3 file to wav

    mp3_path: file name to the file to be converted
    wav_path: name of the wav file that will be created
    """
    # Load the MP3 file using pydub
    audio = AudioSegment.from_mp3(mp3_path)

    # Export the audio as WAV file
    audio.export(wav_path, format="wav")

    print("MP3 to WAV conversion completed successfully.")
    return wav_path


def noise_tests(original_file: str, lsb_file: str):
    """
    Utility function to check the MSE and PSNR values of a wav file that
    had LSB applied, relative to its original.
    """

    sample_rate_original, audio_data_original = wavfile.read(original_file)
    sample_rate_lsb, audio_data_lsb = wavfile.read(lsb_file)

    mse = np.mean((audio_data_original - audio_data_lsb) ** 2)
    print(f"MSE is: {mse}")

    max_value = np.max(audio_data_original)
    psnr = 20 * np.log10(max_value / np.sqrt(mse))
    print(f"PSNR is {psnr}")



"""
def encrypt_audio(audio_path, encryption_matrix):
    # Cargar el archivo de audio
    sample_rate, audio_data = wav.read(audio_path)

    # Convertir el audio en una matriz
    audio_matrix = np.array(audio_data, dtype=np.int32)

    # Asegurar que la matriz de encriptación tenga una forma compatible
    if encryption_matrix.shape[1] != audio_matrix.shape[1]:
        encryption_matrix = np.resize(encryption_matrix, audio_matrix.shape)

    # Multiplicar la matriz de encriptación por la matriz de audio
    encrypted_matrix = np.matmul(encryption_matrix, audio_matrix.T).T

    # Generar el archivo de audio encriptado
    encrypted_audio = encrypted_matrix.astype(np.int16)
    wav.write(f"en{audio_path}", sample_rate, encrypted_audio)

def decrypt_audio(encrypted_audio_path, decryption_matrix):
    # Cargar el archivo de audio encriptado
    sample_rate, encrypted_audio_data = wav.read(encrypted_audio_path)

    # Convertir el audio encriptado en una matriz
    encrypted_audio_matrix = np.array(encrypted_audio_data, dtype=np.int32)

    # Asegurar que la matriz de desencriptación tenga una forma compatible
    if decryption_matrix.shape[1] != encrypted_audio_matrix.shape[1]:
        decryption_matrix = np.resize(decryption_matrix, encrypted_audio_matrix.shape)

    # Multiplicar la matriz de desencriptación por la matriz de audio encriptado
    decrypted_matrix = np.matmul(decryption_matrix, encrypted_audio_matrix.T).T

    # Generar el archivo de audio desencriptado
    decrypted_audio = decrypted_matrix.astype(np.int16)
    wav.write(f"des{encrypted_audio_path}", sample_rate, decrypted_audio)
    
# Ejemplo de uso
# Definir una matriz de encriptación y su inversa para desencriptar
encryption_matrix = np.array([[2, 1], [1, 2]])
decryption_matrix = np.linalg.inv(encryption_matrix)
"""

if input("Do you wish to use the default order?[Y/n] ").lower() == "y":
    order = [0, 0, 0, 2, 1, 2, 3, 1, 4, 0]
else:
    with open(input("name of order_file(exclude .txt)")+".txt", "r") as of:
        order = list(map(int, map(lambda s: s.split("\n")[0], of.readlines())))
    for i, v in enumerate(order):
        if not (0<= v<= 7):
            raise ValueError(f"Please do not attempt to modify bit number {v} as specified on line {i+1}")

while 1:
    print("\nSelect an option: \n1)Encode\n2)Decode\n3)Noise tests\n4)exit")
    choice = int(input("\nChoice:"))
    if choice == 1:
        print(
            "\nPlease Provide the file names from the file to be used as input and the output file to be created"
        )
        sample_wav = input("Name of input .wav file (exclude .wav): ") + ".wav"
        out_wav = input("Name of steganography output .wav file (exclude .wav): ") + ".wav"
        encode(order, sample_wav, out_wav)
    elif choice == 2:
        out_wav = input("Name of steganography .wav file (exclude .wav): ") + ".wav"
        decode(order, out_wav)
    elif choice == 3:
        wav = input("Name of original .wav file (exclude .wav): ") + ".wav"
        lsb = input("Name of lsb .wav file (exclude .wav): ") + ".wav"
        noise_tests(wav, lsb)
    elif choice == 4:
        break
    elif choice == 5:
        mp3 = input("Name of input .mp3 file (exclude .mp3): ") + ".mp3"
        out_wav = input("Name of .wav file (exclude .wav): ") + ".wav"
        convert_mp3_to_wav(mp3, out_wav)
    else:
        print("\Please enter valid choice")
