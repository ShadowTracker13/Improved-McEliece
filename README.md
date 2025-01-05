#McEliece Cryptosystem
This project provides a simple and understandable Python implementation of the McEliece cryptosystem and the associated Goppa Code. It is intended primarily for students and others who have read theoretical papers and want a practical visualization or implementation of this cryptosystem.

#New Feature: Alphabet Support
This modified version of the McEliece cryptosystem extends its functionality to encrypt and decrypt messages containing alphabets, in addition to numerical data. This enhancement makes the implementation more versatile and easier to use for textual data.

Usage
You can set up the cryptosystem by initializing a new instance of the McEliece class with the parameters of your choosing. This instance acts as a single deployment of the system, providing methods to:

Generate new sets of private and public keys
Encrypt messages (including alphabets) with a public key
Decrypt ciphertext with a private key

#Explanation
The implementation uses the galois library for operations in finite fields. For those curious about the inner workings of the methods, the library's documentation is an excellent resource.

The project revolves around the mceliece.py file. You initialize the cryptosystem with parameters $[m, t]$, where:

$n$ is implicitly set as $2^m$
$k$ is computed as the minimal possible value given $[m, t]$.
The used Goppa Code and the Patterson algorithm are implemented in the goppa_code.py file. This version uses a visual matrix implementation instead of the faster polynomial approach discussed in Bernstein's paper.

Additionally, the text encoding and decoding logic for alphabet support is included in the text_encoder.py file. This module handles the conversion of text (letters and numbers) to numerical representations compatible with the McEliece encryption process.

#Sources
This implementation builds upon the foundational work of the McEliece cryptosystem. It was inspired by:

This GitHub repository
This Syracuse University paper
Bernstein's paper on Goppa Codes and the Patterson Algorithm
This thesis

#Disclaimer
This project was developed as part of my bachelor project . While I am open to feedback and will work to address any bugs, future feature updates are not currently planned.