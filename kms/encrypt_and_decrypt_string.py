from botocore.exceptions import ClientError
from config.aws_config import get_session


def encrypt_string(kms_client, Text, key_id):
    """
    Encrypts a string using AWS KMS.
    """
    try:
        response = kms_client.encrypt(
            KeyId=key_id,  # Replace with your KMS key alias or ID
            Plaintext=Text.encode('utf-8')
        )
        return response['CiphertextBlob']
    except ClientError as e:
        print(f"❌ Error encrypting string: {e}")
        return None
    
def decrypt_string(kms_client, ciphertext_blob):
    """
    Decrypts a string using AWS KMS.
    """
    try:
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob
        )
        return response['Plaintext'].decode('utf-8')
    except ClientError as e:
        print(f"❌ Error decrypting string: {e}")
        return None
    

if __name__ == "__main__":
    kms_client = get_session().client('kms')
    key_id = 'alias/my_kms_key'  # Replace with your KMS key alias or ID
    text_to_encrypt = "Hello, this is a secret message!"
    print(f"Original text: {text_to_encrypt}")

    encrypted_text = encrypt_string(kms_client, text_to_encrypt, key_id)
    if encrypted_text:
        print(f"Encrypted text: {encrypted_text}")

        decrypted_text = decrypt_string(kms_client, encrypted_text)
        if decrypted_text:
            print(f"Decrypted text: {decrypted_text}")
        else:
            print("Failed to decrypt the text.")
    else:
        print("Failed to encrypt the text.")
