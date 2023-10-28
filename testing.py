from bitcoin_transaction_helpers import ECDSA, Bitcoin, Hashes
from transaction import Tx, TxIn, TxOut
from script import Script, p2pkh_script
from format_converter import Converter
from io import BytesIO
from unittest import TestCase



# the elliptical curve bitcoin is using
curve = ECDSA("secp256k1")
bitcoin = Bitcoin()
hash = Hashes()
converter = Converter()


def test_for_p2pkh_transaction():
    private_key_wif = "cTwMnFm86YFcQRqzNUfV1ygpKPU78NUqW8m4t3oqWmeEs1gcfDo1"
    private_key_int = converter.convert_private_key_wif_to_int(private_key_wif)
    version = 1
    tx_id_to_spent = 'ca0bf9d6344c56bac32c0e707eb853d162ee6376b7a5d062754ba205281f69d5'
    tx_index_to_spent = 1
    script_pub_key_to_spent = '76a91488fd87526e486c18b2f232df6cb15109a45e9dac88ac'
    amount_to_spent = 9000
    receiver_address = "mhqPXXnKfzhNUk8DNjSkYhwe81u3PTPDut"
    locktime = 0xffffffff

    transaction_input = TxIn(bytes.fromhex(tx_id_to_spent), tx_index_to_spent)
    script_pubkey_receiver = p2pkh_script(converter.decode_base58(receiver_address))
    transaction_output = TxOut(amount_to_spent, script_pubkey_receiver)
    raw_transaction = Tx(version, [transaction_input], [transaction_output], locktime)
    script_sig = Script().parse(BytesIO(bytes.fromhex(f"{hex(len(script_pub_key_to_spent)//2)[2:]}{script_pub_key_to_spent}")))
    raw_transaction.sign_input(0, private_key_int, script_sig)

    print(raw_transaction.serialize().hex() == "0100000001d5691f2805a24b7562d0a5b77663ee62d153b87e700e2cc3ba564c34d6f90bca010000006a473044022008f4f37e2d8f74e18c1b8fde2374d5f28402fb8ab7fd1cc5b786aa40851a70cb02207d788ef22d22ba7373a3ab2f70cea2475c75fb8bc78a2c4d71fb9d05fd724d3a012103c4f5245042eab9fe9fcd5c575f0dbcb2713b796bf62194dab3c4515ed1f9eec8ffffffff0128230000000000001976a914196ccd42e9392eba4baeccc27046373e9c0e91e388acffffffff")


def main():
    test_for_p2pkh_transaction()


if __name__ == "__main__":
    main()