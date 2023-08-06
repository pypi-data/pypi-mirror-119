from typing import Any, Union

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

from .versions.v1 import V1Local, V1Public
from .versions.v2 import V2Local, V2Public
from .versions.v3 import V3Local, V3Public
from .versions.v4 import V4Local, V4Public


class Key:
    @staticmethod
    def new(version: Union[int, str], type: str, key: Union[bytes, str] = b""):

        """
        Constructor of a PASETO key object which has :class:`KeyInterface <pyseto.key_interface.KeyInterface>`.

        Args:
            version(Union[int, str]): The version of the key. It will be ``1``,
                ``2``, ``3`` or ``4``. ``str`` type of version (e.g., ``"v1"``)
                can also be used but it will be DEPRECATED on ``v1.0.0``.
            type (str): The type (purpose) of the key.
            key (Union[bytes, str]): A key itself or keying material.
        Returns:
            KeyInterface: A PASETO key object.
        Raise:
            ValueError: Invalid arguments.
        """
        if isinstance(version, str):
            if version == "v1":
                version = 1
            elif version == "v2":
                version = 2
            elif version == "v3":
                version = 3
            elif version == "v4":
                version = 4
            else:
                raise ValueError(f"Invalid version: {version}.")

        bkey = key if isinstance(key, bytes) else key.encode("utf-8")
        if type == "local":
            if version == 1:
                return V1Local(bkey)
            if version == 2:
                return V2Local(bkey)
            if version == 3:
                return V3Local(bkey)
            if version == 4:
                return V4Local(bkey)
            raise ValueError(f"Invalid version: {version}.")

        elif type == "public":
            k: Any = None
            if bkey.startswith(b"-----BEGIN EC PRIVATE"):
                k = load_pem_private_key(bkey, password=None)
            elif bkey.startswith(b"-----BEGIN PRIVATE"):
                k = load_pem_private_key(bkey, password=None)
            elif bkey.startswith(b"-----BEGIN PUBLIC"):
                k = load_pem_public_key(bkey)
            elif bkey.startswith(b"-----BEGIN RSA PRIVATE"):
                k = load_pem_private_key(bkey, password=None)
            else:
                raise ValueError("Invalid or unsupported PEM format.")
            if version == 1:
                return V1Public(k)
            if version == 2:
                return V2Public(k)
            if version == 3:
                return V3Public(k)
            if version == 4:
                return V4Public(k)
            raise ValueError(f"Invalid version: {version}.")

        raise ValueError(f"Invalid type(purpose): {type}.")

    @staticmethod
    def from_asymmetric_key_params(
        version: Union[int, str], x: bytes = b"", y: bytes = b"", d: bytes = b""
    ):

        """
        Constructor of a PASETO key object which has
        :class:`KeyInterface <pyseto.key_interface.KeyInterface>` wth
        asymmetric key parameters (x-coordinate, y-coordinate, and/or private
        key). This is intended to be used to generate keys for PASETO from JWK
        and other sources.

        Args:
            version(Union[int, str]): The version of the key. It will be ``1``,
                ``2``, ``3`` or ``4``. ``str`` type of version (e.g., ``"v1"``)
                can also be used but it will be DEPRECATED on ``v1.0.0``.
            x (bytes): The x coordinate of the key.
            y (bytes): The y coordinate of the key.
            d (bytes): The private key component of the key.
        Returns:
            KeyInterface: A PASETO key object.
        Raise:
            ValueError: Invalid arguments.
        """
        k: Any = None

        if isinstance(version, str):
            if version == "v1":
                version = 1
            elif version == "v2":
                version = 2
            elif version == "v3":
                version = 3
            elif version == "v4":
                version = 4
            else:
                raise ValueError(f"Invalid version: {version}.")

        if version == 1:
            raise ValueError("v1.public is not supported on from_key_parameters.")

        if version == 2:
            if x and d:
                raise ValueError("Only one of x or d should be set for v2.public.")
            if x:
                try:
                    k = Ed25519PublicKey.from_public_bytes(x)
                except Exception as err:
                    raise ValueError("Failed to load key.") from err
                return V2Public(k)
            if d:
                try:
                    k = Ed25519PrivateKey.from_private_bytes(d)
                except Exception as err:
                    raise ValueError("Failed to load key.") from err
                return V2Public(k)
            raise ValueError("x or d should be set for v2.public.")

        if version == 3:
            if not x or not y:
                raise ValueError("x and y (and d) should be set for v3.public.")
            try:
                pn = ec.EllipticCurvePublicNumbers(
                    x=int.from_bytes(x, byteorder="big"),
                    y=int.from_bytes(y, byteorder="big"),
                    curve=ec.SECP384R1(),
                )
                k = pn.public_key()
            except Exception as err:
                raise ValueError("Failed to load key.") from err

            if not d:
                return V3Public(k)
            try:
                k = ec.EllipticCurvePrivateNumbers(
                    int.from_bytes(d, byteorder="big"), pn
                ).private_key()
            except Exception as err:
                raise ValueError("Failed to load key.") from err
            return V3Public(k)

        if version == 4:
            if x and d:
                raise ValueError("Only one of x or d should be set for v4.public.")
            if x:
                try:
                    k = Ed25519PublicKey.from_public_bytes(x)
                except Exception as err:
                    raise ValueError("Failed to load key.") from err
                return V4Public(k)
            if d:
                try:
                    k = Ed25519PrivateKey.from_private_bytes(d)
                except Exception as err:
                    raise ValueError("Failed to load key.") from err
                return V4Public(k)
            raise ValueError("x or d should be set for v4.public.")

        raise ValueError(f"Invalid version: {version}.")
