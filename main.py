from pynubank import Nubank
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

nu = Nubank()

# Get credentials from environment variables
cpf = os.getenv('NUBANK_CPF')
password = os.getenv('NUBANK_PASSWORD')
cert_path = os.getenv('NUBANK_CERT_PATH', './do_certificado.p12')

# Authenticate with credentials from environment variables
refresh_token = nu.authenticate_with_cert(cpf, password, cert_path)

# Numa futura utilização é possível fazer o login só com o token
nu.authenticate_with_refresh_token(refresh_token, cert_path)

print(nu.get_account_balance())