from datetime import date, datetime, timedelta, timezone

import responses

from icf_client import IcfClient
from icf_client import models as m

BOOKING_JSON = {
    'uuid': 'f149068e-300e-452a-a856-3f091239f1d7',
    'resellerReference': '001-002',
    'supplierReference': 'ABC-123',
    'status': 'ON_HOLD',
    'utcHoldExpiration': '2019-10-31T08:30:00Z',
    'utcConfirmedAt': '2019-10-31T08:30:00Z',
    'utcDeliveredAt': '2019-10-31T08:30:00Z',
    'refreshFrequency': 'HOURLY',
    'productId': 'adult',
    'optionId': 'LR1-01',
    'availability': {
        'id': '28271273-a317-40fc-8f42-79725a7072a3',
        'localStartDateTime': '2019-10-31T08:30:00Z',
        'localEndDateTime': '2019-10-31T10:00:00Z'
    },
    'contact': {
        'fullName': 'Mr. Traveller',
        'emailAddress': 'traveller@fake.com',
        'phoneNumber': '+1 555-555-1212',
        'locales': [
            'en-GB',
            'en-US',
            'en'
        ],
        'country': 'GB'
    },
    'deliveryMethods': [
        'VOUCHER'
    ],
    'voucher': {
        'deliveryFormat': 'CODE39',
        'deliveryValue': '01234567890',
        'redemptionMethod': 'DIGITAL',
        'utcDeliveredAt': '2019-10-31T08:30:00Z',
        'utcRedeemedAt': '2019-10-31T08:30:00Z'
    },
    'unitItems': [
        {
            'uuid': '6be0409f-181e-4520-acc1-cc6791896859',
            'unitId': 'adult',
            'resellerReference': '001-002',
            'supplierReference': 'ABC-123',
            'ticket': {
                'deliveryFormat': 'CODE39',
                'deliveryValue': '01234567890',
                'redemptionMethod': 'DIGITAL',
                'utcDeliveredAt': '2019-10-31T08:30:00Z',
                'utcRedeemedAt': '2019-10-31T08:30:00Z'
            }
        }
    ],
}
BOOKING_MODEL = m.Booking(
    uuid='f149068e-300e-452a-a856-3f091239f1d7',
    status='ON_HOLD',
    utcHoldExpiration=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
    utcConfirmedAt=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
    productId='adult',
    optionId='LR1-01',
    availability=m.BookingAvailability(
        id='28271273-a317-40fc-8f42-79725a7072a3',
        localStartDateTime=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
        localEndDateTime=datetime(2019, 10, 31, 10, 0, tzinfo=timezone.utc),
    ),
    contact=m.BookingContact(
        fullName='Mr. Traveller',
        emailAddress='traveller@fake.com',
        phoneNumber='+1 555-555-1212',
        locales=['en-GB', 'en-US', 'en'],
        country='GB'
    ),
    deliveryMethods=['VOUCHER'],
    voucher=m.BookingVoucher(
        deliveryFormat='CODE39',
        deliveryValue='01234567890',
        redemptionMethod='DIGITAL',
        utcDeliveredAt=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
        utcRedeemedAt=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
    ),
    unitItems=[
        m.BookingUnitItemTicket(
            uuid='6be0409f-181e-4520-acc1-cc6791896859',
            unitId='adult',
            ticket=m.BookingTicket(
                deliveryFormat='CODE39',
                deliveryValue='01234567890',
                redemptionMethod='DIGITAL',
                utcDeliveredAt=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
                utcRedeemedAt=datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc),
            ),
            resellerReference='001-002',
            supplierReference='ABC-123'
        )
    ],
    resellerReference='001-002',
    supplierReference='ABC-123',
    refreshFrequency='HOURLY',
)


def test_suppliers_list(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', json=[
        {
            'id': '0001',
            'name': 'Acme Tour Co.',
            'endpoint': 'https://api.my-booking-platform.com/v1',
            'contact': {
                'website': 'https://acme-tours.co.fake',
                'email': 'info@acme-tours.co.fake',
                'telephone': '+1 888-555-1212',
                'address': '123 Main St, Anytown USA'
            }
        }
    ])
    suppliers = client.get_suppliers()
    assert suppliers == [
        m.Supplier(
            id='0001',
            name='Acme Tour Co.',
            endpoint='https://api.my-booking-platform.com/v1',
            contact=m.SupplierContact(
                address='123 Main St, Anytown USA',
                email='info@acme-tours.co.fake',
                telephone='+1 888-555-1212',
                description=None,
                website='https://acme-tours.co.fake'
            )
        )
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/suppliers'
    assert mocked_responses.calls[0].request.headers['Authorization'] == 'Bearer bar'


def test_products(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/products', json=[
        {
            'id': 'a491687f-1dce-4be2-bc47-0157541bc8c1',
            'internalName': 'Studio Tour',
            'reference': 'STUDIO',
            'locale': 'en',
            'timeZone': 'America/Los_Angeles',
            'instantConfirmation': True,
            'instantDelivery': True,
            'availabilityType': 'START_TIME',
            'deliveryFormats': ['PDF_URL', 'QRCODE'],
            'deliveryMethods': ['TICKET', 'VOUCHER'],
            'redemptionMethod': 'DIGITAL',
            'capabilities': [],
            'options': [
                {
                    'id': '345314bb-aaaf-4ba2-b3ef-ff15ea39a0ae',
                    'internalName': 'Studio Tour',
                    'reference': None,
                    'restrictions': {
                        'minUnits': 0,
                        'maxUnits': None
                    },
                    'units': [
                        {
                            'id': 'adult',
                            'internalName': 'Studio Tour',
                            'reference': None,
                            'type': 'ADULT',
                            'restrictions': {
                                'minAge': None,
                                'maxAge': None,
                                'idRequired': False,
                                'minQuantity': 7,
                                'maxQuantity': None,
                                'accompaniedBy': []
                            }
                        }
                    ]
                }
            ]
        }, {
            'id': '3e803053-6f39-46f7-8a67-2114de59b135',
            'internalName': 'VIP Tour',
            'reference': 'VIP',
            'locale': 'en',
            'timeZone': 'America/Los_Angeles',
            'instantConfirmation': True,
            'instantDelivery': True,
            'availabilityType': 'START_TIME',
            'deliveryFormats': ['PDF_URL', 'QRCODE'],
            'deliveryMethods': ['TICKET', 'VOUCHER'],
            'redemptionMethod': 'DIGITAL',
            'capabilities': [],
            'options': [
                {
                    'id': 'DEFAULT',
                    'internalName': 'DEFAULT',
                    'reference': None,
                    'restrictions': {
                        'minUnits': 0,
                        'maxUnits': None
                    },
                    'units': [
                        {
                            'id': 'adult',
                            'internalName': 'VIP Tour',
                            'reference': None,
                            'type': 'ADULT',
                            'restrictions': {
                                'minAge': None,
                                'maxAge': None,
                                'idRequired': False,
                                'minQuantity': 7,
                                'maxQuantity': None,
                                'accompaniedBy': []
                            }
                        }
                    ]
                }
            ]
        }
    ])
    products = client.get_products(supplier_id='foo')
    assert products == [
        m.Product(
            id='a491687f-1dce-4be2-bc47-0157541bc8c1',
            internalName='Studio Tour',
            reference='STUDIO',
            locale='en',
            timeZone='America/Los_Angeles',
            instantConfirmation=True,
            instantDelivery=True,
            availabilityType='START_TIME',
            deliveryFormats=['PDF_URL', 'QRCODE'],
            deliveryMethods=['TICKET', 'VOUCHER'],
            redemptionMethod='DIGITAL',
            capabilities=[],
            options=[
                m.Option(
                    id='345314bb-aaaf-4ba2-b3ef-ff15ea39a0ae',
                    internalName='Studio Tour',
                    units=[
                        m.Unit(
                            id='adult',
                            internalName='Studio Tour',
                            type='ADULT',
                            reference=None
                        )
                    ],
                    reference=None
                )
            ]
        ),
        m.Product(
            id='3e803053-6f39-46f7-8a67-2114de59b135',
            internalName='VIP Tour',
            reference='VIP',
            locale='en',
            timeZone='America/Los_Angeles',
            instantConfirmation=True,
            instantDelivery=True,
            availabilityType='START_TIME',
            deliveryFormats=['PDF_URL', 'QRCODE'],
            deliveryMethods=['TICKET', 'VOUCHER'],
            redemptionMethod='DIGITAL',
            capabilities=[],
            options=[
                m.Option(
                    id='DEFAULT',
                    internalName='DEFAULT',
                    units=[
                        m.Unit(
                            id='adult',
                            internalName='VIP Tour',
                            type='ADULT',
                            reference=None
                        )
                    ],
                    reference=None
                )
            ]
        ),
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == (
        'http://fake-api.local/products?supplierId=foo'
    )


def test_calendar(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/calendar', json=[
        {'localDate': '2020-12-01', 'status': 'AVAILABLE', 'capacity': 392},
        {'localDate': '2020-12-02', 'status': 'AVAILABLE', 'capacity': 102},
        {'localDate': '2020-12-03', 'status': 'CLOSED', 'capacity': 0},
    ])
    availability = client.get_calendar(
        supplier_id='foo',
        product_id='bar',
        option_id='baz',
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 3),
    )
    assert availability == [
        m.DailyAvailability(localDate=date(2020, 12, 1), status='AVAILABLE', capacity=392),
        m.DailyAvailability(localDate=date(2020, 12, 2), status='AVAILABLE', capacity=102),
        m.DailyAvailability(localDate=date(2020, 12, 3), status='CLOSED', capacity=0),
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == (
        'http://fake-api.local/calendar'
        '?supplierId=foo'
        '&productId=bar'
        '&optionId=baz'
        '&localDateStart=2020-01-01'
        '&localDateEnd=2020-01-03'
    )


def test_availability(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/availability', json=[
        {
            'id': '2020-12-01T09:00:00-08:00',
            'localDateTimeStart': '2020-12-01T09:00:00-08:00',
            'localDateTimeEnd': '2020-12-01T11:00:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 14,
            'capacity': 11,
            'maxUnits': 7
        },
        {
            'id': '2020-12-01T09:30:00-08:00',
            'localDateTimeStart': '2020-12-01T09:30:00-08:00',
            'localDateTimeEnd': '2020-12-01T11:30:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 13,
            'capacity': 12,
            'maxUnits': 7
        },
        {
            'id': '2020-12-01T10:00:00-08:00',
            'localDateTimeStart': '2020-12-01T10:00:00-08:00',
            'localDateTimeEnd': '2020-12-01T12:00:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 12,
            'capacity': 13,
            'maxUnits': 6
        },
    ])
    availability = client.get_availability(
        supplier_id='foo',
        product_id='bar',
        option_id='baz',
        start_date=date(2020, 12, 1),
        end_date=date(2020, 12, 2),
    )
    assert availability == [
        m.AvailabilityStatus(
            id='2020-12-01T09:00:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 9, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 11, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=14,
            capacity=11,
            maxUnits=7,
        ),
        m.AvailabilityStatus(
            id='2020-12-01T09:30:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 9, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 11, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=13,
            capacity=12,
            maxUnits=7,
        ),
        m.AvailabilityStatus(
            id='2020-12-01T10:00:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 10, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 12, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=12,
            capacity=13,
            maxUnits=6,
        ),
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == (
        'http://fake-api.local/availability'
        '?supplierId=foo'
        '&productId=bar'
        '&optionId=baz'
        '&localDateStart=2020-12-01'
        '&localDateEnd=2020-12-02'
    )


def test_test_reservation(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.POST, 'http://fake-api.local/availability', json=[
        {
            'id': '2020-12-01T15:30:00-08:00',
            'localDateTimeStart': '2020-12-01T15:30:00-08:00',
            'localDateTimeEnd': '2020-12-01T17:30:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 14,
            'capacity': 11,
            'maxUnits': 7
        }
    ])
    availability = client.test_reservation(
        supplier_id='foo',
        product_id='bar',
        option_id='baz',
        availability_ids=['2020-12-01T15:30:00-08:00'],
        units=[m.UnitQuantity(id='adult', quantity=2)],
    )
    assert availability == [
        m.AvailabilityStatus(
            id='2020-12-01T15:30:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 15, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 17, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=14,
            capacity=11,
            maxUnits=7,
        )
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/availability?supplierId=foo'


def test_reservation(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.POST, 'http://fake-api.local/reservations', json=BOOKING_JSON)
    reservation = client.create_reservation(
        supplier_id='foo',
        booking_request=m.BookingRequest(
            uuid='f149068e-300e-452a-a856-3f091239f1d7',
            productId='adult',
            optionId='LR1-01',
            availabilityId='28271273-a317-40fc-8f42-79725a7072a3',
            unitItems=[
                m.UnitItem(
                    uuid='6be0409f-181e-4520-acc1-cc6791896859',
                    unitId='adult',
                )
            ],
        ),
    )
    assert reservation == BOOKING_MODEL
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/reservations?supplierId=foo'


def test_reservation_confirm(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.PUT, 'http://fake-api.local/reservations', json=BOOKING_JSON)
    reservation = client.confirm_reservation(
        supplier_id='foo',
        confirmation_request=m.BookingConfirmationRequest(
            uuid='7df49d62-57ad-44be-8373-e4c2fe7e63fe',
            resellerReference='001-002',
            contact=m.BookingContact(
                fullName='Mr. Traveller',
                emailAddress='traveller@fake.local',
                phoneNumber='+1 555-555-1212',
                locales=['en-GB', 'en-US', 'en'],
                country='GB',
            )
        )
    )
    assert reservation == BOOKING_MODEL
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/reservations?supplierId=foo'


def test_booking_details(client: IcfClient, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/bookings', json=BOOKING_JSON)
    reservation = client.get_booking_details(
        supplier_id='foo',
        uuid='f149068e-300e-452a-a856-3f091239f1d7'
    )
    assert reservation == BOOKING_MODEL
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == (
        'http://fake-api.local/bookings'
        '?supplierId=foo'
        '&uuid=f149068e-300e-452a-a856-3f091239f1d7'
    )
