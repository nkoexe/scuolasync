import base64
import ecdsa


def generate_vapid_keys():
    public_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    private_key = public_key.get_verifying_key()

    return {
        "private_key": base64.urlsafe_b64encode(public_key.to_string()).strip(b"="),
        "public_key": base64.urlsafe_b64encode(b"\x04" + private_key.to_string()).strip(b"="),
    }
