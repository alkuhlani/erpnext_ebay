"""A module of eBay constants"""

import frappe

# Assumed maximum length of eBay attributes and values
EBAY_ATTR_LEN = 100
EBAY_ATTR_LEN_STR = str(EBAY_ATTR_LEN)
EBAY_VALUE_LEN = 1000
EBAY_VALUE_LEN_STR = str(EBAY_VALUE_LEN)

# eBay PaymentMethods and their descriptions
PAYMENT_METHODS = {'AmEx': 'American Express',
                   'CashInPerson': 'Cash in person (US/CA Motors only)',
                   'CashOnPickup': 'Payment on delivery',
                   'CCAccepted': 'Credit card',
                   'COD': 'Cash on delivery (not US/CA/UK)',
                   'CODPrePayDelivery': '(reserved)',
                   'CreditCard': 'Credit card (eBay Now only)',
                   'Diners': 'Diners Club Card (Cybersource Gateway sellers)',
                   'DirectDebit': 'Debit card (eBay Now only)',
                   'Discover': 'Discover card',
                   'ELV': 'Elektronisches Lastschriftverfahren (obselete)',
                   'Escrow': '(reserved)',
                   'IntegratedMerchantCreditCard':
                       'Credit card (payment gateway)',
                   'LoanCheck': 'Loan check (US/CA Motors only)',
                   'MOCC': "Money order/cashiers' cheque",
                   'MoneyXferAccepted': 'Money/bank transfer',
                   'MoneyXferAcceptedInCheckout':
                       'Money/bank transfer (displayed at checkout)',
                   'None': 'No payment method specified',
                   'Other': 'Other',
                   'OtherOnlinePayments': 'Other online payment',
                   'PaisaPayAccepted': 'PaisaPay (India only)',
                   'PaisaPayEscrow': 'PaisaPay Escrow (India only)',
                   'PaisaPayEscrowEMI':
                       'PaisaPay Escrow equal monthly installments '
                       + '(India only)',
                   'PaymentSeeDescription':
                       'See description for payment details',
                   'PayOnPickup': 'Pay on pickup',
                   'PayPal': 'Paypal',
                   'PayPalCredit': 'Paypal credit card',
                   # PayUponInvoice is not a valid option for listing
                   'PayUponInvoice': 'Pay Upon Invoice (DE only)',
                   'PersonalCheck': 'Personal cheque',
                   'PostalTransfer': '(reserved)',
                   'PrePayDelivery': '(reserved)',
                   'VisaMC': 'Visa/Mastercard'}

PAYMENT_METHODS_SUPPORTED = ('AmEx', 'CashOnPickup', 'CCAccepted',
                             'CreditCard', 'Discover',
                             'IntegratedMerchantCreditCard', 'MOCC',
                             'MoneyXferAccepted', 'None', 'Other',
                             'OtherOnlinePayments', 'PaymentSeeDescription',
                             'PayPal', 'PayPalCredit', 'PersonalCheck',
                             'VisaMC')

# eBay listing types, and their descriptions
LISTING_TYPES = {'AdType': 'Advertisement',
                 'Auction': None,
                 'Chinese': 'Auction',
                 'Live': None,
                 'FixedPriceItem': 'Buy It Now',
                 'LeadGeneration': 'Advertisement',
                 'PersonalOffer': 'Second Chance Offer',
                 'StoresFixedPrice': 'Buy It Now (eBay Store)'}
# Listing types we use - these should be permissible site-wide as there is
# no checking by category for listing types
LISTING_TYPES_SUPPORTED = ('Chinese', 'FixedPriceItem', 'StoresFixedPrice')

# Feature columns

# Not supported (usually because they are array types)
FEATURES_NOT_SUPPORTED = ('GalleryFeaturedDurations',
                          'StoreOwnerExtendedListingDurations')
# The extra columns produced for ListingDuration
LISTING_DURATION_COLUMNS = tuple(
    'ListingDuration' + x for x in LISTING_TYPES)
# The columns chosen to be stored in the base, rather than extra, table
_BASE_COLUMNS = (
    'CompatibleVehicleType', 'ExpressEnabled', 'GlobalShippingEnabled',
    'MaxFlatShippingCost', 'MaxFlatShippingCostCurrency', 'ConditionEnabled')
# Features removed to separate tables
FEATURES_REMOVED = (
    'ConditionValues', 'ListingDurations', 'PaymentMethods')
# Extra columns to the base table
FEATURES_BASE_ADDED = ('ConditionHelpURL',)

# Columns of the basic features table
# NOTE - changes here should be matched by changes to the SQL query creating
# the table
FEATURES_BASE_COLUMNS = (('CategoryID',)
                         + LISTING_DURATION_COLUMNS
                         + _BASE_COLUMNS
                         + FEATURES_BASE_ADDED)

# These FeatureDefinitions are not stored in the 'extra' table
# For now this includes 'complicated' features like ListingDurations
FEATURES_NOT_EXTRA = (('CategoryID',)
                      + FEATURES_REMOVED
                      + _BASE_COLUMNS)

# Listing code tokens
days = (1, 3, 5, 7, 10, 14, 21, 28, 30, 60, 90, 120)
low_num = ['One', 'Two', 'Three', 'Four', 'Five',
           'Six', 'Seven', 'Eight', 'Nine']
tokens = ['Days_' + str(n) for n in days]
descriptions = ['{}-day listing'.format(
    low_num[n-1] if n < len(low_num) else str(n))
    for n in days]
LISTING_DURATION_TOKENS = (tuple(zip(tokens, days, descriptions))
                           + (('GTC', None, "Good 'Til Cancelled"),))
LISTING_DURATION_TOKEN_DICT = {
    x[0]: (x[1], x[2]) for x in LISTING_DURATION_TOKENS}
del low_num, days, tokens, descriptions

MAX_AUTOPAY_PRICE = 2500.0

@frappe.whitelist()
def get_ebay_constants():
    """Return eBay constants such as the supported listing types"""
    return_dict = {}
    return_dict['listing_type'] = [
        {'value': x, 'label': LISTING_TYPES[x]}
        for x in LISTING_TYPES_SUPPORTED]

    return_dict['payment_methods'] = [
        {'value': x,
         'label': PAYMENT_METHODS[x]}
        for x in PAYMENT_METHODS_SUPPORTED]

    return_dict['MAX_AUTOPAY_PRICE'] = MAX_AUTOPAY_PRICE

    return return_dict