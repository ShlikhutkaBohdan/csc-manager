from sys import argv, exit
from pybitcoin import BitcoinPrivateKey, LitecoinPrivateKey
# import pywaves as pw
from cashaddress import convert

# for ethereum wallets
from ecdsa import SigningKey, SECP256k1
import sha3
import codecs


# for monero wallet
#from moneropy import account

class DashPublicKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 0x4c


class ClubCoinPublicKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 0x1c

class PotCoinPublicKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 0x37

class CryptoCoin:
    address = ''
    wif = ''
    seed = ''

    def __init__(self, address, wif, seed=''):
        self.address = address
        self.wif = wif
        self.seed = seed

    def __repr__(self):
        return "address='{}', wif='{}', seed='{}'".format(self.address, self.wif, self.seed)

def GenerateBTC():
    private_key = BitcoinPrivateKey.from_passphrase()
    wif = private_key.to_wif()
    seed = private_key.passphrase()
    address = private_key.public_key().address()
    coin = CryptoCoin(address, wif, seed)
    # line = "{},{},{}\n".format(coin.wif, coin.address, coin.seed)
    return coin

def FormatBTC(coin):
    line = "{},{},{}\n".format(coin.wif, coin.address, coin.seed)
    return line

def GenerateBCH():
    private_key = BitcoinPrivateKey.from_passphrase()
    # seed = private_key.passphrase()
    # private_key._compressed = True
    wif = private_key.to_wif()
    address = convert.to_cash_address(private_key.public_key().address())
    coin = CryptoCoin(address.replace('bitcoincash:', ''), wif)
    return coin

def FormatBCH(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

def GenerateLTC():
    private_key = LitecoinPrivateKey.from_passphrase()
    # seed = private_key.passphrase()
    wif = private_key.to_wif()
    address = private_key.public_key().address()
    coin = CryptoCoin(address, wif)
    return coin

def FormatLTC(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

def GenerateDASH():
    private_key = DashPublicKey.from_passphrase()
    # private_key._compressed = True
    wif = private_key.to_wif()
    address = private_key.public_key().address()
    coin = CryptoCoin(address, wif)
    return coin

def FormatDASH(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

def GenerateCLUB():
    private_key = ClubCoinPublicKey.from_passphrase()
    # private_key._compressed = True
    wif = private_key.to_wif()
    address = private_key.public_key().address()
    coin = CryptoCoin(address, wif)
    return coin

def FormatCLUB(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

def GeneratePOTE():
    private_key = PotCoinPublicKey.from_passphrase()
    # private_key._compressed = True
    wif = private_key.to_wif()
    address = private_key.public_key().address()
    coin = CryptoCoin(address, wif)
    return coin

def FormatPOTE(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

def GenerateETH():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    priv_hex = codecs.encode(priv.to_string(),'hex')
    coin = CryptoCoin("0x{}".format(address), priv_hex)
    # line = "{},0x{}\n".format(priv_hex, address)
    return coin

def FormatETH(coin):
    line = "{},{}\n".format(coin.wif, coin.address)
    return line

# TODO Add this coins
# def GenerateXMR():
#     seed, sk, vk, addr = account.gen_new_wallet()
#     line = "{},{},{},{}\n".format(addr,vk,sk,seed)
#     return line
#
# def GenerateWaves():
#     addr = pw.Address()
#     line = "{},{},{},{}\n".format(addr.address, addr.publicKey, addr.privateKey, addr.seed)
#     return line

def toNumber(input):
    try:
        return int(input)
    except ValueError:
        print "Please input valid integer! {}".format(input)
        return None

def saveCoinsList(coin, coin_list = [], filename ='address.csv'):
    options = {
        "BTC": FormatBTC,
        "BCH": FormatBCH,
        "LTC": FormatLTC,
        "DASH": FormatDASH,
        'CLUB': FormatCLUB,
        'ETH': FormatETH,
        # 'XMR':FormatXMR, #TODO
        # 'WAVES': FormatWaves, #TODO
        'POTE': FormatPOTE,
    }

    with open(filename, 'w') as file:
        if coin == "XMR":
            file.write("Address,Secret View Key,Secret Spend Key,Secret Mnemonic\n")
        elif coin == "WAVES":
            file.write("Address,Public Key,Private Key,Seed\n")
        elif coin == "BTC":
            file.write("WIF,Address,Seed\n")
        else:
            file.write("WIF,Address\n")
        for coin_item in coin_list:
            line = options[coin](coin_item)
            file.write(line)
            print "{}/{}".format(coin_list.index(coin_item), len(coin_list))
        file.flush()
        file.close()
        print "Done!"

def GenerateAssetIdFromBTC(coin_item):
    coin_address = coin_item.address
    return coin_address[0:6]


def saveAssetIds(coin, coin_list = [], filename ='assetid.txt'):
    options = {
        "BTC": GenerateAssetIdFromBTC,
    }

    with open(filename, 'w') as file:
        for coin_item in coin_list:
            line = "{}\n".format(options[coin](coin_item))
            file.write(line)
            print "Asset IDs {}/{}".format(coin_list.index(coin_item), len(coin_list))
        file.flush()
        file.close()
        print "Done!"

def savePrivateKeys(coin, coin_list = [], filename ='private.txt'):
    with open(filename, 'w') as file:
        for coin_item in coin_list:
            line = "{}\n".format(coin_item.wif)
            file.write(line)
            print "PrivateKeys {}/{}".format(coin_list.index(coin_item), len(coin_list))
        file.flush()
        file.close()
        print "Done!"

def savePublicKeys(coin, coin_list = [], filename ='public.txt'):
    options = {
        "BTC": GenerateAssetIdFromBTC,
    }
    with open(filename, 'w') as file:
        for coin_item in coin_list:
            line = "{},{}\n".format(coin_item.address, options[coin](coin_item))
            file.write(line)
            print "PublicKeys {}/{}".format(coin_list.index(coin_item), len(coin_list))
        file.flush()
        file.close()
        print "Done!"

def init():
    max_iterator_count = 10

    assets_file = 'assetid.txt'
    private_keys_file = 'private.txt'
    public_keys_file = 'public.txt'

    out_file_name = 'address.csv'
    coin = 'BTC'

    output_directory = './'

    if len(argv) >= 4:
        max_iterator_count = toNumber(argv[1])
        output_directory = argv[2]
        coin = argv[3]
    else:
        print "Script will run with default configuration"

    coin = coin.upper()

    if max_iterator_count is None:
        exit(0)

    options = {
        "BTC": GenerateBTC,
        "BCH": GenerateBCH,
        "LTC": GenerateLTC,
        "DASH": GenerateDASH,
        'CLUB': GenerateCLUB,
        'ETH': GenerateETH,
        # 'XMR':GenerateXMR,
        # 'WAVES': GenerateWaves,
        'POTE': GeneratePOTE,
    }
    coins = list(options.keys())
    filename = "{}".format(output_directory + out_file_name)
    if coin in options:
        print "Number of address: {} \nOutput:  {}\nCoin: {} ".format(max_iterator_count, filename, coin)
        coin_list = []
        if (max_iterator_count > 0):
            for i in range(max_iterator_count):
                coin_item = options[coin]()
                coin_list.append(coin_item)
            saveCoinsList(coin, coin_list, filename)
            saveAssetIds(coin, coin_list, output_directory + assets_file)
            savePrivateKeys(coin, coin_list, output_directory + private_keys_file)
            savePublicKeys(coin, coin_list, output_directory + public_keys_file)
        else:
            print "Iterator count should be > 0"
    else:
        print "{} is not supported yet, Supported coins are {}".format(coin, ', '.join(coins))
        print "Usage python script.py <number_of_wallets> <file_name.csv> <coin>"
        print "Usage python script.py 10 wallets.csv BTC"


if __name__ == "__main__":
    init()
